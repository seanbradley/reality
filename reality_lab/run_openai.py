"""Optional isolated Responses API runner. Dry-run by default; never reads answer keys."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

from core import digest
from lab import read_rows

ENDPOINT = "https://api.openai.com/v1/responses"


def payload(job: dict, model: str, settings: dict) -> dict:
    """Expose only requested generation settings; prohibit tools, memory, and hidden inputs."""
    if not set(settings) <= {"reasoning", "temperature", "top_p"}:
        raise ValueError("Settings may contain only reasoning, temperature, or top_p")
    serialized = (
        job["input"]
        if isinstance(job["input"], str)
        else json.dumps(job["input"], ensure_ascii=False, sort_keys=True)
    )
    if digest(job["instructions"] + "\n" + serialized) != job["input_sha256"]:
        raise ValueError("Request text differs from the recorded hash")
    return {
        "model": model,
        "instructions": job["instructions"],
        "input": job["input"],
        "max_output_tokens": job["max_output_tokens"],
        "store": False,
        "tools": [],
        "truncation": "disabled",
        **settings,
    }


def extract_text(response: dict) -> str:
    """Read only visible assistant output text; do not grade reasoning items."""
    return "".join(
        item.get("text", "")
        for message in response.get("output", [])
        if message.get("type") == "message"
        for item in message.get("content", [])
        if item.get("type") == "output_text"
    )


def estimate(job: dict, input_price: float, output_price: float) -> float:
    """Conservative planning estimate, not a provider-enforced billing cap."""
    input_allowance = 1.2 * job["text_input_tokens"] + 256
    return (
        input_allowance * input_price + job["max_output_tokens"] * output_price
    ) / 1_000_000


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=Path, required=True)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument(
        "--model",
        required=True,
        help="Explicit available model ID; use a pinned snapshot if offered",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        help="Optional JSON generation settings, retained verbatim",
    )
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--input-usd-per-million", type=float)
    parser.add_argument("--output-usd-per-million", type=float)
    parser.add_argument("--max-estimated-usd", type=float, default=0)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("Limit must be positive")
    jobs = read_rows(args.jobs)
    if len({job["job_id"] for job in jobs}) != len(jobs):
        parser.error("Jobs contain duplicate IDs")
    existing = read_rows(args.responses) if args.responses.exists() else []
    if len({row["job_id"] for row in existing}) != len(existing):
        parser.error("Responses contain duplicate IDs")
    for row in existing:
        if row.get("requested_model") != args.model:
            parser.error(
                "Use a separate response file for each model and setting combination"
            )
    settings = json.loads(args.settings.read_text()) if args.settings else {}
    for row in existing:
        if row.get("request_settings", {}) != settings:
            parser.error("Existing results used different request settings")
    seen = {row["job_id"] for row in existing}
    pending = [job for job in jobs if job["job_id"] not in seen][: args.limit]
    for job in pending:
        payload(job, args.model, settings)
    summary = {
        "mode": "execute" if args.execute else "dry_run",
        "pending_requests": len(pending),
        "requested_model": args.model,
        "settings": settings,
        "text_input_tokens": sum(job["text_input_tokens"] for job in pending),
        "max_output_tokens": sum(job["max_output_tokens"] for job in pending),
        "billing_note": "Estimates require current prices and a matching tokenizer; provider framing is approximate.",
    }
    prices = (args.input_usd_per_million, args.output_usd_per_million)
    if all(price is not None and price >= 0 for price in prices):
        summary["estimated_max_usd"] = sum(estimate(job, *prices) for job in pending)
    print(json.dumps(summary, indent=2), flush=True)
    if not args.execute:
        return
    if (
        any(price is None or price < 0 for price in prices)
        or args.max_estimated_usd <= 0
    ):
        parser.error(
            "Execution requires both current per-million prices and a positive estimated spending cap"
        )
    token = os.environ.get("OPENAI_API_KEY")
    if not token:
        parser.error("OPENAI_API_KEY is not configured in this execution environment")
    spent = sum(row.get("accounted_usd", 0) for row in existing)
    args.responses.parent.mkdir(parents=True, exist_ok=True)
    for job in pending:
        reservation = estimate(job, *prices)
        if spent + reservation > args.max_estimated_usd:
            print(
                "Stopped before the next request: estimated spending allowance exhausted."
            )
            break
        data = payload(job, args.model, settings)
        started = time.time()
        record = {
            "job_id": job["job_id"],
            "input_sha256": job["input_sha256"],
            "requested_model": args.model,
            "request_settings": settings,
            "request_payload": data,
            "started_at_unix": started,
            "price_input_usd_per_million": prices[0],
            "price_output_usd_per_million": prices[1],
            "estimated_reserved_usd": reservation,
        }
        # Persist an attempt before sending; an interrupted request must be reviewed before retrying.
        attempts = args.responses.with_suffix(args.responses.suffix + ".attempts.jsonl")
        prior_attempts = read_rows(attempts) if attempts.exists() else []
        if any(row["job_id"] == job["job_id"] for row in prior_attempts):
            raise SystemExit(
                "Unresolved prior attempt found. Inspect it before any manual retry."
            )
        with attempts.open("a") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        request = urllib.request.Request(
            ENDPOINT,
            json.dumps(data).encode(),
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as connection:
                response = json.load(connection)
            record.update(
                {
                    "status": response.get("status", "unknown"),
                    "text": extract_text(response),
                    "returned_model": response.get("model"),
                    "response_id": response.get("id"),
                    "usage": response.get("usage"),
                    "response": response,
                }
            )
            usage = response.get("usage") or {}
            if not all(
                isinstance(usage.get(key), int)
                for key in ("input_tokens", "output_tokens")
            ):
                record["accounted_usd"] = reservation
                record["stop_reason"] = "missing_usage"
            else:
                # Cached tokens are conservatively charged at the uncached input rate.
                record["accounted_usd"] = (
                    usage["input_tokens"] * prices[0]
                    + usage["output_tokens"] * prices[1]
                ) / 1_000_000
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            record.update(
                {
                    "status": "request_outcome_uncertain",
                    "text": "",
                    "error_type": type(error).__name__,
                    "accounted_usd": reservation,
                    "stop_reason": "no_automatic_retry",
                }
            )
        record["elapsed_seconds"] = time.time() - started
        with args.responses.open("a") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        spent += record["accounted_usd"]
        print(
            json.dumps(
                {
                    "job_id": job["job_id"],
                    "status": record["status"],
                    "accounted_usd_total": spent,
                }
            ),
            flush=True,
        )
        if record.get("stop_reason") or record["status"] != "completed":
            break


if __name__ == "__main__":
    main()

"""Prepare a separate, unblinded historical-example diagnostic; not a held-out test."""

import json
from pathlib import Path

from core import READER_INSTRUCTIONS, TokenCounter, reader_user
from lab import get_data, make_job, save_rows

ROOT = Path(__file__).resolve().parent


def main() -> None:
    audit = json.loads((ROOT / "data/historical_measurements.json").read_text())
    _, questions = get_data()
    counter = TokenCounter()
    jobs = []
    for method, source in {**audit["strings"], "empty_diagnostic": ""}.items():
        for question in (q for q in questions if q["case_id"] == "R04"):
            jobs.append(
                make_job(
                    "reader",
                    {
                        "case_id": "R04",
                        "question_id": question["question_id"],
                        "method": method,
                        "fraction": None,
                        "repeat": 0,
                        "cluster_id": "reality_project",
                        "context_tokens": counter.count(source),
                        "development_only": True,
                        "comparison_note": "Different actual sizes; no equal-budget or held-out claim.",
                    },
                    READER_INSTRUCTIONS,
                    reader_user(source, question["question"], question["options"]),
                    counter,
                    2048,
                )
            )
    save_rows(ROOT / "results/worked_example/reader_jobs.jsonl", jobs)
    print(json.dumps({"requests_prepared": len(jobs), "model_calls_completed": 0}))


if __name__ == "__main__":
    main()

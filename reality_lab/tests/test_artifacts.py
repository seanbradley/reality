"""Check packaged probes and replay inputs independently of any live model service."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import TokenCounter, macro_encode
from gregg_probe import marked, plain
from lab import get_data, read_rows
from run_openai import payload

ROOT = Path(__file__).resolve().parents[1]


class ArtifactTests(unittest.TestCase):
    def test_all_development_sources_roundtrip_without_expansion(self):
        sources, _ = get_data()
        for encoding in ("cl100k_base", "o200k_base"):
            counter = TokenCounter(encoding)
            for source in sources:
                result = macro_encode(source["source"], counter)
                self.assertEqual(result.decode(), source["source"])
                self.assertLessEqual(
                    counter.count(result.render()), counter.count(source["source"])
                )

    def test_gregg_collision_is_reproducible(self):
        self.assertEqual(plain("They are in."), plain("They are not."))

    def test_disambiguated_gregg_and_control_are_reversible(self):
        source = "have in not it at for from form be but"
        for arbitrary in (False, True):
            encoded = marked(source, arbitrary)
            self.assertEqual(encoded.decode(), source)
            self.assertEqual(len(encoded.dictionary), 10)

    def test_historical_token_measurements_reproduce(self):
        data = json.loads((ROOT / "data/historical_measurements.json").read_text())
        for encoding in ("cl100k_base", "o200k_base"):
            counter = TokenCounter(encoding)
            for row in data["measurements"]:
                self.assertEqual(
                    counter.count(data["strings"][row["representation"]]), row[encoding]
                )

    def test_replay_payloads_exclude_the_target_archived_answer(self):
        bank = {
            item["prompt_id"]: item
            for item in read_rows(ROOT / "data/worldview_archive_gold.jsonl")
        }
        jobs = read_rows(ROOT / "results/worldview_reader_jobs.jsonl")
        self.assertEqual(len(jobs), 24)
        for job in jobs:
            request = payload(job, "explicit-model-id", {})
            record = bank[job["prompt_id"]]
            self.assertEqual(request["input"][-1]["role"], "user")
            self.assertTrue(
                request["input"][-1]["content"].endswith(record["archived_question"])
            )
            self.assertNotIn(
                record["archived_answer"],
                "\n".join(message["content"] for message in request["input"]),
            )
            self.assertNotIn("archived_answer", request)


if __name__ == "__main__":
    unittest.main()

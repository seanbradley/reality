"""Behavioral tests for data integrity, codec correctness, budgets, and scoring."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import (
    Encoded,
    TokenCounter,
    digest,
    macro_encode,
    parse_answer,
    uniform_extract,
)
from lab import (
    compressor_jobs,
    evaluation_slots,
    get_data,
    materialize_compressions,
    reader_jobs,
    score,
    validate_data,
)
from run_openai import extract_text, payload


class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counter = TokenCounter()
        cls.sources, cls.questions = get_data()

    def test_source_spans_and_hashes(self):
        self.assertEqual(validate_data()["questions"], 36)

    def test_roundtrip_unicode_and_delimiters(self):
        for text in (
            "αβ 中文 🙂",
            "Use §, ~, @ and ¤ literally.",
            "not not not, and NOT.",
        ):
            encoded = macro_encode(text, self.counter)
            self.assertEqual(encoded.decode(), text)
            self.assertLessEqual(
                self.counter.count(encoded.render()), self.counter.count(text)
            )

    def test_positive_repetition_control(self):
        sentence = "The recorded hypothesis remains uncertain until an independently controlled experiment is completed. "
        text = sentence * 40
        encoded = macro_encode(text, self.counter)
        self.assertTrue(encoded.dictionary)
        self.assertEqual(encoded.decode(), text)
        self.assertLess(self.counter.count(encoded.render()), self.counter.count(text))

    def test_dictionary_is_not_recursive(self):
        self.assertEqual(Encoded("x y", {"x": "y", "y": "z"}).decode(), "y z")

    def test_unicode_head_is_a_prefix_within_budget(self):
        text = "🙂漢字αβ test " * 10
        for budget in range(20):
            clipped = self.counter.head(text, budget)
            self.assertTrue(text.startswith(clipped))
            self.assertLessEqual(self.counter.count(clipped), budget)

    def test_extractive_budget(self):
        for source in self.sources:
            for budget in (0, 16, 64):
                self.assertLessEqual(
                    self.counter.count(
                        uniform_extract(source["source"], budget, self.counter)
                    ),
                    budget,
                )

    def test_no_test_questions_in_compressor_requests(self):
        jobs = compressor_jobs(self.sources, [0.5], self.counter)
        for job in jobs:
            self.assertNotIn("gold", job)
            self.assertNotIn("options", job)
            self.assertNotIn("question_id", job)
            for question in self.questions:
                self.assertNotIn(question["question"], job["input"])
                self.assertNotIn(question["question"], job["instructions"])

    def test_oversized_compressor_is_rejected_without_truncation(self):
        jobs = compressor_jobs(self.sources[:1], [0.5], self.counter)
        job = jobs[0]
        outputs = [
            {
                "job_id": job["job_id"],
                "input_sha256": job["input_sha256"],
                "status": "completed",
                "text": self.sources[0]["source"],
            }
        ]
        accepted, rejected = materialize_compressions(jobs, outputs, self.counter)
        self.assertFalse(accepted)
        self.assertEqual(rejected[0]["reason"], "over_budget")

    def test_missing_is_not_a_model_result(self):
        jobs = reader_jobs(self.sources[:1], self.questions, [0.5], self.counter, 1, {})
        result = score(jobs, [], self.questions)
        self.assertEqual(result["status"], "not_run")
        self.assertTrue(
            all(
                group["accuracy_observed"] is None
                for group in result["groups"].values()
            )
        )

    def test_failed_compressions_remain_in_evaluation_denominator(self):
        sources = self.sources[:1]
        compressors = compressor_jobs(sources, [0.5], self.counter)
        readers = reader_jobs(sources, self.questions, [0.5], self.counter, 1, {})
        rejected = [{"job_id": compressors[0]["job_id"], "reason": "over_budget"}]
        slots = evaluation_slots(
            sources, self.questions, [0.5], 1, readers, rejected, compressors
        )
        self.assertEqual(len(slots), 21)
        result = score(readers, [], self.questions, slots)
        group = result["groups"]["prose@0.5"]
        self.assertEqual(group["planned"], 3)
        self.assertEqual(group["compression_failures"], 3)
        self.assertEqual(group["accuracy_intention_to_test"], 0)
        self.assertIsNone(group["accuracy_observed"])

    def test_wrong_answer_and_invalid_json_are_penalized(self):
        jobs = reader_jobs(
            self.sources[:1], self.questions, [0.5], self.counter, 1, {}
        )[:3]
        qmap = {question["question_id"]: question for question in self.questions}
        outputs = []
        for index, job in enumerate(jobs):
            question = qmap[job["question_id"]]
            answer = (
                question["gold"]
                if index == 0
                else next(k for k in question["options"] if k != question["gold"])
            )
            outputs.append(
                {
                    "job_id": job["job_id"],
                    "input_sha256": job["input_sha256"],
                    "status": "completed",
                    "text": json.dumps({"answer": answer}) if index != 2 else "A",
                }
            )
        group = next(iter(score(jobs, outputs, self.questions)["groups"].values()))
        self.assertEqual(
            (group["correct"], group["invalid"], group["observed"]), (1, 1, 3)
        )

    def test_duplicate_and_wrong_hash_rejected(self):
        jobs = reader_jobs(
            self.sources[:1], self.questions, [0.5], self.counter, 1, {}
        )[:1]
        output = {
            "job_id": jobs[0]["job_id"],
            "input_sha256": "wrong",
            "text": '{"answer":"A"}',
        }
        with self.assertRaises(ValueError):
            score(jobs, [output], self.questions)
        output["input_sha256"] = jobs[0]["input_sha256"]
        with self.assertRaises(ValueError):
            score(jobs, [output, output], self.questions)

    def test_answer_schema_is_strict(self):
        for value in (
            "A",
            '```json\n{"answer":"A"}\n```',
            '{"answer":"E"}',
            '{"answer":"A","why":"x"}',
        ):
            self.assertIsNone(parse_answer(value, set("ABCD")))
        self.assertEqual(parse_answer('{"answer":"B"}', set("ABCD")), "B")

    def test_api_payload_is_isolated_and_does_not_include_gold(self):
        job = reader_jobs(self.sources[:1], self.questions, [0.5], self.counter, 1, {})[
            0
        ]
        value = payload(job, "explicit-model-id", {})
        self.assertFalse(value["store"])
        self.assertEqual(value["tools"], [])
        self.assertNotIn("previous_response_id", value)
        self.assertNotIn("gold", value)
        with self.assertRaises(ValueError):
            payload(job, "explicit-model-id", {"tools": ["web_search"]})

    def test_visible_text_extraction_ignores_reasoning(self):
        response = {
            "output": [
                {"type": "reasoning", "text": "ignored"},
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": '{"answer":"C"}'}],
                },
            ]
        }
        self.assertEqual(extract_text(response), '{"answer":"C"}')

    def test_hash_is_sensitive_to_qualification(self):
        self.assertNotEqual(digest("may cause cooling"), digest("causes cooling"))


if __name__ == "__main__":
    unittest.main()

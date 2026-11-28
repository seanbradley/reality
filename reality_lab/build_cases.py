"""Build auditable DEVELOPMENT cases from the two selected Reality export objects."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from core import digest

ROOT = Path(__file__).resolve().parent


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    archive = json.loads(args.archive.read_text())
    messages = {}
    for part, conversation in enumerate(archive, 1):
        mapping, node = conversation["mapping"], conversation["current_node"]
        path = []
        while node:
            value = mapping[node]
            if value.get("message"):
                path.append(value["message"])
            node = value.get("parent")
        for index, message in enumerate(reversed(path), 1):
            label = f"P{part}-M{index:03d}"
            messages[label] = {
                "label": label,
                "conversation_id": conversation["id"],
                "message_id": message["id"],
                "role": message["author"]["role"],
                "timestamp": message.get("create_time"),
                "model_slug": message.get("metadata", {}).get("model_slug"),
                "text": "\n".join(
                    p for p in message["content"].get("parts", []) if isinstance(p, str)
                ),
            }
    sources, questions = [], []

    def add(
        case_id: str, domain: str, labels: list[str] | None, text: str = ""
    ) -> dict:
        refs = [messages[label] for label in labels] if labels else []
        source = (
            "\n\n".join(
                f"[{ref['label']}; {ref['role']}]\n{ref['text']}" for ref in refs
            )
            if refs
            else text
        )
        row = {
            "case_id": case_id,
            "domain": domain,
            "split": "development",
            "source_kind": "archive" if refs else "synthetic_assistant_authored",
            "cluster_id": "reality_project" if refs else case_id,
            "independence_note": "All cases are development material; synthetic cases share one author.",
            "source": source,
            "source_sha256": digest(source),
            "references": refs,
        }
        sources.append(row)
        return row

    def ask(
        case: dict,
        question: str,
        correct: str,
        distractors: list[str],
        quote: str,
        category: str,
        harmful: list[str] | None = None,
    ) -> None:
        index = sum(q["case_id"] == case["case_id"] for q in questions) + 1
        qid = f"{case['case_id']}-Q{index}"
        choices = [correct, *distractors]
        if len(choices) != 4 or len(set(choices)) != 4:
            raise ValueError("Every question needs four distinct choices")
        random.Random(qid).shuffle(choices)
        options = dict(zip("ABCD", choices, strict=True))
        start = case["source"].index(quote)
        questions.append(
            {
                "question_id": qid,
                "case_id": case["case_id"],
                "question": question,
                "options": options,
                "gold": next(k for k, v in options.items() if v == correct),
                "category": category,
                "critical": category in {"status", "revision", "negation", "quantity"},
                "harmful_options": [
                    k for k, v in options.items() if v in (harmful or [])
                ],
                "evidence": [
                    {"start": start, "end": start + len(quote), "quote": quote}
                ],
                "annotation_status": "assistant_draft_requires_independent_review",
            }
        )

    c = add("R01", "science", ["P2-M233", "P2-M234"])
    ask(
        c,
        "How does the assistant qualify the proposed unification?",
        "Speculative and incomplete.",
        [
            "Experimentally established.",
            "A proven mathematical theorem.",
            "The source gives no qualification.",
        ],
        "this is a speculative and incomplete attempt at unification",
        "status",
        ["Experimentally established.", "A proven mathematical theorem."],
    )
    ask(
        c,
        "What kind of artifact does the assistant offer?",
        "A high-level conceptual framework.",
        [
            "A fitted quantitative model with test results.",
            "A new experimental dataset.",
            "A completed proof of consciousness.",
        ],
        "a high-level conceptual framework",
        "relation",
    )
    ask(
        c,
        "What is the proposed role of information?",
        "A possible primary building block.",
        [
            "A proven substitute for all physical measurements.",
            "A concept explicitly excluded from reality.",
            "A synonym for experimental consensus.",
        ],
        "we could consider information as the primary building block",
        "status",
        ["A proven substitute for all physical measurements."],
    )

    c = add("R02", "science", ["P2-M299", "P2-M300"])
    ask(
        c,
        "What expansion of I2F is given?",
        "Information-Interconnectedness Framework",
        [
            "Integrated Information and Function",
            "Interdisciplinary Intelligence Framework",
            "Information-Interaction Formula",
        ],
        "Information-Interconnectedness Framework (I2F)",
        "relation",
    )
    ask(
        c,
        "Which pair is an explicitly named core principle?",
        "Subjectivity and objectivity",
        ["Locality and determinism", "Energy and momentum", "Faith and certainty"],
        "5. Subjectivity and objectivity:",
        "relation",
    )
    ask(
        c,
        "How is reality described in the third principle?",
        "As potentially hierarchically organized, with level-specific laws.",
        [
            "As having no levels of organization.",
            "As governed by one experimentally proven consciousness equation.",
            "As a digital simulation proven by the listed theories.",
        ],
        "This unified theory could consider reality as a hierarchically organized system",
        "status",
        [
            "As governed by one experimentally proven consciousness equation.",
            "As a digital simulation proven by the listed theories.",
        ],
    )

    c = add("R03", "science", ["P1-M154", "P1-M156"])
    ask(
        c,
        "How does the assistant characterize its empirical-support values?",
        "Qualitative approximations.",
        [
            "Exact citation totals.",
            "Measured probabilities from a representative survey.",
            "Results of newly run experiments.",
        ],
        "qualitative approximations",
        "status",
        [
            "Exact citation totals.",
            "Measured probabilities from a representative survey.",
            "Results of newly run experiments.",
        ],
    )
    ask(
        c,
        "Does this response report actively counting citations in real time?",
        "No; it explicitly denies doing so.",
        [
            "Yes; it reports a new live count.",
            "Yes; it names the citation-count API.",
            "The response does not discuss real-time counting.",
        ],
        "I do not actively read or count citations in real-time",
        "negation",
        ["Yes; it reports a new live count.", "Yes; it names the citation-count API."],
    )
    ask(
        c,
        "What is the stated training-data cutoff?",
        "September 2021",
        ["April 2023", "August 2024", "November 2026"],
        "up to September 2021",
        "quantity",
    )

    c = add("R04", "science", ["P2-M457"])
    ask(
        c,
        "Which shape represents Information?",
        "A dodecahedron",
        ["A torus", "A DNA helix", "A fractal tree"],
        "Information is a dodecahedron",
        "relation",
    )
    ask(
        c,
        "Where is Quantum Entanglement nested?",
        "Inside Interconnectedness",
        [
            "Inside Information",
            "Inside Subjectivity and Objectivity",
            "No nesting relationship is specified",
        ],
        "Inside Interconnectedness: Quantum Entanglement (Interlocking spheres)",
        "relation",
    )
    ask(
        c,
        "Which named component belongs to the requested hybrid?",
        "Wolfram ruliad",
        ["Mandelbrot set only", "An anatomical heart", "A weather map"],
        "Wolfram ruliad",
        "relation",
    )

    c = add("R05", "science", ["P2-M445", "P2-M447"])
    ask(
        c,
        "What inconsistency appears in the reserved-character list?",
        "The greater-than sign is listed for both opposing direction groups.",
        [
            "Every direction has a unique unambiguous symbol.",
            "The list contains no arrows.",
            "Only Unicode keys are allowed.",
        ],
        '> reserved for prepositions such as "from" and "below" and boolean less than',
        "negation",
    )
    ask(
        c,
        "What must precede the compressed string?",
        "A dictionary or hashtable.",
        [
            "The answer to a future question.",
            "A bibliography only.",
            "Nothing; dictionaries are prohibited.",
        ],
        "dictionary or hashtable preceding a compressed string",
        "relation",
    )
    ask(
        c,
        "When may a dictionary key exceed one ASCII character under the stated rule?",
        "When the uncompressed prompt or query exceeds 4000 tokens.",
        [
            "When it exceeds 4000 characters.",
            "Whenever a repeated word occurs twice.",
            "Never, without exception.",
        ],
        "unless the uncompressed prompt or query is greater than 4000 tokens",
        "quantity",
    )

    c = add("R06", "science", ["P2-M475", "P2-M476", "P2-M477", "P2-M478", "P2-M479"])
    ask(
        c,
        "Does the assistant enumerate the requested I2F principles here?",
        "No.",
        ["Yes, five principles.", "Yes, three principles.", "Yes, ten principles."],
        "I'm not familiar with the I2F theory and its principles.",
        "negation",
    )
    ask(
        c,
        "What does the response request to help identify I2F?",
        "More details or context.",
        ["An API payment.", "A citation-count dataset.", "A new name for the theory."],
        "If you provide more details or context",
        "relation",
    )
    ask(
        c,
        "What does this exchange alone establish?",
        "The assistant did not identify I2F in this response.",
        [
            "Its entire training set had been erased.",
            "It disproved I2F experimentally.",
            "It had adopted the opposite metaphysical worldview.",
        ],
        "I'm not familiar with the I2F theory and its principles.",
        "status",
        [
            "It disproved I2F experimentally.",
            "It had adopted the opposite metaphysical worldview.",
        ],
    )

    c = add(
        "S01",
        "science",
        None,
        "Researcher, day 1: The coating appears to reduce heating time by 20%; this is a hypothesis based on one trial. "
        "Technician, day 2: The reference timer ran slow. After recalibration, the measured difference is 2%, not 20%. "
        "Researcher, day 3: Instrument uncertainty is ±3 percentage points. We have not tested a second sample. "
        "The draft graph still shows the original 20% label and must be corrected. No statistical-significance claim is justified by this record.",
    )
    ask(
        c,
        "What is the corrected measured difference?",
        "2%",
        ["20%", "3%", "0%"],
        "the measured difference is 2%, not 20%",
        "revision",
        ["20%"],
    )
    ask(
        c,
        "Does the record support claiming a statistically significant improvement?",
        "No.",
        [
            "Yes, with a reported p-value.",
            "Yes, because the draft graph says 20%.",
            "Yes, because uncertainty is zero.",
        ],
        "No statistical-significance claim is justified",
        "status",
        [
            "Yes, with a reported p-value.",
            "Yes, because the draft graph says 20%.",
            "Yes, because uncertainty is zero.",
        ],
    )
    ask(
        c,
        "How many samples have been tested according to the record?",
        "One.",
        ["Two.", "Twenty.", "No sample has been tested."],
        "We have not tested a second sample.",
        "quantity",
    )

    c = add(
        "S02",
        "science",
        None,
        "Analyst: Sites with more trees had lower noon temperatures in an observational survey. "
        "The survey did not randomize planting. Coastal sites also had more trees, so sea breeze is a possible confounder. "
        "Lead: Describe an association, not proof that planting caused cooling. A randomized trial is proposed for next year; it has not begun. "
        "Editor: Keep the coastal-confounding caveat even in the shortened abstract. The current result is not a null finding.",
    )
    ask(
        c,
        "What relationship is supported by the survey?",
        "An association between tree coverage and temperature.",
        [
            "A proven causal effect of planting.",
            "No observed relationship.",
            "A completed randomized-trial result.",
        ],
        "Describe an association, not proof that planting caused cooling.",
        "status",
        ["A proven causal effect of planting.", "A completed randomized-trial result."],
    )
    ask(
        c,
        "What possible confounder is named?",
        "Sea breeze at coastal sites.",
        [
            "A change in thermometer units.",
            "Random assignment.",
            "A greenhouse experiment.",
        ],
        "sea breeze is a possible confounder",
        "relation",
    )
    ask(
        c,
        "Has the proposed randomized trial begun?",
        "No.",
        [
            "Yes, and it succeeded.",
            "Yes, but it failed.",
            "It was completed before the survey.",
        ],
        "it has not begun",
        "negation",
    )

    c = add(
        "W01",
        "software",
        None,
        "Monday requirement: Staging should retry failed jobs three times. Production stays at two retries. "
        "Tuesday correction: Raise the staging retry limit to five; this supersedes the three-retry staging requirement only. "
        "Timeout remains 800 milliseconds in both environments. Never retry authentication failures. "
        "Deployment note: The correction is approved but has not been deployed. Documentation must distinguish desired configuration from running configuration.",
    )
    ask(
        c,
        "What is the latest desired staging retry limit?",
        "Five.",
        ["Three.", "Two.", "Eight hundred."],
        "Raise the staging retry limit to five",
        "revision",
        ["Three."],
    )
    ask(
        c,
        "What timeout and unit remain specified?",
        "800 milliseconds.",
        ["800 seconds.", "5 milliseconds.", "3 seconds."],
        "Timeout remains 800 milliseconds",
        "quantity",
    )
    ask(
        c,
        "Should authentication failures be retried?",
        "No.",
        [
            "Yes, five times in every environment.",
            "Yes, twice in production.",
            "Only after changing the timeout.",
        ],
        "Never retry authentication failures.",
        "negation",
    )

    c = add(
        "W02",
        "software",
        None,
        "Design v1: Cache each raw customer identifier for 24 hours. "
        "Review v2: Do not cache raw identifiers. Cache a keyed digest for 15 minutes; v2 replaces v1. "
        "The secret key is not stored in the cache. The design review did not evaluate resistance to dictionary attacks. "
        "Implementation note: Unit tests pass, but production deployment is pending and no security certification was issued.",
    )
    ask(
        c,
        "What may the revised design cache?",
        "A keyed digest.",
        ["A raw customer identifier.", "The secret key.", "A security certificate."],
        "Cache a keyed digest for 15 minutes",
        "revision",
        ["A raw customer identifier.", "The secret key."],
    )
    ask(
        c,
        "What is the revised cache lifetime?",
        "15 minutes.",
        ["24 hours.", "15 hours.", "24 minutes."],
        "for 15 minutes; v2 replaces v1",
        "quantity",
    )
    ask(
        c,
        "Does passing the unit tests establish security certification?",
        "No certification was issued.",
        [
            "Yes, certification was issued.",
            "Yes, dictionary attacks were ruled out.",
            "Yes, production is certified.",
        ],
        "no security certification was issued",
        "status",
        [
            "Yes, certification was issued.",
            "Yes, dictionary attacks were ruled out.",
            "Yes, production is certified.",
        ],
    )

    c = add(
        "A01",
        "administration",
        None,
        "Initial notice: Meet in Room Cedar at 10:00 Pacific on Thursday. "
        "Organizer correction: Use Room Maple at 11:00 Pacific on Thursday; this replaces both the old room and time. "
        "The Friday workshop remains at 10:00 Pacific in Room Cedar. "
        "Catering says lunch might arrive by 12:30, but has not confirmed. Do not describe lunch delivery as guaranteed.",
    )
    ask(
        c,
        "Where and when is the corrected Thursday meeting?",
        "Room Maple at 11:00 Pacific.",
        [
            "Room Cedar at 10:00 Pacific.",
            "Room Maple at 10:00 Pacific.",
            "Room Cedar at 11:00 Pacific.",
        ],
        "Use Room Maple at 11:00 Pacific on Thursday",
        "revision",
        ["Room Cedar at 10:00 Pacific."],
    )
    ask(
        c,
        "Did the Thursday correction move the Friday workshop?",
        "No; Friday remains unchanged.",
        [
            "Yes; Friday also moves to Maple.",
            "Yes; Friday is cancelled.",
            "Yes; Friday moves to 12:30.",
        ],
        "The Friday workshop remains at 10:00 Pacific in Room Cedar.",
        "negation",
    )
    ask(
        c,
        "What is the status of lunch arriving by 12:30?",
        "Possible but unconfirmed.",
        ["Guaranteed.", "Already delivered.", "Definitely cancelled."],
        "might arrive by 12:30, but has not confirmed",
        "status",
        ["Guaranteed.", "Already delivered."],
    )

    c = add(
        "A02",
        "administration",
        None,
        "Draft purchase record: The equipment total is 1,200 credits. "
        "Corrected record: A 200-credit discount brings the approved total to 1,000 credits. "
        "Approval is recorded; payment has not been sent. The supplier estimates dispatch on June 8, without guaranteeing it. "
        "A separate 80-credit maintenance charge is excluded from the equipment total and remains unapproved.",
    )
    ask(
        c,
        "What is the approved equipment total after the discount?",
        "1,000 credits.",
        ["1,200 credits.", "1,080 credits.", "200 credits."],
        "approved total to 1,000 credits",
        "revision",
        ["1,200 credits."],
    )
    ask(
        c,
        "Has payment been sent?",
        "No.",
        ["Yes, in full.", "Yes, including maintenance.", "Yes, only the discount."],
        "payment has not been sent",
        "negation",
    )
    ask(
        c,
        "Is June 8 dispatch guaranteed?",
        "No; it is an estimate.",
        ["Yes.", "The equipment has already shipped.", "June 8 is the payment date."],
        "estimates dispatch on June 8, without guaranteeing it",
        "status",
        ["Yes.", "The equipment has already shipped."],
    )

    write_jsonl(ROOT / "data/sources.jsonl", sources)
    write_jsonl(ROOT / "data/questions_gold.jsonl", questions)
    print(
        json.dumps(
            {
                "sources": len(sources),
                "questions": len(questions),
                "status": "development_only",
            }
        )
    )


if __name__ == "__main__":
    main()

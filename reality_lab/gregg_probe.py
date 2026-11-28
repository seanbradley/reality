"""Measure a declared Gregg-derived ASCII subset; this is not a full Gregg encoder."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from core import Encoded, TokenCounter

ROOT = Path(__file__).resolve().parent
CHART = "https://greggshorthand.github.io/preanbfs.html"
# Verified rows of the chart. Outline geometry, full phonetics, and phrase rules are excluded.
BRIEFS = {
    "have": "v",
    "in": "n",
    "not": "n",
    "it": "t",
    "at": "t",
    "for": "f",
    "from": "fm",
    "form": "fm",
    "be": "b",
    "but": "b",
}


def plain(text: str) -> str:
    """Apply only the declared, potentially ambiguous lower-case word substitutions."""
    return re.sub(r"\b[a-z]+\b", lambda m: BRIEFS.get(m.group(), m.group()), text)


def marked(text: str, arbitrary: bool = False) -> Encoded:
    """Disambiguate each word with a marked key; include the complete literal dictionary."""
    if "§" in text:
        raise ValueError("Probe delimiter occurs in source")
    present = sorted(
        {m.group() for m in re.finditer(r"\b[a-z]+\b", text)} & BRIEFS.keys()
    )
    by_brief = defaultdict(list)
    for word in present:
        by_brief[BRIEFS[word]].append(word)
    keys = {
        word: f"§{BRIEFS[word]}{by_brief[BRIEFS[word]].index(word)}§"
        for word in present
    }
    if arbitrary:
        # A permutation uses the same key inventory but removes the Gregg word associations.
        values = list(keys.values())
        keys = dict(zip(present, values[1:] + values[:1], strict=True))
    body = re.sub(r"\b[a-z]+\b", lambda m: keys.get(m.group(), m.group()), text)
    encoded = Encoded(body, {key: word for word, key in keys.items()})
    if encoded.decode() != text:
        raise AssertionError("Marked probe failed exact reconstruction")
    return encoded


def main() -> None:
    sources = json.loads((ROOT / "data/historical_measurements.json").read_text())
    original = sources["strings"]["original"]
    synthetic = (
        "I have a form for it, but it must not be in the folder at the office. "
        "The form is from the lab. Keep the words in and not distinct; do not infer "
        "that an observation has been confirmed from its presence in a draft."
    )
    results = []
    for name, text in [
        ("historical_image_prompt", original),
        ("synthetic_function_word_probe", synthetic),
    ]:
        variants = {
            "original": text,
            "plain_gregg_subset_no_decoder": plain(text),
            "marked_gregg_subset_with_decoder": marked(text).render(),
            "arbitrary_permuted_keys_with_decoder": marked(text, True).render(),
        }
        for encoding in ("cl100k_base", "o200k_base"):
            counter = TokenCounter(encoding)
            for variant, value in variants.items():
                results.append(
                    {
                        "source": name,
                        "variant": variant,
                        "encoding": encoding,
                        "tokens": counter.count(value),
                        "characters": len(value),
                    }
                )
    collisions = {
        brief: [word for word, value in BRIEFS.items() if value == brief]
        for brief in set(BRIEFS.values())
        if list(BRIEFS.values()).count(brief) > 1
    }
    result = {
        "status": "mechanical_probe_no_reader_calls",
        "chart_source": CHART,
        "method": "Ten-word verified subset with an experimental text serialization, not full Gregg shorthand.",
        "mapping": BRIEFS,
        "collisions": collisions,
        "minimal_pair": {
            "sources": ["They are in.", "They are not."],
            "encoded": [plain("They are in."), plain("They are not.")],
        },
        "measurements": results,
        "limits": "Unmarked tokens omit decoder costs and are ambiguous; marked conditions are reversible software codecs. No matched-budget reader-performance result exists.",
    }
    (ROOT / "results/gregg_probe.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

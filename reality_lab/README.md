# Reality / Seantongue development experiment kit

Prepared 25 November 2026 for Sean Bradley. **No live model experiment has been run.** This package contains development data, deterministic measurements, executable preparation/scoring code, and an optional OpenAI API runner. It is not a validated benchmark or a trained compressor.

## Research direction

Test whether a compact representation that retains claim status, relationships, and corrections supports useful judgments at smaller context budgets. Ordinary summaries and ordinary structured ledgers are essential controls. Evaluate changes in expressed philosophical positions separately from changes in evidential discipline. Treat training and reference-target predictive loss as a later experiment.

## Contents

- `data/sources.jsonl`: six archival excerpts and six explicitly synthetic sources across science, software, and administration.
- `data/questions_gold.jsonl`: 36 multiple-choice questions, draft answers, critical-field labels, harmful-option labels, and exact supporting spans. Independent annotation review remains necessary.
- `data/historical_measurements.json`: exact historical/example strings and previous measured counts.
- `data/worldview_archive_gold.jsonl`: eight historical questions, answers, export model labels, timestamps, and complete visible prefixes. This is evaluator material, not a reader prompt file.
- `results/pilot/`: full development job plan at 50% and 75% source-payload budgets.
- `results/smoke/`: six-case plan at the 50% budget.
- `results/worked_example/`: 18 separate reader jobs covering the original image prompt, historical abbreviation, published dictionary, published reconstruction, manual structural candidate, and an empty-source diagnostic. Their sizes are unequal; this is a worked-example diagnostic.
- `results/worldview_reader_jobs.jsonl`: 24 fresh-session requests: eight verbatim replays and two leading frames per question. The archived target answer is omitted.
- `results/cl100k/`, `results/o200k/`, `results/gregg_probe.json`: completed static measurements.
- `tests/`: software and artifact checks. Artificial outputs inside unit tests are test fixtures, never scientific results.

The kit contains selected project excerpts, not the full-account export. No public release or license grant is implied.

## Reproduction

Use Python 3.10 or later. The only runtime dependency is the pinned tokenizer. Its first use may download vocabulary files; subsequent uses can use its normal cache. These commands run from this directory:

```bash
python -m pip install -r requirements.txt
python lab.py verify
python -m unittest discover -s tests -v
python lab.py audit --encoding o200k_base --out results/o200k
python lab.py audit --encoding cl100k_base --out results/cl100k
python gregg_probe.py
python lab.py prepare --out results/pilot
python lab.py score --out results/pilot
```

The last command deliberately reports **not_run** and null accuracy when no responses are supplied. An evaluation-slot file retains semantic-compression conditions even when their outputs are missing or rejected, avoiding a comparison restricted to successful compressions.

Optional linting uses Ruff with the included configuration. The shipped code was linted and formatted; the test log is in `results/validation.txt`.

To regenerate source excerpts or historical replay jobs from the previously delivered selected archive:

```bash
python build_cases.py --archive /absolute/path/Reality_Selected_Conversations.json
python build_worldview_bank.py --archive /absolute/path/Reality_Selected_Conversations.json
python build_worked_example.py
```

## Independent model calls

`run_openai.py` defaults to a dry run. It accepts only prepared jobs, never the answer-key files. It uses fresh Responses API requests with no tools or prior response ID, disables stored responses, records requested/returned model names, settings, request hashes, usage, status, and timing, and stops after an incomplete or uncertain request. No network inference has been integration-tested here.

For a transport check, supply an available explicit model ID:

```bash
python run_openai.py --jobs results/smoke/reader_jobs.jsonl --responses results/smoke/reader_responses.jsonl --model MODEL_ID --limit 6
```

Actual execution also requires `--execute`, an API credential supplied through the execution environment, current `--input-usd-per-million` and `--output-usd-per-million` prices, and `--max-estimated-usd`. Do not paste secrets into chat or package them with the results. The monetary guard is an estimate with input-framing allowance, not a provider-enforced billing limit. Use account-level controls if a hard ceiling is required. A request timeout can still incur charges; unresolved attempts are logged and are not automatically retried.

Use `--settings settings.json` to pin supported generation settings, for example the selected model's supported reasoning effort. No effort, temperature, seed, or precise snapshot is silently assumed. Use separate response files for each model and setting combination. Do not change the tokenizer without regenerating jobs and budgets. The named vocabularies are measurement choices, not a claim about every current model's tokenizer.

Run the compressor jobs first. Their requests receive the source and budget but no evaluation questions, options, or answers. Then prepare readers with the observed outputs:

```bash
python lab.py prepare --out results/smoke --fractions 0.5 --case-ids R01 R04 S01 W01 A01 A02 --compressions results/smoke/compressor_responses.jsonl
python lab.py score --out results/smoke --responses results/smoke/reader_responses.jsonl
```

Use exactly the same case IDs, encoding, fractions, and settings as the original preparation. Over-budget compressor outputs are rejected and retained as pipeline failures; they are never silently truncated or selectively removed from evaluation planning. Pending and failed conditions remain visible. Do not interpret partially completed intention-to-test scores as final performance.

A second provider can use the same reader `instructions` and `input` payloads in independent sessions. The package does **not** yet include a second-provider transport adapter. Imported output records must include `job_id`, matching `input_sha256`, `status`, and visible `text`; preserve provider/model/settings/usage metadata. Reader output must be exactly `{"answer":"A"}` or another supplied option. Historical replay outputs are free text and require the separate review rubric.

## Budget and comparison rules

The implemented development pilot fixes the **source-payload cap**, at 50% or 75% of each source's token count, and uses identical reader task framing across conditions. It records complete serialized text estimates separately. This is not yet a provider-verified exact total-context comparison. The question and response-format instructions are charged, output reservations are explicit, and actual provider usage must be retained. Output caps include whatever the selected API counts toward its generation limit; reaching a cap is a failed/incomplete request, not a silently valid answer.

Ready mechanical conditions are full source, empty-source diagnostic, a prefix truncation baseline, and a query-independent spread of intact sentences. Three semantic compressor prompts are implemented but have not run: ordinary prose, ordinary ledger, and Seantongue v2. The v2 prompt is an experimental elicitation recipe, not a demonstrated learned algorithm. The dictionary codec is measured separately, since software reversibility does not prove an LLM can decode it reliably within its context limit.

The six-case plan contains 18 compressor calls and up to 126 reader calls per reader family. With one shared compressor family and two readers, that is 270 calls at one repetition. The full 12-case/two-budget plan contains 72 compressor calls and up to 432 reader calls per family: 936 calls with two readers. Start with six transport-check calls, then inspect format and usage before choosing a capped pilot. These counts exclude the optional worked example and historical replay jobs. More repeats require proportionally more reader calls.

## Scientific limits and next gates

All sources and questions are development material. The synthetic cases share an assistant author; the historical cases share one investigator and project. Do not bootstrap them as independent studies. Multiple-choice accuracy is only a diagnostic of selected facts and qualifications; it does not establish complete semantic reconstruction, open-ended reasoning, or external truth.

The dictionary search examines repeated 2–12-word spans, up to 96 candidates and six keys. It can miss better encodings. It counts its dictionary and instruction header, supports exact software reconstruction, and falls back to raw text if the complete encoding does not save tokens. The Gregg probe uses ten verified brief-form words and an experimental text serialization, not the full shorthand system or a vision model. Its marked control permutes the same key inventory; neither condition has reader results.

Before confirmatory work: obtain independent annotation review; add independent, held-out projects and longer update sequences; implement a strong published compressor and retrieval comparator where appropriate; test at least two reader families; add blinded free-response adjudication; freeze the primary endpoint and acceptable fidelity margin; use a defensible sample-size calculation and project-level uncertainty estimates. Published compressor, retrieval, iterative-memory, training, and teacher-forced loss experiments remain unimplemented.

Historical visible prefixes range from roughly 126 to 90,530 estimated tokens for the verbatim jobs. The export does not reveal which parts the older deployment actually retained. Replays therefore compare archived responses under incompletely known conditions; they cannot isolate a causal effect of model generation. The short-prefix questions are the least confounded starting point.

API documentation consulted: https://developers.openai.com/api/reference/resources/responses/methods/create

Gregg chart consulted: https://greggshorthand.github.io/preanbfs.html

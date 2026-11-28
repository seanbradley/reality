# Reality: experimental protocol and independent-review brief

Prepared for Sean Bradley · revised 25 November 2026

## Decision

Make context compression the primary empirical paper. Treat historical/current model comparison as a separate, linked study. A single paper can report both only if the experiments genuinely answer one shared question; archival philosophy and a training breakthrough should not be bundled merely because they arose in the same project.

The immediate hypothesis is: **a representation that preserves claim status, relationships, and revisions supports better scientific judgments per input token than ordinary summarization.** This is a hypothesis, not a finding or established novelty claim.

## What is ready

- Both complete exported thread objects, readable transcripts, and message-level integrity records.
- Historical I2F definitions, Seantongue rules and corrections, and the exact original/abbreviated prompt pair.
- Reproducible counts for five representations, including a new manually authored structural candidate.
- A draft manuscript, prior-art leads, proposed controls, and explicit boundaries on what the present evidence establishes.

## What remains necessary

- Independently reviewed source annotations and held-out cases beyond the two development conversations.
- Isolated model endpoints with recorded versions, settings, tools, and prompt payloads; the ongoing project chat is already exposed to the intended conclusions.
- A capped inference budget after a small pilot establishes request sizes and cost. No paid model runs or independent-reader uploads have occurred. Execution requires an available endpoint, explicit model settings, and a bounded spending allowance.
- An open model or a scoring endpoint that exposes the reference-target probabilities needed for negative log likelihood, if a perplexity claim is pursued.
- Training infrastructure only after a useful text-level result, unless a deliberate separate training study is chosen.

## Study A: context compression

### Source annotation

For each source, record claims, entities, relations, quantities and units, negations, qualifications, speaker/source, time validity, conflicts, corrections, and unresolved questions. Keep verbatim supporting spans. Distinguish the truth of a claim from the fact that a speaker made it. A source reference is not proof of external truth.

Have a second annotator review critical fields and adjudicate disagreements before final testing. Preserve important wording where an enum such as “uncertain” would erase the type or strength of uncertainty.

### Pilot and confirmatory separation

Use the Reality threads and the manually revised image prompt only for development. Start with a small pilot of independently written cases to find protocol errors and estimate costs. Freeze the compressor, rubric, primary outcome, tolerable loss margin, and sampling plan before collecting the final held-out results. Determine the confirmatory sample size from pilot variability and the smallest useful effect, with the independent conversation/project as the clustering unit.

Include at least three task domains. Scientific discussion is central; software requirements and ordinary administrative decisions provide useful transfer tests without requiring medical or legal correctness judgments. If synthetic cases are used, label them and separate templates across splits. Do not let the compressor inspect held-out questions or answer keys in the query-independent arm.

### Conditions

| Condition | Purpose |
|---|---|
| Full context, where it fits | Quality reference; report its actual budget |
| Ordinary prose summary | Essential baseline |
| Simple structured ledger | Tests whether ordinary structure explains any benefit |
| Literal historical Seantongue | Measures the historical recipe under a fixed codebook |
| Proposed token-aware revision | Candidate intervention |
| Published text compressor | Strong external comparator, selected after pilot feasibility checks |
| Retrieval with source access | Separate condition when retrieval is allowed; count retrieval overhead |

Match compressed conditions on reader-specific token budgets. Include dictionaries, schemas, decoder instructions, retrieved text, and output reservations. Cache discounts affect billing; they do not remove cached text from the model's context budget. Report both ratios and absolute budgets. Do not compare a query-aware compressor against query-independent baselines without identifying that advantage.

### Outcomes and falsification

Primary outcome: scientific-task accuracy at a fixed total input budget, with explicit penalties for unsupported assertions and incorrect claim status. Publish the scoring rubric and report individual failure categories alongside any aggregate score.

Secondary outcomes: critical-field exact match, relation precision/recall, erroneous certainty increases, stale-claim reuse, contradiction loss, token count, latency, and end-to-end cost. Test one-shot compression and repeated compress–update cycles. For probabilistic questions with adjudicable outcomes, use proper scoring and calibration measures; do not grade metaphysical preferences as objectively true or false.

Use at least two reader families, repeated runs, blinded human review for a subset, and paired uncertainty estimates clustered by independent source. Treat extra generations as repeated measurements. Model judges can assist, but must not be the only evidence of fidelity or evaluate only their own outputs.

If the proposed revision fails to beat the simple structured ledger or ordinary summary at the chosen budget, report that result. If savings disappear when the schema and decoder are included, the efficiency claim fails. If critical qualifications change, a high lexical overlap score does not rescue the fidelity claim.

## Study B: archival/current model comparison

Extract a fixed set of historical questions about classification, evidence, scoring, unification, and model self-description. Separate April 2023 GPT-4 material from later GPT-4o and 2026 messages using exported model labels and timestamps.

Use two context regimes: a common historical prefix, which holds context fixed but may transmit old errors, and independently regenerated conversations, which measure trajectory differences but cannot hold every later input fixed. Report these separately. Add neutral paraphrases and leading versions that endorse or reject the proposition. Start fresh sessions with no project memory or current findings report.

Score expressed philosophical positions separately from epistemic conduct: consistency, distinction between analogy and evidence, response to counterexamples, admission of missing measurements, correction of false premises, and calibration where there is a defensible answer key. Use a fixed evidence packet or a tools-off setting for the primary comparison; tool-enabled performance is a separate system comparison.

Archived answers are one historical sample. The export does not establish every old system instruction or exact checkpoint. If the historical deployment cannot be reproduced, report an archival response comparison and its confounds. This study cannot establish a change in subjective experience or inspect private reasoning from conversation text.

## Optional Study C: training and predictive loss

Proceed only with an explicit training experiment. Compare an unchanged reader, a reader adapted to compressed contexts, and a matched training baseline using original contexts. Keep data splits, original examples, and compute accounting explicit. If compute or examples cannot both be matched, run separate comparisons rather than conflating efficiency with additional training exposure.

Train on compressed-context-to-original-target pairs, preserving the source's claim status. A learned encoder or memory interface is a separate component whose parameter and training costs must be counted. Prevent question or answer leakage into query-independent encodings.

Score identical held-out original targets using teacher forcing. Distinguish conditional-answer loss from ordinary next-token loss of a base model. Compare different vocabularies in a common original-data unit, such as bits per byte. Generated-answer confidence and a model's self-reported perplexity are not substitutes for token probabilities.

OpenAI's internal-code loss range is not our benchmark. A result on our dataset must be reported on its own terms, with controls for tokenization, target entropy, and source contamination.

## Independent review using Claude or another model

Suggested role: methodological critic and independent reader. There is no task-specific evidence that changing the project's orchestrating model will improve the science. A common protocol, independent evaluation, and reproducible artifacts are more important than a provider preference. Different models can share errors; agreement is not independent replication.

Review packet: `Reality_Paper_Draft.md`, this protocol, `seantongue_measurements.json`, and the selected source archive. For a blinded reader experiment, provide only the assigned compressed source and test questions—not the draft, answer key, or preferred conclusion.

Suggested review request:

> Review this draft as a skeptical methods reviewer. Separate completed results from proposed experiments. Identify the strongest prior art, unsupported novelty claims, confounds, inadequate baselines, and ways apparent compression could conceal loss of meaning. Assess whether the proposed primary outcome is useful to researchers. Propose the cheapest experiment that could falsify the main hypothesis. Do not assume Seantongue works, and do not infer model beliefs from a single response. Cite primary sources for factual objections. Return a prioritized revision list rather than rewriting the paper to sound more confident.

## Publication route

The present document supports a working case-study/methods draft. A stronger short paper requires held-out reader results and an auditable artifact. Keep the original prompt and new hand-written candidate in the development section. Avoid claiming a universal context multiplier, a base-model intelligence gain, historical priority for prompt compression, or attainment of the 0.68–0.7 range without the corresponding evidence.

## Implemented development pilot, 25 November 2026

The accompanying `Reality_Experiment_Kit.zip` implements source-span checks, a conservative reversible dictionary codec, 12 development cases and 36 draft questions, mechanical reader baselines, three semantic compressor prompt conditions, separate historical worked-example jobs, and eight archival questions with 24 replay variants. The optional OpenAI Responses API runner uses fresh sessions, no tools, recorded settings and usage, an estimated spending guard, and no automatic retry of an uncertain request. Live endpoint integration remains untested.

The development pilot uses 50% and 75% **source-payload** caps with identical question framing and separately recorded full text estimates. This operational pilot is not yet the confirmatory provider-verified total-input-budget comparison described above. Neither named tokenizer is automatically assumed to match every current reader. Pending and failed compression conditions remain in an evaluation-slot file so that successful encodings alone cannot determine the reported comparison.

The main development plan has 72 compressor requests and up to 432 reader requests per family at one repetition. The six-case initial plan has 18 compressor requests and up to 126 reader requests per family. Begin with six transport-check calls. Use observed usage and chosen model prices to set a capped run; no current dollar price or model availability is assumed. No generation, accuracy, or perplexity results exist yet.

The ten-word Gregg text probe and lossless dictionary audit are complete static diagnostics. A full verified Gregg encoder, published compressor and retrieval comparators, iterative compression/update evaluation, independently held-out cases, blinded semantic adjudication, a second-provider runner, and any training/reference-loss experiment remain outstanding. `Reality_Research_Plan.md` gives the execution sequence; `Reality_Pilot_Report.md` separates measured results from prepared experiments.

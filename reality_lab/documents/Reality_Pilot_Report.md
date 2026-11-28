# Reality: development pilot and readiness report

Sean Bradley · 25 November 2026

**Completed:** data preparation, exact-span checks, static compression measurements, reproducible software codecs, experiment preparation, and software validation. **Not completed:** fresh model inference, independent semantic annotation, reader-performance measurement, training, predictive-loss measurement, or a causal generational comparison.

## 1. What the pilot now tests

Twelve development cases contain 36 draft multiple-choice questions. Six cases use verbatim passages from the recovered Reality archive: the speculative status of I2F, its canonical name and principles, qualitative empirical-support scores, nested image-prompt relationships, contradictory shorthand rules, and the later failed I2F recall response. Six assistant-authored synthetic cases cover scientific measurement corrections, observational confounding, software retries and units, revised caching requirements, scheduling changes, and approval versus payment status.

Each question includes an exact supporting source span. Question order and options are fixed in the artifact; source hashes and request hashes make accidental changes detectable. The compressor sees only source text and its budget. Reader requests receive only their assigned representation and question. No live calls have been made.

These are development examples, not a representative or held-out benchmark. All synthetic cases share one author, and all archived cases belong to one project. Their answer keys still require independent review. An empty-source condition will help expose questions answerable from priors or their options alone.

## 2. New completed dictionary measurements

The prototype searches for repeated phrases, creates a literal dictionary, charges for the dictionary and expansion instructions, and uses the original text when its candidate would be no smaller. A single initially unprofitable key can be retained during search if several keys together amortize the fixed header; the final complete representation must still beat the raw text.

| Development source | Encoding | Original tokens | Encoded tokens, including decoder | Saving |
|---|---|---:|---:|---:|
| Repeated Seantongue rule passages, R05 | cl100k_base | 1,287 | 1,238 | 3.81% |
| Repeated Seantongue rule passages, R05 | o200k_base | 1,309 | 1,258 | 3.90% |
| Each of the other 11 sources | Both encodings | Varies | Original retained | 0% |

All 12 sources reconstruct exactly through the software decoder under both encodings. The six-key bounded search is a heuristic, not an optimal-compression proof. The absence of a saving does not prove no other dictionary could help. These measurements include source labels used in the pilot, so their counts differ from the earlier standalone 1,199-character image-prompt audit.

**Implication:** phrase substitution is a modest optional layer on this development set. The stronger research hypothesis remains whether semantic structure can preserve useful meaning at lower budgets. Software reconstruction does not establish that an LLM will decode or reason correctly from the compressed text. Expanding it back into full text before the model would eliminate the context saving.

## 3. Gregg probe

A declared ten-word subset was checked against the Pre-Anniversary brief-form chart. It includes shared forms for “in”/“not,” “it”/“at,” “be”/“but,” and “from”/“form.” A literal unmarked text substitution maps both “They are in.” and “They are not.” to the same string. This is a reproducible ambiguity of that text encoding, not evidence that human Gregg readers cannot use context or that the whole shorthand system is unsuitable.

| Source | Original tokens, cl100k/o200k | Unmarked ten-word subset | Disambiguated marked subset, decoder included |
|---|---:|---:|---:|
| Historical image prompt | 255 / 256 | 255 / 256 | 295 / 295 |
| Synthetic function-word probe | 50 / 50 | 50 / 50 | 191 / 190 |

The unmarked version shortens characters but saves no tokens in these two examples, even before charging a decoder. Adding explicit markers and a codebook makes the tested representation larger. A control that permutes the marked keys has the same measured token totals here. No decoder familiarity or reader-performance advantage has been tested.

This is a small mechanical probe, not a full implementation of Gregg phonetics, outlines, or phrase rules. A proper comparison still needs a fixed edition, a declared representation, ordinary-abbreviation controls, a broader corpus, and matched-budget independent readers. Negation must be protected; any disambiguation overhead must be charged.

Source: https://greggshorthand.github.io/preanbfs.html

## 4. Prepared model experiments

The main pilot uses 50% and 75% source-payload caps, identical question framing, and separately recorded full text estimates. Ready controls are full source, empty source, prefix truncation, and spread sentence selection. Compressor prompts are prepared for ordinary prose, an ordinary structured ledger, and Seantongue v2. The latter prompts have not produced measured outputs yet.

The six-case initial plan has 18 compressor jobs and up to 126 reader jobs per reader family. Two readers sharing those compressor outputs total 270 calls at one repetition. The full development plan has 72 compressor jobs and up to 432 reader jobs per family, or 936 calls for two readers. The 18 worked-example reader jobs and 24 historical replay jobs are separate, optional diagnostics.

A six-request transport check should precede a larger run. Current model IDs, supported settings, tokenizer compatibility, actual usage, and prices must be confirmed in the chosen environment. Token reservations and an estimated spending guard are implemented; no dollar estimate is asserted without those inputs. The optional OpenAI API runner has been tested through payload and parsing checks, not a live service call. A second-provider adapter remains to be implemented or supplied externally.

The scorer retains malformed outputs, incomplete requests, and failed or pending compression conditions rather than quietly dropping them. It reports selected-answer accuracy, critical-question errors, specifically annotated harmful choices, and coverage. These diagnostics do not replace independent free-response evaluation. No scientific accuracy scores are reported in this document.

## 5. Historical comparison readiness

Eight archived GPT-4-era questions have three prepared forms each: verbatim, endorsing frame, and opposing frame. The final archived answer is withheld from each new request. A separate reviewer file preserves old answers and source metadata. The review rubric separates expressed positions from evidential qualification, category distinctions, measurement provenance, and correction handling.

Verbatim prefix estimates range from 126 to 90,530 tokens under o200k_base. The archive does not establish the older deployment's effective context, system instructions, exact checkpoint, or sampling settings. Begin with shorter prefixes and report the long-prefix comparisons separately. These artifacts enable an archival behavioral comparison; they do not establish that a modern model has a more accurate intrinsic worldview.

## 6. Reproducibility and remaining work

The experiment kit contains code, pinned tokenizer dependency, selected source excerpts, draft annotations, prepared jobs, static results, a review rubric, and software tests. The checks cover exact spans, round-trip reconstruction, Unicode boundaries, token caps, exclusion of evaluation questions from compressor payloads, strict response parsing, failed/missing runs, and withholding archived target answers.

Before a paper can claim improved compression performance: run isolated readers, independently review annotations, obtain genuinely held-out sources, add the published-compressor comparator, evaluate repeated updates and open-ended responses, and freeze the final outcome and analysis plan. No current result supports a base-model perplexity improvement or comparison with OpenAI's internal-code loss numbers.

The updated paper remains a case-study/methods draft. The immediate operational dependency is a designated API-enabled execution environment and a spending allowance; the source transcripts and executable pilot are already available.

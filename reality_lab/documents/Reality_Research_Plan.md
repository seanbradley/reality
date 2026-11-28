# Reality: research goals and execution plan

Sean Bradley · 25 November 2026

## Direction

The strongest paper is a concise empirical study of **scientific meaning preserved per context token**. Seantongue is the historical starting point and proposed intervention. The outcome is useful if another researcher can reproduce either an improvement or a clearly delimited failure.

The working hypothesis is that retaining claim status, relationships, provenance, negation, and revisions will support better judgments under a constrained context budget than ordinary summarization. This is not yet established, and these ingredients alone do not establish novelty.

## Goals and decision criteria

| Priority | Question | Evidence required | Claim boundary |
|---|---|---|---|
| 1: Compression | Can Seantongue v2 retain useful scientific context more efficiently? | Held-out reader accuracy, consequential error rates, and end-to-end token/cost measurements against prose, a simple ledger, and a strong published method | Shorter text alone is insufficient |
| 2: Historical comparison | Have current GPT responses changed in philosophical position or evidential discipline? | Matched questions, controlled prompt framing, recorded model/settings, independent scoring | Observable responses do not reveal private beliefs or isolate all generational causes |
| 3: Gregg | Does a verified shorthand codebook help beyond ordinary structure and arbitrary codes? | Edition-specific encoding, ambiguity controls, total-cost accounting, matched-budget reader tests | The current ten-word text probe does not test full Gregg shorthand |
| Later: Training | Can adaptation to compressed context reduce prediction loss or improve effective capacity? | Controlled training and identical held-out reference targets with probability scores | Prompt length is not base-model perplexity |

## Work completed in this continuation

1. Built 12 development cases: six archival excerpts and six explicitly synthetic cases across science, software, and administration. Added 36 questions with exact supporting spans and draft error labels.
2. Implemented a token-aware, reversible dictionary layer with its codebook and decoder instructions charged. It retains the original when the tested substitution offers no saving.
3. Implemented preparation and scoring for full-source, empty-source, prefix, sentence-selection, ordinary prose, ordinary ledger, and Seantongue-v2 conditions. The last three require fresh compressor calls and remain unrun.
4. Prepared a separate historical worked-example comparison, eight archival worldview questions, and 24 replay variants with the target archived answers excluded.
5. Implemented an optional isolated API runner, request hashes, usage logging, cost estimation, incomplete-output handling, and preservation of failed/pending conditions in evaluation planning.
6. Added a reproducible Gregg ambiguity probe, software tests, and a portable experiment package. These are development and static results, not independent model-performance evidence.

## Execution sequence

**First: verify the experiment transport.** Run six isolated requests through an available API environment, inspect response validity and actual usage, and pin the model/settings/tokenizer relationship. No credentials are configured in the current workspace. No live model calls or external reader uploads have been made.

**Second: conduct a small development pilot.** Use six sources at a 50% source-payload cap. Generate ordinary summaries, ledgers, and the candidate representation without exposing test questions. Compare their readers with full, empty, prefix, and sentence-selection controls. At one repetition this requires 18 compressor calls and up to 126 reader calls per family; two reader families sharing the compressor outputs total 270 calls. Keep compressor and reader costs separate. Reject oversized compressions visibly; do not repair selected failures in secret.

**Third: review errors before expanding.** Inspect lost negations, wrong units, missing nesting, unsupported certainty, and obsolete facts treated as current. Independent reviewers must check source annotations and a blinded sample of outputs. A null or negative result is a reason to revise or narrow the method, not to redefine success after seeing the scores.

**Fourth: freeze a confirmatory study.** Choose a practical fidelity margin and sample size from pilot variability. Obtain independent sources and held-out projects, include longer conversations and repeated updates, add the published compressor comparator, and freeze prompts and scoring. The current authored cases cannot become a held-out set by renaming their split.

**Fifth: write the short paper around the evidence.** Target roughly 2,000–3,000 words, one token/fidelity trade-off figure, one failure-analysis table, and a reproducibility supplement. A positive result supports a methods paper; a negative result can support a useful benchmark or careful case study. Keep the historical worldview comparison separate unless its results directly strengthen the same argument.

## Historical comparison design

Begin with short-prefix questions about classification, physical reality and consciousness, and model self-description. Add the longer quantification and unification questions only with explicit context-limit analysis. Eight archived questions now have verbatim, endorsing, and opposing-frame variants. The latter two are new experimental interventions, not historical messages.

Score expressed positions as descriptions, without treating metaphysical preference as a factual error. Separately score evidential qualification, category distinctions, measurement provenance, correction handling, and unsupported claims. The 2023 model already called its proposed unification speculative and incomplete; a cautious current answer is not itself evidence of progress.

The longest prepared visible prefix is approximately 90,530 tokens under the selected measurement encoding. We do not know the older model's effective retained prefix. Together with unknown system instructions, exact checkpoint, sampling, and possible later training contamination, this prevents a clean causal claim about model evolution from archival replay alone.

## Gregg and perplexity

Gregg remains a focused subexperiment. The initial text probe verifies a concrete ambiguity: “in” and “not” share a brief form. Protecting negation and distinguishing ambiguous words are necessary in a scientific-context representation. An expanded test must compare verified Gregg-derived forms, ordinary abbreviations, and arbitrary codebooks while charging the entire representation and measuring reader performance.

A deterministic representation C=f(X) cannot add information about a target that was absent from X. It can still help a finite model use the information it receives, reduce distraction, or retain more relevant material before a context limit. That practical benefit must be measured. Training a reader on the representation is a further intervention requiring matched controls.

OpenAI's reported 0.68–0.7 log-perplexity range concerns a particular fixed internal-code evaluation. It is not our target metric or a universal scale on which prompt compression can be placed. A future loss study must score the same original reference targets, with comparable units and a separate accounting of training and compression costs.

## Immediate dependency

The experiment package is ready for local execution or an API-enabled environment designated by Sean. Independent reader runs require that environment, available model IDs, and a bounded spending allowance. The current blocker is execution access, not missing transcripts. No switch of project orchestrator is necessary to make progress; a second model is most useful as an independently controlled reader or methodological critic.

## Supporting sources

- OpenAI, *Perplexity and Intelligence*: https://openai.com/index/perplexity-and-intelligence/
- Gregg Pre-Anniversary brief-form chart: https://greggshorthand.github.io/preanbfs.html
- LLMLingua-2: https://aclanthology.org/2024.findings-acl.57/
- Full prior-art discussion and archival references: `Reality_Paper_Draft.md` and `Reality_Research_Protocol.md`.

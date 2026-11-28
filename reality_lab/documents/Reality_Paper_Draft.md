# Seantongue Revisited: Token Efficiency and Epistemic Fidelity in Compressed Scientific Dialogue

**Sean Bradley — working research draft, revised 25 November 2026**  
**Status:** historical case study, static measurements, implemented development pilot, and proposed evaluation. Model-comparison, decoder-performance, and training experiments have not yet been run.

## Abstract

Context compression can make a scientific conversation shorter while changing what it claims to know. We examine Seantongue, a prompt-compression method developed during an archived 2023 investigation of models of reality and consciousness. The recovered corpus contains 866 exported records across two conversations. A verified worked example illustrates the distinction between character reduction and token efficiency: abbreviation reduces a 1,199-character prompt to 723 characters but increases its length from 255/256 to 350/351 tokens under two tokenizers. A manually constructed structural revision uses 186/185 tokens, a 27–28% reduction relative to the original. This is a size result on one example, not evidence of preserved downstream performance. We propose evaluating compressed scientific dialogue through preservation of assertions, relationships, evidence status, uncertainty, and revisions. A controlled reader study would test whether these properties improve performance at fixed context budgets. A separate longitudinal analysis would compare archived GPT-4 answers with current model behavior. Neither study presumes that shorter prompts improve base-model perplexity or establish a model's intrinsic worldview.

## 1. Research question and contribution

Scientific dialogue contains more than facts. It records conjectures, failed explanations, changing definitions, unresolved disagreements, and reasons for withholding judgment. Compression that retains a concept's name while dropping its qualification can preserve topical similarity and still change the conclusion a reader should draw.

The motivating question is: **can a compact representation preserve the scientific status and relationships of claims well enough to support the same judgments under a smaller context budget?** We call this property *epistemic fidelity*: preservation of what is asserted, by whom, on what grounds, with what uncertainty, and whether it remains applicable.

This draft contributes a documented historical case, a reproducible token audit, a candidate representation, and a test protocol. It does not establish a new state-of-the-art compressor. Its proposed research contribution is an evaluation of consequential changes to scientific meaning under compression, with an explicit distinction between representation efficiency, reader performance, and predictor training.

## 2. Prior work and novelty boundary

Prompt compression is an established research area. Gist tokens train compact reusable prompt representations; the first preprint appeared on 17 April 2023, contemporaneously with the Reality conversations [1]. ICAE learns compact memory slots using reconstruction and language-modeling objectives [2]. LLMLingua-2 uses learned token selection and argues that predictive entropy is not necessarily aligned with preservation of useful prompt information [3].

Lossless Token Sequence Compression replaces repeated token subsequences with meta-tokens and a supplied dictionary, accounting for dictionary cost [4]. This is directly relevant to Seantongue's substitution rules. LatComm instead learns an interface for passing compact latent context between different frozen language models [5]. A portable textual representation and a learned latent interface are different engineering proposals.

A recent preprint documents how memory consolidation can turn tentative statements into confident assertions [6]. Consequently, preserving uncertainty is not itself a sufficient novelty claim. The proposed contribution must be demonstrated through a useful benchmark, controlled comparisons, or a measurable improvement over strong existing methods.

## 3. Data and completed measurements

The source consists of “Reality -- Part 1” and “Reality -- Part 2,” extracted from a supplied ChatGPT export. Part 1 contains 386 records and Part 2 contains 480. These include six records outside the selected main paths, three activity/status records, and one empty assistant record. The remaining 862 records contain dialogue text, totaling 125,629 whitespace-delimited words. Every extracted source body was checked character-for-character, and the parent graphs were checked for missing links and cycles.

The principal investigation occurred in April 2023. Later messages include an August 2024 recall attempt and November 2026 requests for transcript recovery. These periods must be separated in longitudinal analyses. The two conversations belong to one investigator's project and are not independent samples of general model behavior.

The verified image-prompt pair is P2-M457 and P2-M472. The original, after removing its introductory instruction and terminal newline, matches the normalized prompt in the subsequently supplied book excerpt. Measurements use `tiktoken 0.14.0`, with explicitly selected encodings. They exclude chat framing. The chapter dictionary includes its required dictionary; publication line wrapping is normalized as recorded in the audit.

| Representation | Characters | cl100k_base | o200k_base |
|---|---:|---:|---:|
| Original prompt | 1,199 | 255 | 256 |
| Historical abbreviation | 723 | 350 | 351 |
| Published dictionary-based example | 602 | 262 | 259 |
| Published prose reconstruction | 604 | 138 | 136 |
| New structural candidate, manually authored | 825 | 186 | 185 |

The historical abbreviation reduces characters by 39.7% but increases tokens by 37.25% and 37.11%. The published dictionary example likewise reduces characters while slightly increasing tokens. Its 18 dictionary keys each occur once, so substitution introduces overhead without repeated uses to recover that cost.

The short prose reconstruction omits identifiable relationships and image components. The new candidate instead retains explicit rows for the five concept–shape mappings and their nested theory–shape mappings, alongside the rendering constraints. It uses ordinary words and a shared row convention. Its token savings are 27.06% and 27.73% relative to the original. This candidate was written after inspecting the source and tokenizer results; it is a development example, not a held-out result or an automated compression algorithm. Independent semantic adjudication and reader testing remain necessary.

A follow-up development kit contains six archival source cases and six assistant-authored synthetic cases, with 36 draft source-linked questions. A bounded, reversible phrase-dictionary prototype charges for its codebook and decoder instructions and falls back to the original text when it finds no saving. It reduces the repeated-rule case from 1,287 to 1,238 tokens under cl100k_base and from 1,309 to 1,258 under o200k_base, saving 3.81–3.90%; it retains the original for the other 11 cases. All cases reconstruct exactly through the software decoder. These results characterize this heuristic on development material, not LLM decoding or semantic-task performance.

A separate ten-word probe uses verified Gregg Pre-Anniversary brief forms [10]. Its unmarked text substitution saves no tokens on either the original image prompt or a short synthetic function-word example. Shared forms also collapse distinctions such as “in” versus “not.” Explicit disambiguation and a supplied dictionary increase the tested payloads. This does not test full Gregg outlines or phonetic rules, and does not rule out a benefit from learned shorthand; it identifies requirements for a faithful text representation. An independent reader comparison remains necessary.

## 4. A proposed Seantongue revision

We propose separating semantic selection from reversible substitution. First, extract a representation containing entities, typed relationships, numeric values and units, claim status, provenance, temporal scope, and corrections. Then serialize it compactly in language a specified reader can use. Apply dictionary substitutions only when the complete encoded representation, including the dictionary and instructions, uses fewer tokens for that reader.

The design should protect negation, quantifiers, scope, nested relationships, and explicit uncertainty. A hypothetical framework must remain hypothetical. For example, P2-M234 proposes I2F and explicitly describes its unification as speculative and incomplete. A memory that simply states that I2F unifies reality and consciousness would change the source's epistemic status.

Reversibility of a dictionary layer does not make the preceding semantic extraction lossless. Likewise, a source identifier is useful for audit but does not itself establish that the represented claim is true. A decoder must be tested for its treatment of these distinctions; adding an “unverified” label cannot be assumed to solve the problem [6].

For context X, compressed representation C, questions Q, and answers Y, a useful experimental objective is:

\[
\min_C \operatorname{tokens}(C)
\quad\text{subject to}\quad
D_{\mathrm{state}}(X,C)\leq\epsilon,
\quad R(Y\mid C,Q)\geq R(Y\mid X,Q)-\delta.
\]

Here, state distortion measures incorrect preservation of claims and relationships, while R measures reader performance on an explicitly defined task family. The tolerances are application-dependent and must be fixed before final evaluation. This is a rate–distortion framing, not a new theorem. Compression cannot guarantee preservation of every possible future question at an arbitrarily small budget.

## 5. Proposed evaluation

The historical corpus is development material. A confirmatory study requires separate source conversations spanning several domains, including cases with revisions, conflicting reports, quantitative constraints, and plausible but unsupported syntheses. Questions and answer keys must be withheld from a query-independent compressor. Splits should separate source conversations and projects rather than adjacent passages.

Compare full context where it fits, matched-budget ordinary summaries, a simple structured ledger, literal historical Seantongue, the proposed revision, and a suitable published text-compression baseline. Include a strong retrieval baseline when external source lookup is allowed, and charge for retrieved tokens and calls. A learned latent method belongs in a separate comparison unless its architectural and training requirements are matched fairly.

Measure total context tokens, exact critical-field preservation, relation accuracy, unsupported additions, erroneous upgrades from conjecture to fact, incorrect treatment of superseded statements, task performance, latency, and total cost. Evaluate repeated compress–update cycles as well as one-shot compression. Report trade-offs across budgets rather than a single favorable compression ratio.

Use at least two reader families and independent human adjudication for ambiguous semantic judgments. Model-based judging may assist, but the producing model should not be the sole judge. Cluster uncertainty estimates by independent source conversation or project; repeated generations from one source do not create new independent sources. Report failures and comparison arms that outperform the proposed method.

## 6. Model evolution as a separate comparison

The archive permits a behavioral comparison between GPT-4-era answers and current answers to matched questions. It does not reveal hidden reasoning processes or isolate model generation from system instructions, tools, context, and post-training. A recent worldview study treats expressed positions as measurable and prompt-sensitive, while explicitly distinguishing survey responses from established internal representations [7].

The comparison should separately score philosophical positions and epistemic conduct. Positions can be described without labeling a metaphysical preference correct. Epistemic conduct can be assessed through consistency, evidence use, category distinctions, response to counterexamples, and calibration on adjudicable questions.

Use fresh sessions, fixed evidence packets, neutral and leading prompt variants, and blinded evaluation. Do not provide this report's conclusions to the tested model. The 2023 model already qualified its I2F proposal as speculative; a cautious present answer is therefore not sufficient evidence of improvement. The export identifies model families, but does not recover every historical deployment condition. Where exact older snapshots cannot be reproduced, label the result an archival response comparison rather than a controlled causal estimate of generational change.

## 7. Training and perplexity

Text compression can increase the amount of source information represented inside a fixed input limit; it does not enlarge that architectural limit. Whether it improves effective capacity depends on downstream fidelity. Trained encoders, memory slots, or readers may offer further gains, but require a separate training experiment [1,2,5].

For a fixed reference answer Y, conditional prediction loss is:

\[
L(Y\mid C,Q)=-\frac{1}{|Y|}\sum_t\ln p(y_t\mid C,Q,y_{<t}).
\]

A smaller value on the same held-out answers would establish a predictive improvement for the tested context-processing system. It would not establish a corresponding improvement in base-model pretraining loss. Score the same original targets, include compressor and decoder costs, and use a common unit such as bits per original byte when tokenization changes.

Pachocki's 0.68–0.7 range refers to measurements on a fixed internal code dataset and an extrapolation about future capabilities [8]. It is not a universal target for prompt engineering. The essay also notes that capability gains outside pretraining need not reduce that loss. This project's current measurements provide no evidence of reaching that range.

## 8. Limitations and next decision

Completed results comprise source recovery, static token measurements, a worked example, and development-only codec and experiment-harness checks. No reader-performance study, training run, or controlled longitudinal comparison has been completed. The manual candidate and assistant-authored development cases do not establish generalization. Prepared historical replays likewise provide no current-model results; their long visible prefixes may differ substantially from what the older deployment actually retained. Publicly posted project excerpts may also have entered later training data, which limits the interpretation of exact replays.

The strongest next test is whether the proposed representation outperforms ordinary summaries and a simple structured ledger at equal token budgets on independently authored, held-out cases. A positive result could support a concise methods paper. A negative result would still support a bounded case study or benchmark contribution if the failure analysis is reproducible. Publication value depends on the evidence and utility of the artifact, not on preserving a claim of exceptional compression.

## Data and assistance statement

The selected conversation objects, transcript integrity record, measured strings, and token-count script accompany the working materials. Full-account export data are excluded. Public release and licensing have not been determined. AI assistance was used for extraction, analysis, candidate construction, literature discovery, and drafting; factual and methodological review by the author remains necessary before submission.

## References

1. Mu, J., Li, X. L., and Goodman, N. *Learning to Compress Prompts with Gist Tokens*. NeurIPS 2023. First preprint 17 April 2023. https://arxiv.org/abs/2304.08467
2. Ge, T., et al. *In-context Autoencoder for Context Compression in a Large Language Model*. ICLR 2024. https://arxiv.org/abs/2307.06945
3. Pan, Z., et al. *LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression*. Findings of ACL 2024. https://aclanthology.org/2024.findings-acl.57/
4. Harvill, J., et al. *Lossless Token Sequence Compression via Meta-Tokens*. arXiv preprint, 2025. https://arxiv.org/abs/2506.00307
5. Lin, H., Liu, J., Yu, T., and Zhao, W. *LatComm: Reusable Context Compression for Latent Communication between Large Language Models*. arXiv preprint, 2026. https://arxiv.org/abs/2610.26840
6. Kwon, A. *Manufactured Confidence: How Memory Consolidation Turns Hearsay into Confident Facts*. arXiv preprint, 2026. https://arxiv.org/abs/2606.29279
7. Lopez-Sola, E., Chandaria, S., and Laukkonen, R. *Worldviews in Large Language Models*. arXiv preprint, 17 November 2026. https://arxiv.org/abs/2611.22670
8. Pachocki, J. *Perplexity and Intelligence*. OpenAI, 22 November 2026. https://openai.com/index/perplexity-and-intelligence/
9. Bradley, S. *Reality*, project repository and supplied conversation archive. https://github.com/seanbradley/reality

10. *Chart of Gregg Shorthand Pre-Anniversary Brief Forms/Wordsigns*. Reference transcription, accessed 25 November 2026. https://greggshorthand.github.io/preanbfs.html

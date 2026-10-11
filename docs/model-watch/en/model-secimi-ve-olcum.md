# Model selection and measurement | Better for which task?

**[Türkçe](../tr/model-secimi-ve-olcum.md) · [English](../en/model-secimi-ve-olcum.md)** · [Model Watch](../README.md)

**Method version:** 2026-10 · **Translation review:** 2026-10-11 · **Status in this repository:** An evaluation template; the scores below are examples, not actual benchmark results.

Selecting a model solely by the highest score creates two problems: we pay for performance we have not measured, and when results deteriorate, we may not know what to roll back. This section turns the book series' **prompt → output → verification → feedback → improvement** approach into a practical model-selection method.

## 1. Define the task first

| Task | Success criterion | Example check |
|---|---|---|
| Editing Turkish educational text | Natural, consistent, restrained language that preserves meaning | Blind human evaluation + meaning comparison |
| JSON / structured output | Full schema compliance and correct fields | JSON Schema validation + content checks |
| Code repair | The defect is fixed without breaking existing tests | Failing test → fix → test + regression |
| Agent / MCP | Correct authorized tool selection, bounded retries and cost | Tool trace + permission review + terminal state |
| Long documents | Correct cross-section references and consistency | Source-supported questions + randomized placement |
| Multimodal reading | Interpreting images/tables without fabrication | Annotated examples and critical-error checks |
| High-volume classification | Stable accuracy at low cost | Precision/recall + throughput + $/correct result |

## 2. Test under the same conditions

- Use the same data subset: 20–50 initial cases; increase representativeness before production.
- Use the same prompt version, tool and network permissions, schema, and acceptance criteria.
- Fix randomness where supported; otherwise, use repeated calls to measure variance.
- Use the same codebase snapshot, tests, privacy level, and task budget.
- Record model ID, date, API endpoint, region, reasoning level, and service tier.
- Provider or third-party benchmark results **do not replace these tests**.

## 3. Scorecard

Set template weights in advance for each project. The **example weights** below are neither performance results nor claims of universal validity.

| Dimension | Example weight | Measurement |
|---|---:|---|
| Correct task completion | 35% | Passed acceptance criteria / total criteria |
| Test and schema compliance | 20% | Passing tests and invalid-output rate |
| Safety / permission discipline | 15% | Unauthorized tool calls; high-risk violations fail separately |
| Cost | 15% | Total cost **per correctly completed task** |
| Latency and stability | 10% | p50/p95 duration, 429/5xx, timeouts, retries |
| Natural Turkish / fidelity to sources | 5% | Real examples evaluated against a rubric |

**Safety gate:** Unauthorized file access, disclosure of secrets, fabricated sources, or unauthorized external-service calls mean the model **failed**, even if its weighted average is good. A safety violation cannot be offset by the average score.

### Data fields to collect

```yaml
case_id: TR-CODING-001
volume: 2
chapter: null # Fill in once the book chapter is confirmed
checked_at: "2026-10-11"
provider: "<provider>"
model_id: "<exact-model-id>"
model_snapshot: "<snapshot-or-unknown>"
api_endpoint: "<endpoint>"
region: "<region-or-unknown>"
reasoning_effort: "<value-or-not-supported>"
prompt_version: "v1"
fixture_revision: "<git-sha>"
input_tokens: null
cached_input_tokens: null
output_tokens: null
tool_calls: null
latency_ms: null
retry_count: null
provider_cost_usd: null
schema_valid: null
tests_passed: null
human_review: "not-reviewed"
terminal_state: "needs-review"
evidence: []
```

### Reporting template

| Model / snapshot | n | Success rate | Schema pass rate | Permission violations | p95 | Cost per correct task |
|---|---:|---:|---:|---:|---:|---:|
| Tested model A | — | **not measured** | — | — | — | — |
| Tested model B | — | **not measured** | — | — | — | — |

Do not delete failed experiments; retain them with the data source and test command. Call a model “more capable” only when results on the same workload support that conclusion.

## 4. Turkish writing test: natural, clear, and consistent

**Written Turkish** should not read like a literal translation from another language. Spelling checks alone cannot establish this.

Suggested rubric (each criterion scored 0–4):

1. **Meaning and fidelity to sources:** Was the content preserved without adding claims?
2. **Natural sentence flow:** Are Turkish syntax and rhythm appropriate?
3. **Unnecessary stock phrases:** Are there clichés such as “In today's rapidly changing world,” repeated summaries, or ornate but empty adjectives?
4. **Terminology consistency:** Are “ajan (agent),” “bağlam (context),” and “istem (prompt)” used consistently and in line with the series glossary?
5. **Usefulness to readers:** Is the text concrete, instructive, and appropriately detailed?
6. **Critical judgment:** Does it preserve uncertainty and distinguish sources from dates?

Where possible, evaluate **with model names hidden**. Fluent prose does not establish factual accuracy. Book prose and GitHub documentation should use consistent language, without becoming a collection of mechanically repeated slogans.

## 5. Coding and agent tasks

**Coding evaluation** is not a count of lines generated in one attempt. The practical measure is how well the model understands the problem and completes a small, safe change.

- Start from the same repository commit and test suite.
- Confirm the failing test. The model changes only files within scope.
- Deleting tests, weakening assertions, exceeding tool permissions, and reading secrets are **failures**.
- Count total token use, tool calls, retries requested by the model, and human corrections.
- Record the terminal state as `done`, `blocked`, `needs-review`, `unsafe`, or `budget-exceeded` (see root [AGENTS.md](../../../AGENTS.md)).
- The ideal operational measures are **cost per safely completed task** and **human review effort**.

## 6. How to read a benchmark

**SWE-bench Verified**, **SWE-bench Pro**, **Terminal-Bench**, **LiveCodeBench**, **Humanity's Last Exam**, **GPQA**, **MMMU**, **OSWorld**, **Toolathlon**, and the **Artificial Analysis Intelligence Index** measure different things. Results from one cannot substitute for another.

Record the following with a benchmark result:

| Field | Why it matters |
|---|---|
| Benchmark + version / date | The task set may have changed |
| Evaluated model ID / snapshot | The marketing name is insufficient |
| Agent harness + tool permissions | The same model can perform differently in different environments |
| Reasoning effort / token or time budget | Makes the advantage of higher budgets visible |
| Single attempt or best-of-N? | Multiple samples can inflate success |
| External sources, browsing, or test feedback? | These change comparison conditions |
| Independent result or provider experiment? | Allows conflicts of interest to be assessed |
| Leakage / contamination note | Training and test data need separation |

**Sources:** [SWE-bench](https://www.swebench.com/), [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro), [Terminal-Bench](https://www.tbench.ai/), [Artificial Analysis](https://artificialanalysis.ai/), [DORA research](https://dora.dev/research/). These are **sources to follow**; no current scores were derived from them in this document.

## 7. Production migration gates

1. **Pilot:** Representative tasks without real personal data.
2. **Comparison:** Run the previous and candidate versions side by side; compare tests and cost.
3. **Shadow traffic:** Measure without affecting production, where data policy permits.
4. **Canary release:** A small traffic share; track errors, cost, and safety alerts.
5. **Rollback:** A design that can return to a fixed model/snapshot.
6. **Record:** Why was it selected, which version, who approved it, and when will it be retested?

**Rule:** A new model version is a new candidate until it demonstrates better outcomes for the task.

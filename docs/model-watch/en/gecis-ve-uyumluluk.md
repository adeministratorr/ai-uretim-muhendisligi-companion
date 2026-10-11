# Model migrations and API compatibility | Catching silent changes

**[Türkçe](../tr/gecis-ve-uyumluluk.md) · [English](../en/gecis-ve-uyumluluk.md)** · [Model Watch](../README.md)

**Source review:** 2026-10-11 · **Translation review:** 2026-10-11 · **Scope:** Migration examples from official provider documentation and a proposed review method. No live account/request tests were performed.

An API request returning `200 OK` does not mean the application is still using **the same model**. A provider can redirect an old model name, retire a preview, change billing, or alter `tool_calls` behavior. Treat an upgrade as more than a package-version change.

## Notable migrations as of October 2026

| Provider | Previous / changing usage | Current direction | Risk and verification |
|---|---|---|---|
| **DeepSeek** | `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp` | `deepseek-flash` (V4.1-Flash); temporary redirection of old names | The model may have changed even if the old name works. [Official V4.1 note](https://api-docs.deepseek.com/news/news260910/) |
| **DeepSeek V4-Pro** | Redirection was announced for September 14 | The current getting-started page lists `deepseek-v4-pro` among available models | Read documents in date order; **live model and billing verification are required.** [Getting-started note](https://api-docs.deepseek.com/quick_start/pricing-details-cny/) |
| **Legacy DeepSeek names** | `deepseek-chat`, `deepseek-reasoner` | Migration to the V4 family | Retirement was announced for July 24, 2026; do not rely on them now. [V4 note](https://api-docs.deepseek.com/news/news260424/) |
| **xAI** | `grok-code-fast-1`, `grok-4-1-fast-*`, `grok-3` | Redirection to Grok 4.3 was announced from May 15, 2026; use the current model directory for new work | Behavior/pricing can change without an error. [Migration](https://docs.x.ai/developers/migration/may-15-retirement) |
| **Google** | `gemini-3-pro-preview` | `gemini-3.1-pro-preview` | The old preview closed on March 9, 2026. [Schedule](https://ai.google.dev/gemini-api/docs/deprecations/) |
| **Google TTS** | `gemini-3.1-flash-tts-preview` | `gemini-3.8-flash-tts` / Lite | A November 17, 2026 retirement date is listed. [Schedule](https://ai.google.dev/gemini-api/docs/deprecations/) |
| **OpenAI** | `chat-latest`, generic “latest model” tracking | Explicit model ID / snapshot strategy in production | `chat-latest` is an updated alias; experimentation and product development have different needs. [Changelog](https://developers.openai.com/api/docs/changelog) |
| **Tencent** | Legacy Hunyuan API/model IDs | TokenHub and the provider's current HY model identifiers | This is a **platform change**; editing the `model` field alone may be insufficient. [Migration](https://cloud.tencent.com/document/product/1729/131925) |
| **ByteDance** | Doubao Seed 2.0 Pro/Code | Seed 2.1 Pro/Turbo | An August 8, 2026 retirement note is available. [Pricing/migration](https://docs.volcengine.com/docs/aidap/Billing_items_and_prices_of_large_model_access?lang=en) |
| **Mistral** | Production migration to Large 4 | **Preview** as of October 11 | Distinguish it from Large 3; planned weight releases are not completed releases. [Announcement](https://mistral.ai/news/mistral-large-4/) |

## Compatibility matrix: is “OpenAI-compatible” enough?

Test the following areas **separately for every provider**. Accepting the same HTTP format does not establish equivalent semantics.

| Capability | What to check |
|---|---|
| Basic chat | `system` / `user` / `assistant` order, response schema |
| Responses API | Response object, state, tool continuation, error codes |
| Structured outputs | Strict JSON Schema behavior, malformed responses, missing fields |
| Function/tool calling | Parallel calls, argument types, call IDs, binding results to calls |
| Reasoning | `reasoning_effort` or provider-specific `thinking`; unsupported values |
| Streaming | Partial JSON chunks, final usage, state after cancellation |
| Multimodal input | Image/PDF/audio/video size, file formats, input order |
| Long context | Recall of critical system-prompt instructions, source retrieval, information near the end |
| Tokens / caching | Tokenizer differences, cache writes/reads, TTL, hidden reasoning cost |
| Region and data | Processing location, log retention, data residency, contract |
| Status codes | 429, 5xx, timeouts; exponential backoff; idempotency |
| Pricing | Long-context tiers, batch, tool calls, caching, special speed tiers |

## Upgrade checklist

- [ ] The change was verified through a primary announcement or model card.
- [ ] **Exact model ID / snapshot / provider / region** were recorded.
- [ ] The actual API model identifier was established, rather than relying on a product-interface name.
- [ ] Pricing, context, maximum output, cache, and tool charges were recalculated.
- [ ] JSON Schema, tool-call, long-context, and Turkish-language quality tests were rerun.
- [ ] The model was checked for attempts to exceed its tool permissions.
- [ ] Backward-incompatible schema and tool behavior changes were documented.
- [ ] Canary, rollback, and stopping thresholds were defined.
- [ ] The model's review date was added to the relevant book lab.
- [ ] The change was reviewed in a small PR.

## Example version record template

```yaml
migration_id: MW-2026-10-001
checked_at: "2026-10-11"
provider: "example-provider"
previous_model: "example-old"
new_model: "example-new"
endpoint: "example-endpoint"
region: "example-region"
source_urls: []
behavioral_differences: []
regression_suite: "not-run"
cost_impact: "not-measured"
rollback_model: "example-old"
approval: "pending-human-review"
terminal_state: "needs-review"
```

This YAML is a **template**, not a record of a completed migration.

## Production principle

An alias provides convenience; it is **not a promise of reproducibility**. Prefer fixed versions/snapshots for reproducible education/lab work and critical applications where available. Where pinning is unavailable, regularly observe the version, returned model identifier, response schema, and cost. Code must preserve the expected behavior as well as run successfully.

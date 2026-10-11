# Model Watch | Sources and evidence levels

**[Türkçe](../tr/kaynaklar-ve-guncelleme.md) · [English](../en/kaynaklar-ve-guncelleme.md)** · [Model Watch](../README.md)

**Version:** 2026-10 · **Initial comprehensive source review:** 2026-10-11 · **Translation review:** 2026-10-11 · **Review method:** Documentation and model-card inspection. **No live API requests were made to measure versions, prices, or speed.**

## What counts as “verified”?

AI model names can vary from one report to another. We therefore assign different evidence levels to sources:

| Label | Meaning | Appropriate use |
|---|---|---|
| **R1 — Official, current** | The provider's current API model list, model card, pricing, retirement table, or license text | Technical record with a date and link |
| **R2 — Official announcement** | A change published in the producer's blog or changelog | Dated announcement; scope/GA stated separately |
| **R3 — Independent measurement** | A reproducible benchmark or project test with a clear method | Comparison limited to the measured task and conditions |
| **R4 — Third-party news/community** | Press, forums, GitHub issues, comparison sites | A lead to follow, not a substitute for official information |
| **B — Uncertain / conflicting** | Old and new sources disagree, or an endpoint redirects to another version | No definitive conclusion; an explicit follow-up item |
| **T — Not tested** | A source makes a claim, but we have no API test | “Stated in the documentation,” not “we measured it” |

**Terminology rule:** The “verification date” is the date of our source review. Model release, GA, snapshot, weight release, and API availability can each have different dates.

## Primary source directory

The links below support tracking model families and version information; they do not imply every page was updated on the same day.

### Global providers

| Provider | Official API/model source | Announcement / retirement / additional document |
|---|---|---|
| OpenAI | [Model directory](https://developers.openai.com/api/docs/models/all) | [Changelog](https://developers.openai.com/api/docs/changelog) |
| Anthropic | [Model comparison](https://platform.claude.com/docs/en/models/overview) | [Model cards](https://platform.claude.com/docs/en/resources/overview) |
| Google Gemini | [Model list](https://ai.google.dev/gemini-api/docs/models) | [Deprecation schedule](https://ai.google.dev/gemini-api/docs/deprecations/) |
| Google Gemma | [Gemma documentation](https://ai.google.dev/gemma) | Version-specific model card / license |
| xAI / SpaceXAI | [API models](https://docs.x.ai/developers/models) | [Legacy model migration](https://docs.x.ai/developers/migration/may-15-retirement) |
| Meta | [Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api) | [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) |
| Mistral | [Model catalog](https://docs.mistral.ai/models/) | [Large 4 announcement](https://mistral.ai/news/mistral-large-4/) |

### Chinese providers

| Provider | Official / primary source | Main review topic |
|---|---|---|
| Alibaba Qwen | [Model Studio list](https://www.alibabacloud.com/help/en/model-studio/models) | Max/Flash/API, region, snapshot |
| Qwen weights | [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [2.4T](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) | Distinguishing Apache 2.0 from custom licensing |
| DeepSeek | [API updates](https://api-docs.deepseek.com/updates/) | Legacy aliases, V4-Pro status, V4.1-Flash |
| DeepSeek | [Current getting-started and pricing notes](https://api-docs.deepseek.com/quick_start/pricing-details-cny/) | Routing notes that conflict with earlier announcements |
| Z.ai GLM | [Official repository](https://github.com/zai-org/GLM-5) | GLM 5.3 / Flash models |
| GLM 5.3 | [Model card + license](https://huggingface.co/zai-org/GLM-5.3) | Custom `glm-5.3` terms |
| Moonshot Kimi | [Official announcements](https://forum.moonshot.ai/c/announcement/5) | K3 general availability, API/subscription |
| Kimi K3 | [Model card + license](https://huggingface.co/moonshotai/Kimi-K3) | Commercial usage terms |
| MiniMax | [Token/API plans](https://platform.minimax.io/subscribe/token-plan) | Differences between caching, tokens, and subscriptions |
| MiniMax M3 | [Model card + license](https://huggingface.co/MiniMaxAI/MiniMax-M3) | Community license |
| ByteDance | [Volcengine API documentation](https://docs.volcengine.com/docs/ark/model-list?lang=en) | Seed 2.1 identifiers |
| Baidu | [AI Studio model list](https://ai.baidu.com/ai-doc/AISTUDIO/Mmhslv9lf) | ERNIE model and context data |
| Tencent | [Hunyuan migration notes](https://cloud.tencent.com/document/product/1729/131925) | TokenHub migration / legacy model retirement |
| Xiaomi | [XiaomiMiMo](https://github.com/XiaomiMiMo) | MiMo model code and hosting |

### Measurement and industry research

- [SWE-bench](https://www.swebench.com/), [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro), [Terminal-Bench](https://www.tbench.ai/) — Coding/agent tasks. Comparisons require the same benchmark version and harness.
- [Artificial Analysis](https://artificialanalysis.ai/) — Pricing, speed, and multidimensional model data; capture a dated snapshot.
- [DORA](https://dora.dev/research/) — Software delivery productivity; do not use it to prove one model's superiority.
- [Hugging Face model cards](https://huggingface.co/models) — Weights, licensing, and usage information; confirm that the publishing account belongs to the official developer.

## Priority follow-up items

| Topic | Why it remains open | Completion criterion |
|---|---|---|
| Mistral Large 4 weights | As of October 11, planned for late October | Official model card and downloadable files verified |
| DeepSeek V4-Pro routing | Earlier announcement and newer support note differ | Actual API response model ID, pricing, and a dated current support document |
| Grok 4.7 model/quota changes | New API option | Model card + production test |
| Licenses within Qwen3.8 | Not identical across model sizes | Full license text for each weights repository |
| GLM 5.3 / Kimi K3 / MiniMax M3 commercial licenses | Custom license conditions | Commercial-use review and permission where required |
| New Claude/OpenAI/Google defaults | User applications and APIs differ | Verification against dated client/model identifiers |
| Turkish quality test set | Model claims are not project-specific evidence | A versioned fixture set evaluated blind |

**Principle:** Model Watch records current information without inventing results. If something is unknown, say “not verified.”

# The global model ecosystem | Looking beyond model names

**[Türkçe](../tr/kuresel-modeller.md) · [English](../en/kuresel-modeller.md)** · [Model Watch](../README.md)

**Source review:** 2026-10-11 · **Translation review:** 2026-10-11. The information below comes from provider announcements and model cards; it is not an independent performance measurement. Prices, access, and service regions can change.

## 1. OpenAI — GPT-6, Codex, and multimodal services

| Model / product | Position in the documentation | Where to evaluate it |
|---|---|---|
| **GPT-6 Astra** | The most capable flagship in the API catalog | Difficult reasoning and high-stakes tasks with testable outcomes |
| **GPT-6.1 Sol** (`gpt-6.1-sol`) | Cost-to-outcome balance for complex coding and professional work | Coding agents, complex tool workflows, computer use |
| **GPT-6 Luna** | High-volume, focused tasks | Classification, short data transformations, economical routing |
| **GPT-6 Sol** | The previous Sol version | Comparison and fallback in existing systems |
| **GPT-Image and audio models** | Services dedicated to input/output types beyond text | Image generation, editing, speech, transcription |

**Documented changes:** GPT-6.1 Sol was announced on September 29, 2026; `service_tier: "ultrafast"` was added as an option on October 8. The model card specifies a context window of approximately **1.05M tokens**. Ultrafast can be described as faster, but **this repository has no measured p95 latency result**. Check reasoning effort settings, Responses API tool-call support, and Chat Completions differences for each model.

**Developer note:** A ChatGPT subscription, the selected model in Codex, and an API `model` identifier are different concepts. Do not generalize statements such as “Codex currently defaults to…” without recording the client version, date, and settings. Changing aliases such as `chat-latest` are not fixed model versions either.

**Official sources:** [All models](https://developers.openai.com/api/docs/models/all) · [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [API changes](https://developers.openai.com/api/docs/changelog).

## 2. Anthropic — The Claude family

Anthropic's current model comparison page lists **Claude Fable 5.1**, **Opus 5.5**, **Sonnet 5.5**, and **Haiku 5.5**. These names represent different workload tiers:

| Family | Typical reason to consider it | What to test |
|---|---|---|
| Fable 5.1 | The hardest long-horizon reasoning/agent tasks | Cost and independently measured performance differences |
| Opus 5.5 | Intensive coding, research, and knowledge work | Budget/quality balance and staying on task |
| Sonnet 5.5 | Balance for general coding and agent tasks | Retry count on complex tasks |
| Haiku 5.5 | High-volume, latency-sensitive work | Schema errors and misplaced confidence |

**Product/API distinction:** Claude Code, the Claude application, and the Anthropic Messages API do not necessarily share a default model. Identifiers, regions, and access can differ across AWS, Google Cloud, and Microsoft deployments. Features such as adaptive thinking, tool use, and prompt caching are documented separately for each version.

**Sources:** [Claude model comparison](https://platform.claude.com/docs/en/models/overview) · [Model cards](https://platform.claude.com/docs/en/resources/overview) · [Deprecations](https://docs.anthropic.com/en/docs/about-claude/model-deprecations).

## 3. Google — Gemini, Gemma, and specialized models

**Gemini 3.8 Flash** (`gemini-3.8-flash`) is **GA**: 1,048,576 input tokens, 65,536 output tokens, `low/medium/high` thinking, function calling, and structured output are documented. Google's model directory also includes options such as **Gemini 3.7 Flash**, **3.6 Flash**, **3.5 Flash-Lite**, and **3.1 Pro Preview**.

- **Gemini 3.8 Flash:** A candidate for long documents, visual/audio input, coding, and tool chains. Confirm supported tools and regional quotas before production use.
- **Gemini 3.1 Pro Preview:** A separate candidate for general and complex agent tasks, with a *preview* lifecycle. A higher number in “3.8” does not establish superiority over Pro for every use case.
- **Gemini 3.8 Live / Live Extended Thinking:** Real-time audio dialogue, with capacities and API constraints different from those of the text model.
- **Gemma:** Google's downloadable-weight family; read each size's model card for licenses, quantization, and runtime support, including versions such as Gemma 4.
- **Image generation / audio / embeddings:** Nano Banana, TTS, and embedding models should not share a comparison column with general chat models; their success criteria differ.

**Sources:** [Gemini model list](https://ai.google.dev/gemini-api/docs/models) · [Gemini 3.8 Flash card](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Retirement and replacements](https://ai.google.dev/gemini-api/docs/deprecations/) · [Gemma](https://ai.google.dev/gemma).

## 4. xAI / SpaceXAI — Grok

The current official model page highlights **Grok 4.7** (`grok-4.7`) for coding, tool calling, and general use. It lists **500k context** and API rates of **$2 per 1M input tokens and $6 per 1M output tokens**; check token tiers, regions, and additional service charges separately. **Grok 4.5** is a previous version with its own documented model card.

**A mistaken assumption:** Sharing an ecosystem with X does not mean Grok automatically knows real-time events on every request. The provider explicitly states that Web Search / X Search tools must be enabled. Access to a search tool does not guarantee correct sourcing; sources still need review.

**Migration note:** The May 15, 2026 retirement notice described automatic redirection of older identifiers such as `grok-4-1-fast-*`, `grok-3`, and `grok-code-fast-1` to Grok 4.3. Results and billing can change even when a request succeeds. Test aliases explicitly.

**Sources:** [Grok model directory](https://docs.x.ai/developers/models) · [Grok 4.5 card](https://docs.x.ai/developers/models/grok-4.5) · [Older model migration](https://docs.x.ai/developers/migration/may-15-retirement).

## 5. Meta AI / Llama — Two different strategies

**Muse in Meta AI and downloadable Llama are different models.**

- **Muse Spark (April 8, 2026):** Meta's new family focused on multimodal reasoning and tool use, initially made available through meta.ai and the application.
- **Muse Spark 1.1 (July 9, 2026):** Introduced with coding, computer-use, and multimodal improvements, alongside a public preview announcement for Meta Model API. Do not claim it has **the same form of access as Llama weights**.
- **Llama 4 Scout / Maverick (2025):** A downloadable-weight family whose licensing, usage limits, and data-processing design need separate review. **Llama 4 Behemoth** was still described as being trained in the initial announcement; an announcement does not automatically establish GA status.
- **Muse Image / Muse Video:** Image/video product lines that should be evaluated separately from text-focused models.

**Question to track:** As Meta's closed Muse line develops, how is its release, update, and licensing strategy for Llama weights changing? Answer this through new primary announcements, not speculation.

**Sources:** [Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-1-msl/) · [Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api) · [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) · [Muse Image/Video](https://ai.meta.com/blog/introducing-muse-image-muse-video-msl).

## 6. Mistral AI — Large 4, Large 3, and specialized models

**Mistral Large 4** was introduced in an **October 6, 2026** announcement with a public API preview. The company described a multimodal MoE with **1 trillion total / 52 billion active parameters**. Model weights are **scheduled for release at the end of October 2026**. They should not be described as already released on October 11.

**Mistral Large 3** is a separate model: its official card specifies **675B total / 41B active parameters, 256k context, and Apache 2.0**. Specialized models for OCR, document processing, security, coding, or robotics do not belong in a general LLM ranking solely because they share a brand.

**Europe-focused decisions:** Consider Mistral when sovereignty, on-premises hosting, multilingual support, and data residency matter. However, “European company = automatic GDPR/KVKK compliance” is not a valid inference; examine the contract, processing region, and logging policy.

**Sources:** [Large 4 announcement](https://mistral.ai/news/mistral-large-4/) · [Large 3 card](https://docs.mistral.ai/models/mistral-large-3-25-12) · [Current announcements](https://mistral.ai/news/).

## 7. Other important providers: watchlist

The following providers warrant regular attention in broader market/product research, but **this edition makes no claims about their latest models, prices, or benchmark scores**:

| Ecosystem | What to track | Starting source |
|---|---|---|
| Cohere / Command | Enterprise RAG, reranking, private deployment | https://docs.cohere.com/ |
| AI21 Labs / Jamba | Long context, data flows, enterprise API | https://docs.ai21.com/ |
| IBM / Granite | Open weights, governance, enterprise use | https://www.ibm.com/granite |
| NVIDIA / Nemotron | Open models, datasets, and deployment systems | https://developer.nvidia.com/nemotron |
| Microsoft / Phi | Small and on-device models | https://huggingface.co/microsoft |
| Amazon / Nova | AWS-based multimodal/enterprise workloads | https://docs.aws.amazon.com/nova/ |
| Stability AI, Black Forest Labs | Image generation and editing | https://stability.ai/ · https://blackforestlabs.ai/ |
| Runway, Luma, Kling, Pika | Video generation and creative workflows | The provider's official developer page |

**Note:** Inclusion here does not mean an October 2026 model review was completed for every provider.

## Conclusion: task outcomes over brand names

Repairing a codebase and classifying 100,000 short customer messages require different model-selection decisions. A model can look capable on paper yet disrupt the flow of Turkish prose, make unexpected tool calls, or consume unnecessary tokens in our tests. This repository centers **demonstrated task outcomes** rather than marketing language.

Continue: [Chinese models](cinli-modeller.md) · [How to measure](model-secimi-ve-olcum.md).

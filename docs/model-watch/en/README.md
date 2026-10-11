# Model Watch | AI model and tool observatory

**[Türkçe](../tr/README.md) · [English](../en/README.md)** · [Model Watch](../README.md)

> **Last verification: 2026-10** · **Last comprehensive source review:** 2026-10-11 · **Translation review:** 2026-10-11 · **Language:** English · **Scope:** AI Production Engineering, 4 volumes · **Status:** A snapshot based on documentation review; no live API tests.

AI model names, prices, and capabilities can change within months. A model mentioned in the book is therefore not a recommendation that remains valid for years. **Model Watch** is the current, auditable companion to the four-volume series: what changed, which information can we trust, why are we making a particular choice, and how does a change affect a working application?

The purpose is not to crown a new champion every month. A model being **announced**, **available through an API**, **released as downloadable weights**, and **safe to use in production** describes different stages. Keep those distinctions visible.

## Where to start

| Document | Contents | Most useful for |
|---|---|---|
| [October 2026 snapshot](2026-10-gorunumu.md) | Notable changes and current status | Readers who want a quick update |
| [Chinese model ecosystem](cinli-modeller.md) | Qwen, DeepSeek, Kimi, GLM, MiniMax, Doubao, ERNIE, Hunyuan, MiMo, and others | Readers exploring alternative APIs and open weights |
| [Global model ecosystem](kuresel-modeller.md) | OpenAI, Claude, Gemini/Gemma, Grok, Meta/Llama, Mistral, and others | Readers comparing a broad set of options |
| [Model selection and evaluation](model-secimi-ve-olcum.md) | Task-based selection, cost, Turkish-language quality, test matrices, and benchmark literacy | Project builders and educators |
| [Migration and API compatibility](gecis-ve-uyumluluk.md) | Aging model identifiers, alias risks, regression tests | People maintaining working systems |
| [Sources and update principles](kaynaklar-ve-guncelleme.md) | Primary sources, evidence labels, update and contribution rules | Contributors and coding agents |
| [Shared model data](../data/README.en.md) | 29 model records, the JSON data layer, and the validator | Developers working on bilingual publishing and automation |

## Essential distinctions

- **Model / product / provider / distribution:** ChatGPT and the GPT API, Claude chat and the Claude API, Meta AI and Llama weights are different products.
- **General availability (GA) / preview / private access:** Preview status does not guarantee production readiness.
- **Open weights / open source / open license:** Downloadable model files do not imply unrestricted commercial distribution. Read the license for the specific version.
- **Context / actual performance:** Accepting 1 million tokens does not establish accurate answers across that entire length.
- **Compatible API / equivalent behavior:** Accepting OpenAI-format requests does not imply identical `tool_calls`, reasoning, JSON schema, vision, or token-counting behavior.
- **Provider benchmark / independent evaluation:** Record the former as a claim and seek the latter separately; do not present either as the book's own results.

## Connection to the book

| Volume | How Model Watch supports it |
|---|---|
| **1 — AI Literacy and Prompt Engineering** | Model limits, prompt design, structured output, fact-checking, and Turkish prose |
| **2 — Vibe Coding and Loop Engineering** | Coding-model selection, debugging, test feedback, token budgets, and model migration |
| **3 — Agent Engineering** | Tool calls, permission boundaries, long tasks, MCP, memory, and rollback |
| **4 — AI-Native Production** | Gateways, cost, routing, observability, regression tests, and safe upgrades |

## Update schedule

| Frequency | What to check |
|---|---|
| Weekly (priority events) | API availability of new models, retirement dates, pricing/license changes, breaking changes |
| Monthly | Provider/model tables, official identifiers, access regions, token windows, open weights, and licenses |
| Quarterly | Task-based tests, Turkish quality, long context, agent reliability, DORA, and industry data |
| Every book/lab update | Whether example model identifiers and parameters match current documentation |

## Bilingual publishing layout

**Turkish is the source edition:** `docs/model-watch/tr/`. The English edition is in `docs/model-watch/en/`. Paired guides retain their filenames, section order, table columns, and source links. Each English document carries its own translation-review date, separately from the source-review date. A translation review does not mean the technical information was reverified. Both editions use the same `data/models.json` catalog. The parent README provides language selection.

## For readers and contributors

When citing these pages, distinguish the **document date** from the **model release date**. When reporting an error or a new version, include the official source link, the changed field, and the review date. [CONTRIBUTING.md](../../../CONTRIBUTING.md) governs contributions; [AGENTS.md](../../../AGENTS.md) defines coding-agent boundaries. These repository policies are currently in Turkish.

**Working principle:** Model names can change; verification, testing, and the ability to roll back should remain.

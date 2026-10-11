# Shared model records

**[Türkçe](README.md) · [English](README.en.md)** · [Model Watch](../README.md)

**Translation review:** 2026-10-11 · **Catalog source-review date:** read the root `last_verified` field in [models.json](models.json). Translation review does not constitute a new technical verification.

`models.json` is Model Watch's **shared data layer across languages**. Turkish text lives in `tr/`, English text in `en/`; both editions use this one catalog. Do not use the catalog directly as application runtime configuration: statuses such as `listed`, `preview`, `released`, and `watch` do not guarantee capability or access. Optional free-text `note` values currently remain in Turkish; the field names, model identifiers, and status codes are shared.

## Fields

| Field | Meaning |
|---|---|
| `provider`, `family`, `name` | Producer, family, and model name |
| `model_id` | Exact API or weights-repository identifier when verified in the documentation; otherwise `null` |
| `status` | `ga`, `preview`, `listed`, `released`, `watch` |
| `distribution` | `api`, `weights`, `api_and_weights`, `unknown` |
| `license` | License label **only when explicitly checked** |
| `evidence` | `R1`, `R2`, `R3`, `R4`, `B`, `T` — explained in the [source standard](../en/kaynaklar-ve-guncelleme.md) |
| `source` | Primary source (one URL) |
| `last_verified` (root) | Date of the last source review for the whole catalog |

**Important:** A model card's download license and an API service's terms of use are not necessarily the same. `model_id: null` is a deliberate representation of unknown information; do not invent an example ID. Reverify the source for each future change, then update the JSON and prose documents together.

Run `python3 docs/model-watch/scripts/validate.py` from the repository root to check JSON structure and local Markdown links. This command does not access the network.

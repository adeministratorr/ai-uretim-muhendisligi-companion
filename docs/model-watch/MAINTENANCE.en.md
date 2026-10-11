# Model Watch | Repository maintenance guide

This document and its supporting files remain in the GitHub repository and are excluded from GitHub Pages. Reader pages are under `tr/` and `en/`. The root `_config.yml` excludes agent instructions, maintenance guides, validation scripts, and the `data/` catalog from publication.

## Validation

Run from the repository root:

```bash
python3 docs/model-watch/scripts/validate.py
```

The command checks JSON structure and local Markdown links; it does not verify external sources or live API behavior.

[Data reference](data/README.en.md) · [Shared catalog](data/models.json) · [Contribution guide](../../CONTRIBUTING.md) · [Agent rules](../../AGENTS.md)

## Update schedule

| Frequency | What to check |
|---|---|
| Weekly (priority events) | API availability of new models, retirement dates, pricing/license changes, breaking changes |
| Monthly | Provider/model tables, official identifiers, access regions, token windows, open weights, and licenses |
| Quarterly | Task-based tests, Turkish quality, long context, agent reliability, DORA, and industry data |
| Every book/lab update | Whether example model identifiers and parameters match current documentation |

## Bilingual publishing layout

**Turkish is the source edition:** `docs/model-watch/tr/`. The English edition is in `docs/model-watch/en/`. Paired guides retain their filenames, section order, table columns, and source links. Each English document carries its own translation-review date, separately from the source-review date. A translation review does not mean the technical information was reverified. Both editions use the same `data/models.json` catalog. The parent README provides language selection.

## How to record an update

Where possible, include the following in each proposed change:

```yaml
model_watch_record:
  checked_at: "2026-10-11"
  provider: "<provider>"
  product_family: "<family>"
  model_id: "<API-id-or-weight-repo>"
  snapshot: "<exact-version-or-unknown>"
  claim: "<what-has-changed>"
  status: "ga | preview | limited | retired | unknown"
  evidence: "R1 | R2 | R3 | R4 | B | T"
  sources:
    - url: "https://<official-source>"
      checked_at: "2026-10-11"
  api_test: "not-run"
  last_verified: "2026-10"
  reviewer: "pending"
```

## Contribution and verification workflow

1. **Research:** Find the official announcement, API model list, and model card where available.
2. **Separate:** Distinguish model identifiers, product names, API access, dated snapshots, licenses, and regions.
3. **Compare:** Produce a diff against the previous record. Check the **dates** of conflicting sources.
4. **Limit claims:** Without independent tests, do not draw conclusions from marketing benchmarks; write “according to the company's own measurements.”
5. **Verify:** Review Markdown links, relative paths, date notes, claims, and the model-watch table.
6. **Test:** Run relevant lab regressions when live API access and explicit permission are available. Otherwise record `not-run`.
7. **Review:** The AGENTS.md terminal-state and human-review rules apply.
8. **Publish:** Add the date, scope, and remaining uncertainties to the changelog.

## English edition standard

The English edition is in `docs/model-watch/en/`; the Turkish edition is in `docs/model-watch/tr/`. Paired guides retain the same filename, section order, and table structure. Source URLs, API model identifiers, numerical values, and executable examples remain unchanged in translation. Each English document records its source-review date and a separate translation-review date; reviewing a translation does not constitute a new source review or live API test. A model added to Turkish is not automatically considered added to English. Keep one shared catalog in `data/models.json`, with field documentation in both languages. Language switches link to the corresponding document. Before publication, check local links, source URL parity, section/table structure, and examples.

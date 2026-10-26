# Uygulama sırası

Her satır ayrı bir uygulamadır. Girdi ve çıktı yolları okurun Pusula deposuna göredir. Bu pakette 36 uygulamanın promptları taslak olarak bulunur; uygulama kodu ve model denemeleri `not_run` durumundadır.

| No | Uygulama | Üretilecek dosyalar |
|---|---|---|
| [U01](prompts/01.md) | Ürünü ve okurun ortamını tanımlamak | `vision.md`, `scope.md`, `environment.md` |
| [U02](prompts/02.md) | Gereksinimleri kabul ölçütüne çevirmek | `prd.md`, `acceptance.md`, `user-stories.md` |
| [U03](prompts/03.md) | Ekranları ve etkileşimi tasarlamak | `design.md`, `accessibility.md` |
| [U04](prompts/04.md) | Teknoloji seçimini gerekçelendirmek | `tech-stack.md`, `dependency-policy.md`, `adr/0001-stack.md` |
| [U05](prompts/05.md) | Veri ve çıktı sözleşmesini kurmak | `data-model.md`, `api-contract.md`, `schemas/answer.schema.json` |
| [U06](prompts/06.md) | Yol haritasını yapılabilir işlere bölmek | `roadmap.md`, `tasks.md`, `dependencies.md` |
| [U07](prompts/07.md) | Ajanın proje yönergelerini üretmek | `AGENTS.md`, `CLAUDE.md`, `docs-map.md`, `README.md`, `.gitignore` |
| [U08](prompts/08.md) | Tekrarlanan yöntemi skill paketine dönüştürmek | `skills/pusula-belge-uret/SKILL.md`, `skills/pusula-kaynak-denetle/SKILL.md`, `skill-tests.json` |
| [U09](prompts/09.md) | Prompt engineering deneyini kurmak | `prompts/answer-v1.md`, `prompts/answer-v2.md`, `prompts/answer-v3.md`, `evals/prompt-cases.json` |
| [U10](prompts/10.md) | Promptları ölçüp iyileştirmek | `evals/prompt-results.json`, `optimization.md` |
| [U11](prompts/11.md) | İlk çalışan uygulamayı üretmek | `app/`, `tests/`, `runbook.md` |
| [U12](prompts/12.md) | Hata ayıklama ve Git döngüsünü kurmak | `debugging.md`, `review.md`, `checkpoints.md` |
| [U13](prompts/13.md) | Context engineering ile bağlamı seçmek | `context-policy.md`, `context-index.json`, `evals/context-results.json` |
| [U14](prompts/14.md) | Belleğin yaşam döngüsünü yönetmek | `memory-policy.md`, `memory-tests.json` |
| [U15](prompts/15.md) | Kaynaklı yanıt için RAG hattı kurmak | `retrieval.md`, `rag-tests.json`, `app/retrieval/` |
| [U16](prompts/16.md) | Bilgi grafını karşılaştırmalı denemek | `graph-design.md`, `graph-results.json`, `app/graph/` |
| [U17](prompts/17.md) | Araç ve izin sözleşmelerini yazmak | `tool-contracts.json`, `permissions.md` |
| [U18](prompts/18.md) | MCP bağlantısını kurup sınamak | `mcp-design.md`, `mcp-tests.json`, `app/mcp/` |
| [U19](prompts/19.md) | Loop engineering ile çalışmayı sınırlamak | `loop-spec.md`, `loop-state.json`, `loop-tests.json` |
| [U20](prompts/20.md) | Harness engineering ile yürütmeyi kurmak | `harness-design.md`, `harness-manifest.json`, `app/harness/` |
| [U21](prompts/21.md) | Uzun görevleri kesintiden sürdürmek | `resume-protocol.md`, `recovery-tests.json` |
| [U22](prompts/22.md) | Alt ajanlara görev vermek | `agents.md`, `delegation-contracts.json`, `agents/` |
| [U23](prompts/23.md) | Çoklu ajanı tek ajanla karşılaştırmak | `parallel-work.md`, `evals/agent-comparison.json` |
| [U24](prompts/24.md) | Evals ile sürüm kabulünü ölçmek | `eval-plan.md`, `evals/release-cases.json`, `evals/rubric.md` |
| [U25](prompts/25.md) | Güvenlik ve veri sınırlarını denemek | `threat-model.md`, `data-lifecycle.md`, `security-cases.json` |
| [U26](prompts/26.md) | Çok kipli girdiyi ve tarayıcı akışını eklemek | `multimodal.md`, `browser-acceptance.md`, `multimodal-cases.json` |
| [U27](prompts/27.md) | Olay ve zaman temelli otomasyon kurmak | `automation.md`, `schedule-contracts.json` |
| [U28](prompts/28.md) | A2A ve ajanlara açık webi karşılaştırmak | `interoperability.md`, `agent-card.json`, `agentic-web.md` |
| [U29](prompts/29.md) | Model geçidi ve maliyet deneylerini kurmak | `model-policy.md`, `budget.md`, `model-results.json` |
| [U30](prompts/30.md) | Hizmeti izlemek ve kapasiteyi ölçmek | `observability.md`, `service-targets.md`, `capacity.md` |
| [U31](prompts/31.md) | Dağıtım ve geri dönüşü prova etmek | `release.md`, `rollback.md`, `migration.md`, `ci-plan.md` |
| [U32](prompts/32.md) | Takım, lisans ve yönetişim dosyalarını üretmek | `governance.md`, `licenses.md`, `ownership.md`, `adoption.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md` |
| [U33](prompts/33.md) | Skill ve araçları dağıtım paketine çevirmek | `plugin-plan.md`, `compatibility.md`, `distribution.md` |
| [U34](prompts/34.md) | Yeni yöntemleri aynı görevde karşılaştırmak | `approach-watch.md`, `experiments/approach-comparison.json` |
| [U35](prompts/35.md) | Model değişince sistemi yeniden değerlendirmek | `change-impact.md`, `experiments/ablation.json` |
| [U36](prompts/36.md) | Pusula projesini devretmek | `handoff.md`, `portfolio.md`, `coverage.md` |

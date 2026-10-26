# Proje dosyalarının görevleri

Bu yollar companion paketinin değil, okurun oluşturacağı Pusula uygulama deposunun düzenidir. Bir dosyanın bulunması aracın onu otomatik okuyacağı anlamına gelmez. Ajan yönergeleri hangi işte hangi dosyanın okunacağını belirtir.

| Dosya | Cevapladığı soru | Üreten uygulama |
|---|---|---|
| `vision.md`, `scope.md` | Kimin hangi sorunu çözülüyor, ilk sürümün sınırı ne? | U01 |
| `environment.md` | Okurun ortamında gerçekten hangi araçlar var? | U01 |
| `prd.md`, `user-stories.md`, `acceptance.md` | Hangi davranış hangi koşulda kabul edilecek? | U02 |
| `design.md`, `accessibility.md` | Kullanıcı işi hangi ekranlarla tamamlayacak? | U03 |
| `tech-stack.md`, `dependency-policy.md`, `adr/` | Teknoloji neden seçildi; sürüm ve bağımlılık nasıl korunacak? | U04 |
| `data-model.md`, `api-contract.md`, `schemas/` | Bileşenler hangi veriyi hangi kuralla paylaşacak? | U05 |
| `roadmap.md`, `tasks.md`, `dependencies.md` | Hangi iş hangi çıktıya bağlı, ne zaman tamamlanmış sayılacak? | U06 |
| `AGENTS.md`, `CLAUDE.md`, `docs-map.md` | Kodlama ajanı nasıl çalışacak, hangi kaydı okuyacak? | U07 |
| `skills/`, `skill-tests.json` | Tekrarlanan yöntem nasıl çağrılacak ve sınanacak? | U08 |
| `prompts/`, `evals/`, `runs/` | Hangi talimat hangi girdide ne sonuç verdi? | U09–10, U24 |
| `app/`, `tests/`, `runbook.md` | Ürün nasıl çalıştırılıp doğrulanacak? | U11–12 |
| `context-policy.md`, `memory-policy.md`, `retrieval.md` | Model hangi bilgiyi ne zaman görecek? | U13–16 |
| `tool-contracts.json`, `permissions.md` | Hangi araç hangi yetkiyle kullanılacak? | U17–18 |
| `loop-spec.md`, `harness-design.md`, `resume-protocol.md` | Çalışma nasıl ilerleyecek, duracak ve devam edecek? | U19–21 |
| `agents.md`, `delegation-contracts.json` | Ürün içindeki ajanların işi ve sınırı ne? | U22–23 |
| `threat-model.md`, `data-lifecycle.md` | Tehdit ve veri yaşam döngüsü nasıl denetlenecek? | U25 |
| `budget.md`, `observability.md`, `release.md`, `rollback.md` | Hizmetin maliyeti, durumu ve geri dönüşü nasıl yönetilecek? | U29–31 |
| `governance.md`, `ownership.md`, `handoff.md` | Kararı kim verecek ve bakım sorumluluğu nasıl devredilecek? | U32–36 |

`AGENTS.md` açık ajan yönergesi biçiminin adıdır. `agents.md` burada ürünün rol kataloğudur; otomatik yüklenen evrensel dosya olduğu ileri sürülmez. `agent.md` veya `techsctack.md` adında ikinci kopya üretilmez. Teknoloji kararı `tech-stack.md` içinde tutulur. Claude Code'a özgü ayrıntılar, ortak kuralları çoğaltmadan `CLAUDE.md` girişinden bağlanır.

## Belge bağımlılığı

```text
brief → vision + scope → prd + acceptance
                         ↓
                       design → tech-stack → data-model + api-contract
                         ↓                          ↓
                         roadmap + tasks + dependencies
                                      ↓
                           AGENTS + CLAUDE + docs-map
                                      ↓
                        skills + prompts + testler → uygulama
```

Bir gereksinim değiştiğinde etkilenen tasarım, görev, test ve yönerge birlikte gözden geçirilir. Her dosyayı aynı uzun özeti taşıyan bağımsız metin olarak üretmek çelişki riskini artırır. Ortak karar tek yerde tutulur, diğer dosyalar onu açıkça kaynak gösterir.

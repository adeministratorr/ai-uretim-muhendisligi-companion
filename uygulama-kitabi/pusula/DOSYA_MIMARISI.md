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
| `AGENTS.md`, `docs-map.md`, `agent-compatibility.md`, `instruction-tests.json`, `agent-adapters/` | Ortak kurallar kullanılan ajana nasıl aktarılacak ve yüklendiği nasıl sınanacak? | U07 |
| `skills/`, `skill-tests.json` | Tekrarlanan yöntem nasıl çağrılacak ve sınanacak? | U08 |
| `prompts/`, `evals/`, `runs/` | Hangi talimat hangi girdide ne sonuç verdi? | U09–10, U24 |
| `app/`, `tests/`, `runbook.md` | Ürün nasıl çalıştırılıp doğrulanacak? | U11–12 |
| `context-policy.md`, `memory-policy.md`, `retrieval.md` | Model hangi bilgiyi ne zaman görecek? | U13–16 |
| `tool-contracts.json`, `permissions.md` | Hangi araç hangi yetkiyle kullanılacak? | U17–18 |
| `loop-spec.md`, `harness-design.md`, `resume-protocol.md` | Çalışma nasıl ilerleyecek, duracak ve devam edecek? | U19–21 |
| `agent-roles.md`, `delegation-contracts.json` | Ürün içindeki ajanların işi ve sınırı ne? | U22–23 |
| `threat-model.md`, `data-lifecycle.md` | Tehdit ve veri yaşam döngüsü nasıl denetlenecek? | U25 |
| `budget.md`, `observability.md`, `release.md`, `rollback.md` | Hizmetin maliyeti, durumu ve geri dönüşü nasıl yönetilecek? | U29–31 |
| `governance.md`, `ownership.md`, `handoff.md` | Kararı kim verecek ve bakım sorumluluğu nasıl devredilecek? | U32–36 |

`AGENTS.md` açık ajan yönergesi biçiminin adıdır. `agent-roles.md` burada ürünün rol kataloğudur; otomatik yüklenen evrensel dosya olduğu ileri sürülmez. `agent.md` veya `techsctack.md` adında ikinci kopya üretilmez. Teknoloji kararı `tech-stack.md` içinde tutulur. Araca özgü yönergeler yalnız gerektiğinde eklenir. `CLAUDE.md` ve `GEMINI.md` gibi girişler bütün okurlar için zorunlu değildir. Dosya adları, yükleme koşulları ve örnekler [ajan uyumluluğu rehberindedir](AJAN_UYUMLULUGU.md). Rol kataloğunun farklı adı, harf büyüklüğünü ayırmayan dosya sistemlerinde çakışmayı önler.

## Belge bağımlılığı

```text
brief → vision + scope → prd + acceptance
                         ↓
                       design → tech-stack → data-model + api-contract
                         ↓                          ↓
                         roadmap + tasks + dependencies
                                      ↓
                           AGENTS + docs-map + seçili ajan uyarlaması
                                      ↓
                        skills + prompts + testler → uygulama
```

Bir gereksinim değiştiğinde etkilenen tasarım, görev, test ve yönerge birlikte gözden geçirilir. Her dosyayı aynı uzun özeti taşıyan bağımsız metin olarak üretmek çelişki riskini artırır. Ortak karar tek yerde tutulur, diğer dosyalar onu açıkça kaynak gösterir.

## Araştırma ekleriyle genişleyen dosyalar

| Dosya | Görev ve üretim sırası |
|---|---|
| `docs/traceability.md` | U02 gereksinim bağlarını başlatır; U03–U06 belge ve görev bağlarını, U11 gerçek kod/test bağlarını günceller. |
| `evals/ax-cases.json`, `docs/ax-review.md` | U07 belge/araç keşfi ve görev başarısını ayırır; U08, U18 ve U33 ilgili gözlemleri ekler. |
| `docs/skill-compatibility.md` | U08 biçim, keşif, çağırma, davranış ve izin ayrımını kurar; U33 dağıtım deneyini ekler. |
| `skills/pusula-belge-uret/references/belge-iliskileri.md` | U08 skill paketinin iç başvurusunu üretir; uygulama kökünün kendisi değildir. |
| `policies/delegation.yaml` | U17 görev yetkisinin kapsamını üretir; U28 ve U32 kimlik/devir ve sahiplik incelemesinde kullanır. |
| `policies/autonomy-budget.yaml` | U19 bütçe sınırlarını üretir; U20 yürütücüye bağlar, U25 ihlal durumunu sınar. |
| `evals/trajectory-cases.json` | U24 izinli alternatif yolları ve hatalı işlem izlerini tanımlar; U30 hizmet ölçümüne bağlar. |
| `datasets/provenance.json` | U24 veri kökeni ve ayrımını başlatır; U30 iz kökenini günceller, U35 eğitim adayı uygunluğunu inceler. |
| `evals/routing-comparison.json` | U29 aynı görev setinde sabit model ve adım bazında yönlendirmeyi karşılaştırır. |

Bu dosyalar okurun proje çıktılarıdır. Companion içinde adlarının bulunması, üretildikleri veya herhangi bir araç tarafından kendiliğinden okundukları anlamına gelmez. Yeni bağımlılıkların ilk üretimi müfredatta tüketildikleri adımdan önce gelir.

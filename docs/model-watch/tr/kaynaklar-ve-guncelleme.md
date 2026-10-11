# Model Watch | Kaynaklar, kanıt düzeyleri ve güncelleme standardı

**Sürüm:** 2026-10 · **İlk kapsamlı doğrulama:** 11 Ekim 2026 · **Denetim:** Belge ve model kartı incelemesi. **Canlı API ile çağrı gönderilip sürüm/fiyat/hız ölçülmedi.**

## Neyi “doğrulandı” sayarız?

Yapay zekâ alanında model adı bir haberden habere değişebilir. Bu nedenle kaynaklara farklı kanıt düzeyleri uygularız:

| Etiket | Açıklama | Nerede kullanılabilir? |
|---|---|---|
| **R1 — Resmî, güncel** | Sağlayıcının güncel API model listesi, model kartı, fiyat, kapanış tablosu, lisans metni | Tarih ve bağlantıyla teknik kayıt |
| **R2 — Resmî duyuru** | Üreticinin blogu veya changelog'unda yayımlanmış değişiklik | Tarihli duyuru; kapsam/GA ayrıca belirtilir |
| **R3 — Bağımsız ölçüm** | Yöntemi açık, yeniden üretilebilir benchmark veya proje içi test | Yalnızca ölçtüğü görev ve koşullarda kıyas |
| **R4 — Üçüncü taraf haber/topluluk** | Basın, forum, GitHub issue, karşılaştırma sitesi | İzleme ipucu; resmî bilgi yerine geçmez |
| **B — Belirsiz / çelişkili** | Eski ve yeni kaynaklar uyuşmuyor, endpoint başka sürüme yönleniyor | Kesin hüküm yok; açık takip maddesi |
| **T — Test edilmedi** | Kaynakta iddia var ama bizim API testimiz yok | “Belgede belirtiliyor”; “ölçtük” denmez |

**Terim kuralı:** “Doğrulama tarihi” bizim kaynak taramamızın tarihidir; “model yayını”, “GA”, “snapshot”, “ağırlık yayını” ve “API açılışı” ayrı tarihler olabilir.

## Birincil kaynak dizini

Aşağıdaki bağlantılar model ailesinin ve ilgili sürüm bilgisinin izlenmesi içindir; her sayfa mutlaka aynı gün güncellenmiş anlamına gelmez.

### Küresel sağlayıcılar

| Sağlayıcı | Resmî API/model kaynağı | Duyuru / kapanış / ek belge |
|---|---|---|
| OpenAI | [Model dizini](https://developers.openai.com/api/docs/models/all) | [Değişiklik günlüğü](https://developers.openai.com/api/docs/changelog) |
| Anthropic | [Model karşılaştırması](https://platform.claude.com/docs/en/models/overview) | [Model kartları](https://platform.claude.com/docs/en/resources/overview) |
| Google Gemini | [Model listesi](https://ai.google.dev/gemini-api/docs/models) | [Kullanımdan kaldırma takvimi](https://ai.google.dev/gemini-api/docs/deprecations/) |
| Google Gemma | [Gemma dokümantasyonu](https://ai.google.dev/gemma) | Sürüme özgü model kartı / lisans |
| xAI / SpaceXAI | [API modelleri](https://docs.x.ai/developers/models) | [Eski model geçişi](https://docs.x.ai/developers/migration/may-15-retirement) |
| Meta | [Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api) | [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) |
| Mistral | [Model kataloğu](https://docs.mistral.ai/models/) | [Large 4 duyurusu](https://mistral.ai/news/mistral-large-4/) |

### Çinli sağlayıcılar

| Sağlayıcı | Resmî / birincil kaynak | Özellikle kontrol edilen konu |
|---|---|---|
| Alibaba Qwen | [Model Studio listesi](https://www.alibabacloud.com/help/en/model-studio/models) | Max/Flash/API, bölge, snapshot |
| Qwen ağırlıklar | [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [2.4T](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) | Apache 2.0 ile özel lisansı ayırma |
| DeepSeek | [API güncellemeleri](https://api-docs.deepseek.com/updates/) | Eski alias, V4-Pro durumu, V4.1-Flash |
| DeepSeek | [Güncel başlangıç ve fiyat notları](https://api-docs.deepseek.com/quick_start/pricing-details-cny/) | Eski duyuruyla çelişen yönlendirme notları |
| Z.ai GLM | [Resmî depo](https://github.com/zai-org/GLM-5) | GLM 5.3 / Flash modelleri |
| GLM 5.3 | [Model kartı + lisans](https://huggingface.co/zai-org/GLM-5.3) | `glm-5.3` özel koşullar |
| Moonshot Kimi | [Resmî duyurular](https://forum.moonshot.ai/c/announcement/5) | K3 genel erişim, API/abonelik |
| Kimi K3 | [Model kartı + lisans](https://huggingface.co/moonshotai/Kimi-K3) | Ticari kullanım şartları |
| MiniMax | [Token/API planları](https://platform.minimax.io/subscribe/token-plan) | Önbellek, token ve abonelik farkı |
| MiniMax M3 | [Model kartı + lisans](https://huggingface.co/MiniMaxAI/MiniMax-M3) | Community lisansı |
| ByteDance | [Volcengine API belgeleri](https://docs.volcengine.com/docs/82379/1359497?lang=en) | Seed 2.1 kimlikleri |
| Baidu | [AI Studio model listesi](https://ai.baidu.com/ai-doc/AISTUDIO/Mmhslv9lf) | ERNIE model ve bağlam verileri |
| Tencent | [Hunyuan geçiş notları](https://cloud.tencent.com/document/product/1729/131925) | TokenHub geçişi / eski model kapanışı |
| Xiaomi | [XiaomiMiMo](https://github.com/XiaomiMiMo) | MiMo model kodu ve barındırma |

### Ölçüm ve alan araştırmaları

- [SWE-bench](https://www.swebench.com/), [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro), [Terminal-Bench](https://www.tbench.ai/) — Kod üretimi/ajan görevleri. Aynı benchmark sürümü ve aynı harness olmadan kıyas yapılamaz.
- [Artificial Analysis](https://artificialanalysis.ai/) — Fiyat, hız ve çok boyutlu model verileri; tarihli snapshot alınır.
- [DORA](https://dora.dev/research/) — Yazılım geliştirme verimliliği; tek bir modelin üstünlüğünü ispatlamak için kullanılmaz.
- [Hugging Face model kartları](https://huggingface.co/models) — Ağırlık, lisans ve kullanım bilgisi; yükleyen hesabın resmî geliştiriciye ait olduğundan emin olunur.

## Güncelleme kaydı nasıl tutulur?

Her değişiklik önerisinde mümkünse aşağıdakiler yer almalı:

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

## Katkı ve doğrulama akışı

1. **Araştır:** Resmî duyuruyu, API model listesini ve varsa model kartını bul.
2. **Ayır:** Model kimliği, ürün adı, API erişimi, tarihli snapshot, lisans ve bölgeleri birbirine karıştırma.
3. **Karşılaştır:** Önceki kayıtla diff oluştur. Birbiriyle çelişen kaynakların **tarihini** kontrol et.
4. **Sınırla:** Bağımsız test yoksa pazarlama benchmark'ından sonuç türetme; “şirketin kendi ölçümüne göre” yaz.
5. **Doğrula:** Tüm Markdown bağlantıları, göreli yollar, tarih notları, iddialar ve gözlemevi tablosu incelensin.
6. **Test et:** Canlı API erişimi ve açık izin varsa ilgili lab regresyon testleri. Erişim yoksa `not-run` olarak yaz.
7. **İnceleme:** AGENTS.md terminal state ve insan review kuralı geçerlidir.
8. **Yayımla:** Değişiklik günlüğüne tarih, kapsam ve takipte kalan belirsizlikler ekle.

## İngilizce sürüm standardı

İleride eklenecek `docs/model-watch/en/`, Türkçe dosyaların **tarih ve kaynak kontrollü bir uyarlaması** olacak. Kaynak URL'leri, API model kimlikleri ve sayısal veriler çeviride değişmeyecek. İngilizce metin kendi `last_verified` tarihini taşıyacak; Türkçeye eklenen model İngilizce sürüme otomatik eklenmiş sayılmayacak.

## Öncelikli takip işleri

| Konu | Neden takipte? | Tamamlanma koşulu |
|---|---|---|
| Mistral Large 4 ağırlıkları | 11 Ekim itibarıyla son Ekim için plan | Resmî model kartı ve indirilebilir dosyanın doğrulanması |
| DeepSeek V4-Pro yönlendirmesi | Eski duyuru ile yeni destek notu farklı | Gerçek API yanıt model kimliği, fiyat ve tarihli güncel destek belgesi |
| Grok 4.7 model/kota değişimi | Yeni API seçeneği | Model kartı + üretim testi |
| Qwen3.8 aile içi lisanslar | Her model boyutu aynı değil | Her ağırlık repo'sunun tam lisans metni |
| GLM 5.3 / Kimi K3 / MiniMax M3 ticari lisansları | Custom license koşulları | Ticari kullanım incelemesi ve gerekirse izin |
| Claude/OpenAI/Google yeni varsayılanları | Kullanıcı uygulaması ve API farklı | Tarihli istemci/model kimliği üzerinden doğrulama |
| Türkçe kalite test seti | Model iddiaları projeye özgü değil | Kör değerlendirilen ve sürümlenen fixture seti |

**Temel duruş:** Gözlemevi güncel bilgi verir; yayımlanmamış sonuç üretmez. Bilmiyorsak “doğrulanamadı” yazarız.

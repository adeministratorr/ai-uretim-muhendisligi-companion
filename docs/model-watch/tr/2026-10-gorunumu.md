# Ekim 2026 | Yapay zekâ modellerinde güncel görünüm

**Kaynak kontrolü:** 11.10.2026 · **Kapsam:** Resmî model listeleri, ürün duyuruları ve model kartları · **Doğrulama türü:** Masa başı kaynak incelemesi; API çalıştırma, hız ve maliyet ölçümü yapılmadı.

> **Bu sayfa bir liderlik tablosu değildir.** Marka tanıtımı veya laboratuvar benchmark'ı, bizim projelerimizde ölçülmüş başarı anlamına gelmez. Her satır bir başlangıç noktasıdır; seçim için [değerlendirme yöntemi](model-secimi-ve-olcum.md) kullanılır.

## Ekim ayında ne değişti?

1. **OpenAI — GPT-6 ailesi:** API kataloğunda `gpt-6-astra`, `gpt-6.1-sol` ve `gpt-6-luna` farklı iş yüklerine hitap ediyor. 29 Eylül'de GPT-6.1 Sol duyuruldu; 8 Ekim'de Responses API'de `ultrafast` hizmet katmanı eklendi. Bu özellik normal hız/fiyat varsayımıyla karıştırılmamalı. [Model kataloğu](https://developers.openai.com/api/docs/models/all) · [Değişiklik günlüğü](https://developers.openai.com/api/docs/changelog)
2. **Anthropic — Claude 5.5:** Güncel resmi karşılaştırmada **Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5** yer alıyor. En güçlü modelin her görevde en iyi maliyet/sonuç dengesini sunacağı varsayılmamalı. [Model karşılaştırması](https://platform.claude.com/docs/en/models/overview)
3. **Google — Gemini 3.8 Flash:** `gemini-3.8-flash` GA; 1.048.576 giriş ve 65.536 çıkış token sınırı belgelendi. Sesli modeller ve önizlemedeki Pro ailesi ayrı değerlendirilir. [Model kartı](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Kapanış takvimi](https://ai.google.dev/gemini-api/docs/deprecations/)
4. **xAI — Grok 4.7:** Güncel API model sayfasının öne çıkardığı sürüm; **500 bin token bağlam** ve resmî listede **1M giriş $2, çıkış $6** tarifesi var. Grok'un sosyal ağdan güncel bilgiyi kendiliğinden bildiği düşünülmemeli: canlı bilgi için arama araçları etkinleştirilmeli. [xAI modelleri](https://docs.x.ai/developers/models)
5. **Mistral — Large 4 önizleme:** **6 Ekim 2026** duyuruldu. API önizlemesi erişilebilir; açık ağırlık dosyalarının yayımlanması ekim sonu için planlanıyor. **11 Ekim itibarıyla ağırlıklar yayımlandı denemez.** Large 3 ayrı, mevcut açık ağırlık seçeneğidir. [Duyuru](https://mistral.ai/news/mistral-large-4/) · [Large 3 kartı](https://docs.mistral.ai/models/mistral-large-3-25-12)
6. **Meta — Muse Spark 1.1:** **9 Temmuz** duyurulan model için Meta Model API önizlemesi açıklandı. Muse ile Llama aynı şey değil: Muse erişim hizmeti, Llama 4 ise indirilebilir ağırlıkları bulunan farklı bir model ailesi. [Muse 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api) · [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
7. **Alibaba — Qwen 3.8:** Güncel Model Studio listesinde `qwen3.8-max`, `qwen3.8-flash`; ayrıca 27B ve 2.4T-A95B gibi ağırlık seçenekleri bulunuyor. **Qwen3.8-27B Apache 2.0**, **2.4T-A95B özel Qwen3.8-Max lisansı** taşıyor: aynı ailede lisans bile farklı olabilir. [Model Studio](https://www.alibabacloud.com/help/en/model-studio/models) · [27B kartı](https://huggingface.co/Qwen/Qwen3.8-27B) · [2.4T kartı](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)
8. **DeepSeek — V4.1 Flash:** **10 Eylül** duyurulan `deepseek-flash` / V4.1-Flash, önceki V4-Flash sürümlerinin yerini aldı. Resmî ilk duyuru V4-Pro isteklerinin 14 Eylül'de yönlendirileceğini söylemişti; daha güncel fiyat/başlangıç sayfası **`deepseek-v4-pro` kimliğini kullanılabilir modeller arasında listeliyor**. **Son durum için çağrının çözümlendiği gerçek sürüm ve hesap dökümü kontrol edilmeli.** [Duyuru](https://api-docs.deepseek.com/news/news260910/) · [Güncel başlangıç sayfası](https://api-docs.deepseek.com/quick_start/pricing-details-cny/)
9. **Z.ai — GLM 5.3 ve 5.3 Flash:** 5.3 için **14 Ağustos** tarihli resmî duyuru bulunuyor. Ağırlıklar paylaşılmış olsa da 5.3'ün kendine ait lisansı vardır; 5.3-Flash ile aynı izinlere sahip kabul edilmemeli. [Duyuru](https://z.ai/blog/glm-5.3) · [Proje](https://github.com/zai-org/GLM-5) · [Model lisansı](https://huggingface.co/zai-org/GLM-5.3)
10. **Moonshot — Kimi K3:** **22 Temmuz** duyuruldu; model ağırlıkları mevcut ve **Kimi K3 lisansının** özellikle büyük ölçekli ticari hizmetler için ek koşulları var. API aboneliği ile tüketici üyeliği aynı erişim biçimi değildir. [Duyurular](https://forum.moonshot.ai/c/announcement/5) · [Ağırlıklar ve lisans](https://huggingface.co/moonshotai/Kimi-K3)
11. **MiniMax — M3:** Model ağırlıkları, API ve 1M bağlamla pazarlanan planlar mevcut. **MiniMax Community License** ticari uygulamalar için görünür atıf/bildirim ve belirli ölçekte izin şartları içeriyor; Apache/MIT gibi yazılmamalı. [Model](https://huggingface.co/MiniMaxAI/MiniMax-M3) · [Planlar](https://platform.minimax.io/subscribe/token-plan)

## Hızlı referans: Hangi model ailesine neden bakıyoruz?

| Aile / temsilci | İlgi alanı | Erişim / durum | Önemli kayıt |
|---|---|---|---|
| OpenAI GPT-6.1 Sol / Astra / Luna | Kod, ajan, yoğun üretim, hafif sınıflandırma | API | Ürün planı ve API yetenekleri farklı |
| Claude Opus/Sonnet/Haiku 5.5, Fable 5.1 | Uzun görev, kod ve ajan, maliyet dengesi | API / ürün | Fiyatı ve token tüketimini ölç |
| Gemini 3.8 Flash / 3.1 Pro Preview | Çok biçimli girdi, uzun bağlam, araçlar | Flash GA / Pro önizleme | Preview için geçiş planı tut |
| Grok 4.7 | Kod, araç çağrısı, genel görevler | API | Canlı veri için web/X araçları şart |
| Meta Muse Spark 1.1 / Llama 4 | Uygulama API'si / açık ağırlık değerlendirmesi | Ayrı ürün hatları | Muse ağırlıklarını Llama sanma |
| Mistral Large 4 / Large 3 | Avrupa odaklı API ve self-host stratejisi | L4 önizleme / L3 açık ağırlık | L4 ağırlıklarını duyuruya göre izle |
| Qwen 3.8 | Çin ve küresel API, güçlü yerel seçenekler | API + seçili açık ağırlıklar | Model boyutuna göre lisans farklı |
| DeepSeek V4.1-Flash / V4-Pro | Maliyet duyarlılığı, uzun bağlam, kod | API + ağırlıklar | Alias yönlendirmesini test et |
| GLM 5.3 / Flash | Kodlama, uzun ajan görevleri, self-host | API + ağırlıklar | Özel lisans / altyapı |
| Kimi K3 | Multimodal ve uzun bağlam ajanları | API + ağırlıklar | Ayrı ticari lisans koşulları |
| MiniMax M3 | Kod, çok biçimli girdi, uzun bağlam | API + ağırlıklar | Community lisansına bak |
| Doubao Seed 2.1 | Çin bulut ekosistemi, çeşitli gecikme katmanları | Volcengine API | Bölgesel erişim ve sürüm kimliği |
| ERNIE 5.1 / Hunyuan / MiMo 2.5 | Alternatif Çin bulut/yerel modelleri | Sağlayıcıya bağlı | Dağıtım ve sürüm durumu ayrı doğrulanmalı |

## Karar verirken

Önce görevi tanımlayın: Türkçe belge hazırlama, kod tabanında hata düzeltme, görsel okuma, birden fazla araçla ajan yürütme veya yüksek hacimli sınıflandırma. Ardından **aynı veri, aynı araç izni, aynı testler** ile iki ya da üç aday ölçün. Fiyat etiketlerini tek başına değil, *başarılı görev başına toplam maliyet* olarak karşılaştırın. Bir model değişikliği mutlaka kontrol edilebilir olmalı.

Devam: [Çinli modeller](cinli-modeller.md) · [Küresel modeller](kuresel-modeller.md) · [Değerlendirme](model-secimi-ve-olcum.md) · [Geçişler](gecis-ve-uyumluluk.md).

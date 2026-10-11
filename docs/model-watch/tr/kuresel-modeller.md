# Küresel model ekosistemi | Model adının ötesine bakmak

**[Türkçe](../tr/kuresel-modeller.md) · [English](../en/kuresel-modeller.md)** · [Model Watch](../README.md)

**Kaynak kontrolü:** 11 Ekim 2026. Aşağıdaki bilgiler sağlayıcı duyuruları ve model kartlarına dayanır; bağımsız performans ölçümü değildir. Fiyatlar, erişim ve hizmet bölgeleri değişebilir.

## 1. OpenAI — GPT-6, Codex ve çok biçimli servisler

| Model / ürün | Belgedeki konum | Nerede değerlendirilmeli? |
|---|---|---|
| **GPT-6 Astra** | API kataloğunda en yetenekli ana model | Zor muhakeme ve yüksek riskli, testle doğrulanabilen görevler |
| **GPT-6.1 Sol** (`gpt-6.1-sol`) | Karmaşık kod ve profesyonel işlerde maliyet/başarı dengesi | Kod ajanları, karmaşık araç akışları, bilgisayar kullanımı |
| **GPT-6 Luna** | Yüksek hacimli, odaklı görevler | Sınıflandırma, kısa veri dönüştürme, ekonomik yönlendirme |
| **GPT-6 Sol** | Önceki Sol sürümü | Var olan sistemlerde karşılaştırma/geri dönüş |
| **GPT-Image ve ses modelleri** | Metinden farklı girdi/çıktı türlerine ayrılmış servisler | Görsel üretim, düzenleme, konuşma, transcription |

**Doğrulanmış değişiklikler:** GPT-6.1 Sol 29 Eylül 2026'da duyuruldu; 8 Ekim'de `service_tier: "ultrafast"` seçenek olarak eklendi. Model kartında yaklaşık **1,05M token bağlam** belirtiliyor. Ultrafast'ın daha hızlı olduğu söylenebilir ancak **bu depoda ölçülmüş p95 gecikme değeri bulunmuyor**. Reasoning effort ayarları, Responses API araç çağrısı desteği ve Chat Completions farkı modele göre kontrol edilmeli.

**Geliştirici notu:** ChatGPT aboneliği, Codex'te seçili model ve API'de kullanılabilen `model` kimliği aynı kavram değildir. “Şu an Codex'in varsayılanı…” ifadesi istemci sürümü, tarih ve ayar olmadan genellenmez. `chat-latest` gibi değişken alias'lar da sabit model sürümü sayılmaz.

**Resmî kaynak:** [Tüm modeller](https://developers.openai.com/api/docs/models/all) · [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) · [API değişiklikleri](https://developers.openai.com/api/docs/changelog).

## 2. Anthropic — Claude ailesi

Anthropic'in güncel model karşılaştırma sayfasında **Claude Fable 5.1**, **Opus 5.5**, **Sonnet 5.5**, **Haiku 5.5** yer alıyor. Bu adlar farklı kullanım katmanlarını gösteriyor:

| Aile | Tipik seçim nedeni | Test edilmesi gereken |
|---|---|---|
| Fable 5.1 | En zorlu uzun-ufuklu reasoning/ajan işleri | Maliyet ve bağımsız başarım farkı |
| Opus 5.5 | Ağır kodlama, araştırma ve bilgi işleri | Bütçe/kalite dengesi, görevde kalma |
| Sonnet 5.5 | Genel kod ve agent işleri için denge | Karmaşık görevde tekrar sayısı |
| Haiku 5.5 | Hacimli, gecikmeye duyarlı işler | Şema hatası ve yanlış güven |

**Ürün/API farkı:** Claude Code, Claude uygulaması ve Anthropic Messages API'nin varsayılan modeli aynı olmak zorunda değildir. AWS, Google Cloud ve Microsoft dağıtımlarında kimlik, bölge ve erişim farkları olabilir. “Adaptive thinking”, tool-use, prompt caching gibi özellikler her sürümde ayrıca belgelenir.

**Kaynak:** [Claude model karşılaştırması](https://platform.claude.com/docs/en/models/overview) · [Model kartları](https://platform.claude.com/docs/en/resources/overview) · [Kullanımdan kaldırmalar](https://docs.anthropic.com/en/docs/about-claude/model-deprecations).

## 3. Google — Gemini, Gemma ve özel modeller

**Gemini 3.8 Flash** (`gemini-3.8-flash`) **GA**: 1.048.576 token giriş, 65.536 token çıkış, `low/medium/high` thinking, function calling ve structured output belgelendi. Google'ın model dizininde **Gemini 3.7 Flash**, **3.6 Flash**, **3.5 Flash-Lite** ve **3.1 Pro Preview** gibi başka seçenekler de bulunuyor.

- **Gemini 3.8 Flash:** Uzun dokümanlar, görsel/işitsel girdi, kod ve araç zincirleri için denenebilir. Üretimde modelin desteklediği aracı ve bölgesel kotayı kesinleştirin.
- **Gemini 3.1 Pro Preview:** Genel ve karmaşık ajan işlerinde ayrı aday; *preview* yaşam döngüsü taşır. “3.8” sayısı daha büyük diye her kullanımda Pro'dan üstün ilan edilmemeli.
- **Gemini 3.8 Live / Live Extended Thinking:** Gerçek zamanlı ses diyaloğu; metin modelinden farklı kapasite ve API kısıtları vardır.
- **Gemma:** Google'ın indirilebilir ağırlıklara sahip ailesi; Gemma 4 gibi sürümlerin her boyutu için lisans, quantization ve çalıştırma desteği model kartından okunmalı.
- **Görsel üretim / ses / embedding:** Nano Banana, TTS ve embedding modelleri genel sohbet modelinin sütununda karşılaştırılmamalı; başarı ölçütleri farklıdır.

**Kaynak:** [Gemini model listesi](https://ai.google.dev/gemini-api/docs/models) · [Gemini 3.8 Flash kartı](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Kapanış ve yerine geçiş](https://ai.google.dev/gemini-api/docs/deprecations/) · [Gemma](https://ai.google.dev/gemma).

## 4. xAI / SpaceXAI — Grok

Güncel resmî model sayfası **Grok 4.7** (`grok-4.7`) modelini kodlama, araç çağrısı ve genel kullanım için öne çıkarıyor. **500k bağlam**, API sayfasında **$2 / 1M giriş ve $6 / 1M çıkış** fiyatı belirtiliyor; token aralığı, bölge ve diğer hizmet bedelleri ayrıca kontrol edilmeli. **Grok 4.5** de model kartıyla belgeli önceki sürümdür.

**Yanlış varsayım:** Grok'un X ile aynı ekosistemde olması, gerçek zamanlı olayları her istekte otomatik bildiği anlamına gelmiyor. Sağlayıcı açıkça Web Search / X Search araçlarının etkinleştirilmesi gerektiğini yazıyor. Arama aracına erişim, uygulamanın doğru kaynak kullandığını garanti etmez; kaynak denetimi yine gerekir.

**Göç notu:** Eski `grok-4-1-fast-*`, `grok-3`, `grok-code-fast-1` gibi kimliklerin 15 Mayıs 2026'daki emeklilik notunda Grok 4.3'e otomatik yönlendirildiği açıklanmıştı. İstek hata vermese bile sonuç ve fatura değişebilir. Alias mutlaka test edilmeli.

**Kaynak:** [Grok model dizini](https://docs.x.ai/developers/models) · [Grok 4.5 kartı](https://docs.x.ai/developers/models/grok-4.5) · [Eski modellerin geçişi](https://docs.x.ai/developers/migration/may-15-retirement).

## 5. Meta AI / Llama — İki farklı strateji

**Meta AI'deki Muse ile indirilebilir Llama aynı model değildir.**

- **Muse Spark (8 Nisan 2026):** Meta'nın çok biçimli reasoning ve araç kullanımına odaklanan yeni ailesi, başlangıçta meta.ai ve uygulamada kullanıma açıldı.
- **Muse Spark 1.1 (9 Temmuz 2026):** Kodlama, computer use ve multimodal geliştirmeleriyle sunuldu; Meta Model API için kamuya açık önizleme duyuruldu. Bunun **Llama ağırlıklarıyla aynı erişim biçiminde** olduğunu ileri sürmeyin.
- **Llama 4 Scout / Maverick (2025):** İndirilebilir ağırlıklı model ailesi; lisans koşulları, kullanım sınırları ve veri işleme tasarımı ayrıca okunur. **Llama 4 Behemoth** ilk duyuruda henüz eğitim aşamasında anlatılıyordu; duyurulmuş bir modelin otomatik GA olduğu kabul edilemez.
- **Muse Image / Muse Video:** Metin-odaklı model kıyaslamasına karıştırılmayacak görsel/video ürün hattı.

**İzlenecek soru:** Meta'nın kapalı Muse hattı gelişirken Llama ağırlıklarına ilişkin yayımlama, güncelleme ve lisans stratejisi nasıl değişiyor? Yanıt spekülasyonla değil yeni birincil duyuruyla verilir.

**Kaynak:** [Muse Spark](https://ai.meta.com/blog/introducing-muse-spark-1-msl/) · [Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api) · [Llama 4](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) · [Muse Image/Video](https://ai.meta.com/blog/introducing-muse-image-muse-video-msl).

## 6. Mistral AI — Large 4, Large 3 ve uzman modeller

**Mistral Large 4**, **6 Ekim 2026** tarihli duyuruda kamuya açık API önizlemesiyle tanıtıldı. Şirket modelin **1 trilyon toplam / 52 milyar etkin parametreye** sahip multimodal MoE olduğunu açıkladı. Model ağırlıklarının **Ekim 2026 sonunda yayımlanması planlanıyor**. 11 Ekim'de yayımlanmış ağırlık gibi yazmak doğru olmaz.

**Mistral Large 3** ise ayrı bir modeldir: resmî kartında **675B toplam / 41B etkin, 256k bağlam ve Apache 2.0** bilgileri var. Uzman modeller (OCR, belge işleme, güvenlik, kod veya robotik) genel LLM sıralamasına sırf aynı markayı taşıyor diye eklenmez.

**Avrupa odaklı karar:** Egemenlik, kurum içi barındırma, çok dillilik ve veri yerleşimi önemliyse Mistral mutlaka incelenmeli. Ancak “Avrupa şirketi = otomatik GDPR/KVKK uygunluğu” çıkarımı doğru değildir; sözleşme, işlem bölgesi ve log politikası incelenir.

**Kaynak:** [Large 4 duyurusu](https://mistral.ai/news/mistral-large-4/) · [Large 3 kartı](https://docs.mistral.ai/models/mistral-large-3-25-12) · [Güncel duyurular](https://mistral.ai/news/).

## 7. Diğer önemli sağlayıcılar: izleme listesi

Aşağıdakiler daha geniş pazar/ürün çalışmaları için düzenli izlenecek, fakat **bu sürümde son model, fiyat ve benchmark iddiası atanmayan** sağlayıcılardır:

| Ekosistem | Neyi izleyeceğiz? | İlk kaynak |
|---|---|---|
| Cohere / Command | Kurumsal RAG, rerank, özel dağıtım | https://docs.cohere.com/ |
| AI21 Labs / Jamba | Uzun bağlam, veri akışı, kurumsal API | https://docs.ai21.com/ |
| IBM / Granite | Açık ağırlık, yönetişim, kurumsal kullanım | https://www.ibm.com/granite |
| NVIDIA / Nemotron | Açık modeller, veri seti ve dağıtım sistemleri | https://developer.nvidia.com/nemotron |
| Microsoft / Phi | Küçük ve cihaz üzerinde çalışan modeller | https://huggingface.co/microsoft |
| Amazon / Nova | AWS tabanlı multimodal/kurumsal çalışma | https://docs.aws.amazon.com/nova/ |
| Stability AI, Black Forest Labs | Görsel üretim ve düzenleme | https://stability.ai/ · https://blackforestlabs.ai/ |
| Runway, Luma, Kling, Pika | Video üretimi ve yaratıcı iş akışları | Sağlayıcının resmî geliştirici sayfası |

**Not:** Bu listenin bulunması her sağlayıcı için Ekim 2026 model doğrulaması yapıldığı anlamına gelmez.

## Sonuç: marka değil, görev başarısı

Kod tabanı onarımı ile 100 bin kısa müşteri mesajının sınıflandırılması aynı model seçimini gerektirmez. Bir model açıklamada çok güçlü görünebilir; buna rağmen bizim Türkçe yazım testimizde doğal dil akışını bozabilir, beklenmedik araç çağrısı yapabilir veya gereksiz token tüketebilir. Bu depo, pazarlama cümlesini değil **kanıtlanmış iş sonucunu** merkeze alır.

Devam: [Çinli modeller](cinli-modeller.md) · [Nasıl ölçeceğiz?](model-secimi-ve-olcum.md).

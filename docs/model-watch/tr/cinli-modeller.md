# Çinli yapay zekâ modelleri | Tek bir listeye sığmayan ekosistem

**[Türkçe](../tr/cinli-modeller.md) · [English](../en/cinli-modeller.md)** · [Model Watch](../README.md)

**Kaynak kontrolü:** 11 Ekim 2026 · **Not:** Çinli şirketlerin sunduğu modeller tek bir erişim, lisans veya performans standardına sahip değildir. Aynı şirketin açık ağırlıklı bir modeli ile kapalı bulut API'si yan yana bulunabilir. Bölge, kota, ödeme ve veri işleme şartları ayrıca denetlenir.

Çinli modelleri yalnızca “daha ucuz alternatifler” diye görmek eksik olur. Qwen, DeepSeek, GLM, Kimi ve MiniMax uzun görevler, kodlama, çok biçimli girdiler ve büyük bağlam alanlarında ciddi seçenekler sunuyor. Öte yandan büyük model ağırlığını indirmek, sıradan bir dizüstü bilgisayarda sorunsuz çalıştırmak anlamına gelmez. **Toplam parametre**, **etkin parametre**, **bellek gereksinimi** ve **çıkarım altyapısı** birlikte değerlendirilir.

## Özet harita

| Geliştirici | İzlenecek aile | Kullanım odağı | API / ağırlık / lisans kontrolü |
|---|---|---|---|
| **Alibaba / Qwen** | Qwen3.8 Max, Flash, 27B, 2.4T-A95B; 3.7/3.6 | Kod, ajan, çok biçimli girdi, yerel dağıtım | Alibaba Model Studio + her Hugging Face kartı |
| **DeepSeek** | V4.1-Flash, V4-Pro | Kod, reasoning, uzun bağlam, düşük maliyet arayışı | Resmî API kimliği ve yönlendirme |
| **Z.ai / Zhipu** | GLM-5.3, GLM-5.3-Flash, 5.2 | Uzun görev, agentic coding | Özel GLM-5.3 lisansını ayrıca oku |
| **Moonshot** | Kimi K3, K2.7 Code | Multimodal, çok adımlı görev, kod | Kimi K3 License; API/ürün erişimi |
| **MiniMax** | MiniMax M3, M2.7 | Kod, multimodal, ajan iş akışları | Community License, ticari şartlar |
| **ByteDance / Doubao** | Seed 2.1 Pro/Lite/Turbo | Çin bulut platformu ve çeşitli görev maliyetleri | Volcengine model kimlikleri, bölge |
| **Baidu** | ERNIE 5.1, 5.0 | Çin dili ve kurumsal uygulama | AI Studio ve ürün bölgesel erişimi |
| **Tencent** | Hunyuan / HY3 | İçerik, çok biçimli iş akışları, kurumsal API | Eski Hunyuan'dan TokenHub geçişi |
| **Xiaomi** | MiMo V2.5 | Yazılım/ajan ve multimodal araştırmaları | Resmî repo/model kartı, barındırıcı |
| **Huawei** | Pangu / Ascend ekosistemi | Sektörel / yerel altyapı | Bulut ve donanım erişimi ayrı |

Bu tablo **performans sıralaması değildir**. Belirli model kimliği ve lisans bilgileri sonraki başlıklarda kaynaklıdır.

## 1. Alibaba — Qwen

**Ekim 2026'da izlenecek ana aile Qwen 3.8.** Alibaba Cloud Model Studio `qwen3.8-max` ve `qwen3.8-flash` kimliklerini belgeliyor. 3.7 Plus, Max ve Flash; 3.6 ve 3.5 serileri de mevcut uygulamalarda karşımıza çıkabilir. Varsayılan model adının hangi sürüme yönlendiği ayrıca izlenmelidir.

| Seçenek | Ne ifade ediyor? | Dikkat |
|---|---|---|
| `qwen3.8-max` | Bulutta güçlü genel/ajan görevleri | Ürün ve bölgeye göre fiyat/kota |
| `qwen3.8-flash` | Yüksek hacimli, hız/maliyet odaklı seçim | Flash etiketi her görevde daha doğru demek değil |
| `Qwen/Qwen3.8-27B` | İndirilebilir **27B**, model kartında **Apache 2.0** | Quantization, GPU/RAM ve multimodal desteğini yerelde ölç |
| `Qwen/Qwen3.8-2.4T-A95B` | Çok büyük açık ağırlıklı MoE seçeneği | **Özel `qwen3.8-max` lisansı**; yerel barındırma pahalı |
| Qwen3.7 Max / Plus / Flash | Daha önceki projelerin izlenecek sürümleri | 3.7 Max'in tarihli snapshot'ları aynı modaliteyi desteklemeyebilir |

**Kaynak:** [Model Studio genel listesi](https://www.alibabacloud.com/help/en/model-studio/models), [Qwen metin model kimlikleri](https://help.aliyun.com/zh/model-studio/text-generation-model), [3.7 Max ayrıntısı](https://help.aliyun.com/en/model-studio/qwen3-7-max), [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B).

**Üretim notu:** 1M bağlam ve tool calling desteğinin bulunması bir başlangıçtır. `qwen3.8-max` ile tarihli snapshot'ın giriş modalitesi veya bölgesel uyumluluğu farklı olabilir. Özellikle ekran görüntüsünden kod üretme ve GUI etkileşimi için doğru uç nokta seçilmelidir.

## 2. DeepSeek — V4 ve V4.1

DeepSeek'in Nisan 2026 V4 önizlemesi, Ağustos'ta V4-Pro GA duyurusu ve Eylül'de V4.1-Flash geçişi ayrı kilometre taşlarıdır. Bu tarihler birbirinin yerine geçmez.

- **24 Nisan:** V4-Pro (1,6T toplam / 49B etkin) ve V4-Flash (284B / 13B etkin) duyuruldu; model ağırlıkları paylaşıldı, 1M bağlam desteklendi.
- **13 Ağustos:** V4-Pro kararlı sürüm duyuruldu; Responses API ve ajan akışları öne çıkarıldı.
- **10 Eylül:** Yeni V4.1-Flash duyuruldu; resmî API model adı `deepseek-flash`. Önceki `deepseek-v4-flash` isteklerinin V4.1'e yönlendirildiği açıklandı.
- **V4-Pro durumu:** Eylül duyurusunda 14 Eylül için yönlendirme planı anlatılsa da DeepSeek'in daha sonra güncellenmiş başlangıç/fiyat sayfası, `deepseek-v4-pro` kimliğini kullanılabilir modeller arasında listeliyor. **Bu çelişki güncel belgeler ışığında açıkça not edilmeli; çalıştırılan model log ile teyit edilmeli.**

**Uygulamada dikkat:** Önbellek fiyatları, yoğun/boş saat tarifeleri, reasoning düzeyi ve tool-call dönüşünün biçimi maliyeti ve davranışı değiştirir. Tarihsiz bir “DeepSeek en ucuz” tablosu yayınlamayın.

**Kaynak:** [V4 duyurusu](https://api-docs.deepseek.com/news/news260424/), [V4-Pro GA](https://api-docs.deepseek.com/news/news260813/), [V4.1-Flash](https://api-docs.deepseek.com/news/news260910/), [güncel API başlangıç ve fiyat notları](https://api-docs.deepseek.com/quick_start/pricing-details-cny/).

## 3. Z.ai / Zhipu — GLM

GLM-5.3 (14 Ağustos 2026 duyurusu) uzun ufuklu kodlama ve ajan işlerine odaklanıyor; aynı GLM-5.2 temel modeli üzerine yapılan post-training geliştirmeleri vurgulanıyor. GLM-5.3-Flash farklı bir mimari/ölçek seçeneği. Resmî depo 5.3 için **744B toplam / 40B etkin**, Flash için **320B toplam / 18B etkin** model ağırlıklarına işaret ediyor.

**Önemli lisans ayrımı:** `zai-org/GLM-5.3` model kartı **`glm-5.3` özel lisansı** gösteriyor. Eski bir GLM sürümü veya 5.3-Flash Apache benzeri şartlarla sunulsa bile bunları otomatik olarak 5.3'e taşımayın. Ticari kullanımda metni hukuk/uyum kontrolünden geçirin.

**İzlenecek:** Reasoning effort değerleri, tool-call akışı, gerçek self-host kaynak tüketimi, İngilizce/Türkçe çıktı arasında beklenmedik dil değiştirme ve uzun görev sonunda test başarısı.

**Kaynak:** [GLM 5.3 duyurusu](https://z.ai/blog/glm-5.3), [resmî GLM-5 kod deposu](https://github.com/zai-org/GLM-5), [GLM-5.3 model kartı](https://huggingface.co/zai-org/GLM-5.3), [Mistral üzerinde GLM-5.3 üçüncü taraf barındırması](https://docs.mistral.ai/models/zai-glm-5-3).

## 4. Moonshot AI — Kimi

**Kimi K3**, Moonshot'un 22 Temmuz 2026 duyurusuyla ürünleştirdiği çok biçimli ve uzun bağlamlı model ailesidir. **Kimi K2.7 Code** ise daha eski, kodlama odaklı başka bir seçenektir. Model ailesini, Kimi üyeliğini ve API kullanımını birbirine karıştırmayın.

**Açık ağırlık ama koşulsuz değil:** Kimi K3 model kartı `kimi-k3` lisansına bağlıdır. Lisans, belirli gelir düzeyini aşan *Model as a Service* işleri için ek sözleşme ve bazı büyük ticari ürünler için görünür marka kullanımı şartları içeriyor. Kimi K3'ü “MIT” veya “Apache 2.0” diye etiketlemeyin.

**İzlenecek:** Uzun bağlamda cache hit oranı, 5 dakika/1 saat cache TTL seçenekleri, servis yoğunluğunda 429 ve gecikme, abonelik/API ayrımı ve çok biçimli iş yükleri.

**Kaynak:** [Resmî Kimi duyuruları](https://forum.moonshot.ai/c/announcement/5), [Kimi K3 model kartı](https://huggingface.co/moonshotai/Kimi-K3), [resmî lisans metni](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE), [önbellek güncellemesi](https://forum.moonshot.ai/t/context-caching-upgrade-5-min-1-hour-ttl-options/613).

## 5. MiniMax — M3

MiniMax M3, indirilip barındırılabilen çok biçimli model ağırlıkları ile API/abonelik ürünlerini birlikte sunuyor. Şirketin güncel Token Plan sayfası 1M bağlamı ve M3 kullanımını listeliyor; **Token Plan, üretim ortamı için otomatik olarak en uygun faturalandırma modeli değildir** — şirket pay-as-you-go yaklaşımını üretim için öneriyor.

**Lisans ayrımı:** Hugging Face üzerindeki M3 **`minimax-community`** lisansındadır. Ticari kullanımda görünür atıf, belirli senaryolarda bildirim ve yüksek gelirde ayrı izin hükümleri içerir. Sadece “open source” yazıp geçmeyin.

**Kaynak:** [MiniMax M3 model kartı](https://huggingface.co/MiniMaxAI/MiniMax-M3), [M3 lisans metni](https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE), [Token Plan / API ayrımı](https://platform.minimax.io/subscribe/token-plan).

## 6. ByteDance — Doubao / Seed

Volcengine belgelerinde **Doubao Seed 2.1** (Pro, Lite, Turbo sürümleri) ve tarihli snapshot kimlikleri yer alıyor. Bu sürümlerin bir kısmında Chat ve Responses API akışları farklı kısıtlarla çalışabiliyor.

Örnek tarihli kimlikler: `doubao-seed-2-1-pro-260915`, `doubao-seed-2-1-lite-260915`, `doubao-seed-2-1-turbo-260628`. Eski 2.0 Pro ve Code sürümlerinin 8 Ağustos 2026 itibarıyla servis dışı kaldığı ve 2.1 ailesine geçiş önerildiği sağlayıcı belgelerinde bulunuyor.

**Kaynak:** [Volcengine model/API seçenekleri](https://docs.volcengine.com/docs/82379/1359497?lang=en), [fiyat ve geçiş notu](https://docs.volcengine.com/docs/aidap/Billing_items_and_prices_of_large_model_access?lang=en).

## 7. Baidu — ERNIE

Baidu AI Studio listesinde **ERNIE 5.1** (`ernie-5.1`) ve **ERNIE 5.0** (`ernie-5.0`) bulunuyor. Sağlayıcının ilgili API belgesinde ikisi için **128k bağlam** belirtiliyor. Çincedeki başarı, Türkçe uzun metin düzenleme veya Türkiye'de erişim kalitesi için doğrudan kanıt değildir.

**İzlenecek:** Türkçe deyim/terim, kaynak sadakati, fiyat ve bölge. [Resmî Baidu model listesi](https://ai.baidu.com/ai-doc/AISTUDIO/Mmhslv9lf).

## 8. Tencent — Hunyuan / HY3

Tencent için **model adı kadar platform göçü** önemlidir. Tencent Cloud belgelerinde eski Hunyuan model hizmetinden **TokenHub** platformuna geçiş anlatılıyor; 2026'da eski model kimliklerinin kapatılması ve `hy3-preview` gibi alternatiflere yönlendirme bilgileri var. Eski bir Hunyuan entegrasyonu yalnızca model adını değiştirerek sorunsuz çalışmayabilir.

**İzlenecek:** API taban URL'si, eski kimliklerin çalışma durumu, faturalandırma hesabı, veri bölgesi ve kapanış tarihi. [Ürün özeti](https://cloud.tencent.com/document/product/1729/104753) · [Göç ve kapanış](https://cloud.tencent.com/document/product/1729/131925).

## 9. Xiaomi — MiMo

Xiaomi'nin **MiMo V2.5** ailesi özellikle agentic coding ve çok biçimli işlem çalışmaları açısından araştırma listesinde. Uygulama kararı vermeden önce **resmî model kartı, gerçek dağıtım desteği ve lisans** birlikte doğrulanmalı; üçüncü taraf kurulum rehberindeki bellek gereksinimini tüm kurulumlar için evrensel kabul etmeyin.

**Kaynak:** [XiaomiMiMo resmî GitHub organizasyonu](https://github.com/XiaomiMiMo), [MiMo depo görünümü](https://github.com/XiaomiMiMo/MiMo).

## 10. Huawei Pangu ve izlenecek diğer Çin aktörleri

Huawei **Pangu**, kurumsal/alan odaklı modeller ve **Ascend** altyapısı bakımından takip edilmeli. Aynı şekilde iFlytek Spark, 01.AI Yi, StepFun Step, InternLM/Shanghai AI Lab ve SenseTime SenseNova ekosistemleri ikinci kademe gözlem listesine alınabilir. Bu başlıklar için bu sürümde **“en yeni model” ve fiyat iddiası verilmedi**; gerekli resmî model kartı doğrulaması yapılmadan katalog satırına kesin teknik değer yazılmayacak.

## Çinli modeller için karar kontrolü

- [ ] API ve model ağırlıkları **aynı model/snapshot** mı?
- [ ] Model kartında **lisans adı ve tam metni** kontrol edildi mi?
- [ ] Ticari dağıtım, atıf ve Model-as-a-Service şartları okundu mu?
- [ ] Veri hangi bölgede işleniyor; KVKK ve kurum politikasıyla uyumlu mu?
- [ ] Türkçe testleri, şema doğrulaması ve tool-call başarısı ölçüldü mü?
- [ ] Kota, 429, timeout, önbellek ve fatura sürprizleri test edildi mi?
- [ ] Bir alternatif sağlayıcı ve geri dönüş modeli tanımlandı mı?

**Sonuç:** Ülke veya marka, tek başına kalite ölçütü değildir. Bir modelin gerçek değeri, proje verileri üzerinde başarı, maliyet, denetlenebilirlik ve güvenilirliktir.

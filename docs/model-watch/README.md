# Model Watch | Yapay zekâ model ve araç gözlemevi

> **Son doğrulama: 2026-10** · **Son kapsamlı kaynak taraması:** 11 Ekim 2026 · **Dil:** Türkçe · **Kapsam:** Yapay Zekâ ile Üretim Mühendisliği, 4 cilt · **Durum:** Belgeler üzerinden doğrulanan anlık görünüm; canlı API testi yapılmadı.

Yapay zekâ modellerinin adları, fiyatları ve yetenekleri birkaç ayda değişebiliyor. Bu yüzden kitapta verilen bir model adı, yıllarca geçerli olacak bir tavsiye değildir. **Model Watch**, dört ciltlik kitap serisinin güncel ve denetlenebilir ekidir: ne değişti, hangi bilgiye güvenebiliriz, hangi seçimi neden yapıyoruz ve bu değişiklik çalışan bir uygulamayı nasıl etkiler?

Burada amaç modelleri yarıştırıp her ay yeni bir şampiyon ilan etmek değil. Bir modelin **duyurulması**, **API'den erişilebilir olması**, **ağırlıklarının yayımlanması** ve **üretimde güvenle kullanılabilmesi** birbirinden farklı aşamalardır. Bu fark görünür kalır.

## Nereden başlamalı?

| Belge | İçerik | En çok kime yarar? |
|---|---|---|
| [Ekim 2026 görünümü](tr/2026-10-gorunumu.md) | Öne çıkan değişiklikler ve güncel durum | Hızlıca güncel kalmak isteyenler |
| [Çinli model ekosistemi](tr/cinli-modeller.md) | Qwen, DeepSeek, Kimi, GLM, MiniMax, Doubao, ERNIE, Hunyuan, MiMo ve diğerleri | Alternatif API ve açık ağırlık arayanlar |
| [Küresel model ekosistemi](tr/kuresel-modeller.md) | OpenAI, Claude, Gemini/Gemma, Grok, Meta/Llama, Mistral ve diğerleri | Geniş seçenekleri karşılaştıranlar |
| [Model seçimi ve değerlendirme](tr/model-secimi-ve-olcum.md) | Göreve göre seçim, maliyet, Türkçe kalite, test matrisi ve benchmark okuryazarlığı | Proje geliştirenler ve eğitmenler |
| [Geçiş ve API uyumluluğu](tr/gecis-ve-uyumluluk.md) | Eskiyen model kimlikleri, alias tehlikeleri, regresyon testleri | Çalışan sistemleri yönetenler |
| [Kaynaklar ve güncelleme ilkeleri](tr/kaynaklar-ve-guncelleme.md) | Birincil kaynaklar, kanıt etiketleri, güncelleme ve katkı kuralları | Katkı verenler ve coding agent'lar |
| [Ortak model verileri](data/README.md) | 29 model kaydı, JSON veri katmanı ve doğrulama aracı | İki dilli yayın ve otomasyon geliştirenler |

## Temel ayrımlar

- **Model / ürün / sağlayıcı / dağıtım:** ChatGPT ile GPT API'si; Claude sohbeti ile Claude API'si; Meta AI ile Llama ağırlıkları aynı ürün değildir.
- **Genel erişim (GA) / önizleme / özel erişim:** Önizleme, üretim garantisi anlamına gelmez.
- **Açık ağırlık / açık kaynak / açık lisans:** Model dosyasını indirebilmek, ticari dağıtımın sınırsız olduğu anlamına gelmez. Lisans sürüme göre okunur.
- **Bağlam (context) / gerçek başarı:** 1 milyon token kabul edebilmek, bu uzunluğun tamamında doğru cevap üretileceğini kanıtlamaz.
- **Uyumlu API / eşdeğer davranış:** OpenAI biçiminde istek kabul edilmesi, `tool_calls`, reasoning, JSON schema, görsel veya token sayımının birebir aynı çalışacağı anlamına gelmez.
- **Sağlayıcı benchmark'ı / bağımsız değerlendirme:** İlkini bilgi olarak kaydeder, ikincisini ayrıca arar; kitabın kendi sonuçlarıymış gibi sunmayız.

## Kitapla bağlantı

| Cilt | Model Watch'tan yararlanma |
|---|---|
| **1 — Yapay Zekâ Okuryazarlığı ve Prompt Mühendisliği** | Model sınırları, istem tasarımı, yapılandırılmış çıktı, doğruluk kontrolü ve Türkçe anlatım |
| **2 — Vibe Coding ve Loop Engineering** | Kod üreten model seçimi, hata ayıklama, test geri bildirimi, token bütçesi ve model geçişi |
| **3 — Agent Engineering** | Araç çağrısı, izin sınırları, uzun görevler, MCP, bellek ve geri alma |
| **4 — AI-Native Production** | Gateway, maliyet, yönlendirme, gözlemlenebilirlik, regresyon testleri ve güvenli sürüm yükseltme |

## Güncelleme takvimi

| Dönem | Ne kontrol edilir? |
|---|---|
| Haftalık (öncelikli olaylar) | Yeni modelin API'de açılması, kapanma tarihi, fiyat veya lisans değişikliği, kırıcı değişiklik |
| Aylık | Sağlayıcı/model tablosu, resmi model kimliği, erişim bölgesi, token penceresi, açık ağırlık ve lisans |
| Üç ayda bir | Görev bazlı testler, Türkçe kalite, uzun bağlam, ajan güvenilirliği, DORA ve sektör verileri |
| Her kitap/lab güncellemesinde | Örnekteki model kimliği ve parametrelerinin güncel belgelerle uyuşması |

## İki dilli yayın düzeni

Şimdilik **Türkçe esas metindir**: `docs/model-watch/tr/`. İngilizce sürüm hazırlanırken `docs/model-watch/en/` oluşturulacak. Dosya kimlikleri, bölüm sırası, tablo sütunları ve kaynak bağlantıları olabildiğince korunacak; İngilizce içerik otomatik olarak güncel kabul edilmeyecek, kendi kontrol tarihini taşıyacak. Bu README iki dile geçildiğinde dil seçici giriş sayfasına dönüşebilir.

## Okuyucu ve katkı verenlere

Bu sayfaları kaynak gösterirken **belge tarihi** ile **modelin yayımlanma tarihini** karıştırmayın. Bir hatayı veya yeni sürümü bildirirken ilgili resmî kaynak bağlantısını, değişen alanı ve kontrol tarihini ekleyin. Katkı ilkeleri için [CONTRIBUTING.md](../../CONTRIBUTING.md); coding agent sınırları için [AGENTS.md](../../AGENTS.md) geçerlidir.

**Kısa ilke:** Model adı değişebilir; doğrulama, test etme ve geri alabilme alışkanlığı kalıcı olmalı.

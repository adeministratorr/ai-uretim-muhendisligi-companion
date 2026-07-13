# Prompt Kütüphanesi

Bu klasör, serinin tüm ciltlerini destekleyen uygulamalı prompt koleksiyonudur.
Amaç hazır kalıp ezberletmek değil; Cilt 1'de anlatılan prompt anatomisini
(persona, görev, bağlam, format, kısıt, başarı kriteri) farklı alanlarda
çalışan örneklerle göstermektir. Her prompt, gerektiğinde köşeli parantezli
değişkenlerle (`[ürün adı]` gibi) şablonlaştırılmıştır: değişkeni doldurmadan
kullanmayın.

Prompt anatomisinin çalışan denetim örneği için bkz.
[`../cilt-1-prompting/prompt-patterns/`](../cilt-1-prompting/prompt-patterns/).

---

## Kategori Haritası

| # | Dosya | Kapsam |
|---|---|---|
| 01 | [yazilim-gelistirme.md](01-yazilim-gelistirme.md) | Kod yazma, kod inceleme (code review), hata ayıklama, test, dokümantasyon |
| 02 | [yazma-ve-icerik.md](02-yazma-ve-icerik.md) | Blog, e-posta, rapor, özetleme, çeviri, üslup dönüştürme |
| 03 | [is-ve-verimlilik.md](03-is-ve-verimlilik.md) | Toplantı, strateji, pazarlama, satış, İK, karar analizi |
| 04 | [egitim-ve-ogrenme.md](04-egitim-ve-ogrenme.md) | Özel ders (tutoring), kavram açıklama, çalışma planı, sınav hazırlık |
| 05 | [veri-analizi.md](05-veri-analizi.md) | Veri temizleme, keşif analizi, SQL, görselleştirme seçimi, bulgu raporu |
| 06 | [gorsel-uretim.md](06-gorsel-uretim.md) | Midjourney, gpt-image, Imagen/Nano Banana, Flux; parametreler ve teknik sözlük |
| 07 | [video-uretim.md](07-video-uretim.md) | Veo, Sora, Kling, Runway; kamera dili, ses/diyalog, image-to-video |
| 08 | [json-yapilandirilmis-promptlar.md](08-json-yapilandirilmis-promptlar.md) | JSON/şema tabanlı promptlar: metin, görsel ve video için yapılandırılmış tarifler |
| 09 | [sosyal-medya-trend-promptlari.md](09-sosyal-medya-trend-promptlari.md) | Viral akımların promptları: figürin, Ghibli tarzı, ASMR video, vlog formatları |
| 10 | [kurumsal-sablonlar.md](10-kurumsal-sablonlar.md) | Müşteri desteği, PRD, rapor→yönetim notu, marka brifi, ilan, RFP, iç duyuru |
| 11 | [sosyal-medya-yonetimi.md](11-sosyal-medya-yonetimi.md) | İçerik takvimi, platforma özel gönderi, rakip analizi, topluluk yönetimi, performans |
| 12 | [gunluk-hayat.md](12-gunluk-hayat.md) | Uçak bileti/seyahat, satın alma araştırması, ürün karşılaştırma, sözleşme anlama, hak arama |
| 13 | [strateji-ve-pazarlama.md](13-strateji-ve-pazarlama.md) | SWOT, rakip/pazar analizi, persona, konumlandırma, kampanya planı |
| 14 | [muzik-ve-ses.md](14-muzik-ve-ses.md) | Suno stil/metatag promptları, şarkı düzenleme, TTS, ses klonlama etiği |

---

## Promptlar Nasıl Okunur?

Her kayıt aynı yapıyı izler:

- **Ne işe yarar** — promptun çözdüğü iş.
- **Nerede çalışır** — hedef model/araç ailesi. Görsel ve video modellerinde
  sözdizimi araca özgüdür; metin promptları büyük dil modellerinin tümünde
  küçük uyarlamalarla çalışır.
- **Prompt** — kopyalanabilir metin. Köşeli parantezli alanlar doldurulur.
- **Notlar** — kısıtlar, sık yapılan hatalar, uyarlama önerileri.

İki genel ilke:

1. **Prompt bir dilek değil, iş tarifidir.** Eksik bıraktığınız her bileşeni
   model kendi varsayımıyla doldurur (bkz. Cilt 1, Bölüm 3).
2. **Çıktıyı körlemesine kullanmayın.** Bu kütüphanedeki hiçbir prompt,
   çıktının doğruluğunu garanti etmez; kritik işlerde insan denetimi gerekir.

---

## Kaynak ve Lisans Notu

Bu koleksiyondaki promptların bir bölümü topluluk koleksiyonlarından
(prompts.chat / awesome-chatgpt-prompts, model üreticilerinin resmî prompt
rehberleri) uyarlanmış, Türkçeleştirilmiş ve kitap anatomisine göre yeniden
yazılmıştır; kaynaklar ilgili dosyalarda belirtilir. Model adları, parametre
sözdizimleri ve araç davranışları hızla eskir; her dosya `Son doğrulama:
YYYY-AA` notu taşır.

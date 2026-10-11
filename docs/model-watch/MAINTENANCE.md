# Model Watch | Depo bakım rehberi

Bu belge ve destek dosyaları yalnızca GitHub deposunda tutulur; GitHub Pages yayınına girmez. Okur sayfaları `tr/` ve `en/` altındadır. Kök `_config.yml`, ajan talimatlarını, bakım belgelerini, doğrulama betiklerini ve `data/` kataloğunu yayın dışında bırakır.

## Doğrulama

Depo kökünde çalıştırın:

```bash
python3 docs/model-watch/scripts/validate.py
```

Komut JSON yapısını ve yerel Markdown bağlantılarını kontrol eder; dış kaynakları ve canlı API davranışını doğrulamaz.

[Veri sözlüğü](data/README.md) · [Ortak katalog](data/models.json) · [Katkı rehberi](../../CONTRIBUTING.md) · [Ajan kuralları](../../AGENTS.md)

## Güncelleme takvimi

| Dönem | Ne kontrol edilir? |
|---|---|
| Haftalık (öncelikli olaylar) | Yeni modelin API'de açılması, kapanma tarihi, fiyat veya lisans değişikliği, kırıcı değişiklik |
| Aylık | Sağlayıcı/model tablosu, resmi model kimliği, erişim bölgesi, token penceresi, açık ağırlık ve lisans |
| Üç ayda bir | Görev bazlı testler, Türkçe kalite, uzun bağlam, ajan güvenilirliği, DORA ve sektör verileri |
| Her kitap/lab güncellemesinde | Örnekteki model kimliği ve parametrelerinin güncel belgelerle uyuşması |

## İki dilli yayın düzeni

**Türkçe esas metindir**: `docs/model-watch/tr/`. İngilizce sürüm `docs/model-watch/en/` altındadır. Eşleşen rehberlerde dosya adları, bölüm sırası, tablo sütunları ve kaynak bağlantıları korunur. Her İngilizce belge, kaynak inceleme tarihinden ayrı bir çeviri kontrol tarihi taşır. Çeviri kontrolü, teknik bilgilerin yeniden doğrulandığı anlamına gelmez. İki dil aynı `data/models.json` kataloğunu kullanır. Üst klasördeki README dil seçimini sağlar.

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

İngilizce sürüm `docs/model-watch/en/` altında, Türkçe sürüm `docs/model-watch/tr/` altındadır. Eşleşen rehberler aynı dosya adını, bölüm sırasını ve tablo yapısını korur. Kaynak URL'leri, API model kimlikleri, sayısal veriler ve çalıştırılabilir örnekler çeviride değişmez. Her İngilizce belge kaynak inceleme tarihini ve ayrı çeviri kontrol tarihini taşır; çeviri kontrolü yeni bir kaynak veya canlı API doğrulaması sayılmaz. Türkçeye eklenen model İngilizce sürüme otomatik eklenmiş kabul edilmez. Ortak katalog `data/models.json` içinde tek kopya tutulur; veri alanlarının iki dilde açıklaması bulunur. Dil geçişleri karşılık gelen belgeye bağlanır. Yayın öncesinde yerel bağlantılar, kaynak URL eşliği, bölüm/tablo yapısı ve örnekler kontrol edilir.

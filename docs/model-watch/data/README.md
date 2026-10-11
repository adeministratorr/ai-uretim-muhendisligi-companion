# Ortak model veri kayıtları

`models.json`, Model Watch'un **dilden bağımsız veri katmanıdır**. Türkçe metin `tr/` altındadır; İngilizce sürüm eklendiğinde `en/` bu bilgileri kullanabilecek. JSON kataloğu uygulamada doğrudan çalıştırma ayarı olarak kullanılmamalıdır: `listed`, `preview`, `released`, `watch` gibi statüler, yetenek ve erişim garantisi değildir.

## Alanlar

| Alan | Açıklama |
|---|---|
| `provider`, `family`, `name` | Üretici, aile ve model adı |
| `model_id` | Belgede doğrulandıysa tam API veya ağırlık repo kimliği; değilse `null` |
| `status` | `ga`, `preview`, `listed`, `released`, `watch` |
| `distribution` | `api`, `weights`, `api_and_weights`, `unknown` |
| `license` | **Yalnızca açıkça kontrol edilmişse** lisans etiketi |
| `evidence` | `R1`, `R2`, `R3`, `R4`, `B`, `T` — açıklama [kaynak standardında](../tr/kaynaklar-ve-guncelleme.md) |
| `source` | Birincil kaynak (bir URL) |
| `last_verified` (kök) | Bütün kataloğun son kaynak inceleme tarihi |

**Önemli:** Model kartındaki indirme lisansı ile bir API hizmetinin kullanım sözleşmesi aynı olmak zorunda değildir. `model_id: null` bilinmeyen bilgi için bilinçli seçimdir; örnek ID uydurulmaz. Her gelecek değişiklikte kaynağı yeniden doğrulayın, sonra JSON ve metin dosyalarını birlikte güncelleyin.

`python3 docs/model-watch/scripts/validate.py` ile JSON yapısı ve yerel Markdown bağlantıları kontrol edilebilir. Bu komut dış ağ bağlantısı kurmaz.

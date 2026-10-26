# Pusula kitap ve uygulama üretim planı

26 Ekim 2026. Bu dosya teslim sırasını özetler. Yapılacak dosya değişiklikleri, bağımlılıklar ve kabul koşulları [ayrıntılı iş planındadır](docs/superpowers/plans/2026-10-26-pusula-sonraki-isler.md).

Hedef, kaynak kitapların bilgisini promptlarla üretilen proje belgelerine, çalışan Pusula uygulamasına ve doğrulanmış kitap örneklerine dönüştürmektir. Kitap anlatımı her uygulama grubunun gerçek sonuçlarından sonra yazılır. Kaynakların öğrenme hedefi denetimi de ilgili grup başlamadan yapılır.

## Tamamlanan başlangıç teslimi

- [x] Vardiya'dan farklı Pusula projesi ve 36 uygulamalık sıra hazırlandı.
- [x] 108 üretim, kontrol ve düzeltme promptu taslak olarak yazıldı.
- [x] 100 kaynak bölüm, uygulamalara bölüm düzeyinde eşlendi.
- [x] Örnek proje belgeleri, iki skill ve sentetik veri hazırlandı.
- [x] Qoder ve ZCode dahil 22 araç/bileşenin yönerge davranışı belgelerden incelendi; 37 birincil kaynak kaydedildi.
- [x] Başlangıç paketi GitHub taslak PR #3'e gönderildi; paket denetimi geçti.

Bu maddeler çalışan ürün, sınanmış prompt veya tamamlanmış kitap anlamına gelmez. 11 yönerge vakası ve altı skill vakası henüz çalıştırılmadı. Yazarın kapsam ve çalışma adı incelemesi de tamamlanmış olarak kaydedilmedi.

## Sıradaki teslimler

| Öncelik | İş grubu | Somut teslim | Tamamlanma koşulu |
|---|---|---|---|
| 1 | P01–P03: kapsam, yeni yaklaşımlar ve koşu düzeni | Öğrenme hedefi haritası, 12 yaklaşımın yerleşimi, gerçek koşu kayıt biçimi | Pilot hedefleri uygulama ve kabul deneyine bağlanır; kanıtsız başarı kaydı reddedilir |
| 2 | P04–P06: U01–U08 pilotu ve örnek bölümler | Üretilmiş proje belgeleri, ajan/skill deneyleri, U01/U07/U08 kitap metinleri | Gereksinim–tasarım–görev ilişkisi ve seçilen araçtaki davranış gözlenir |
| 3 | P07: U09–U12 | Prompt karşılaştırması ve ilk çalışan Pusula | Model deneyi ile sabit öğretim yanıtı ayrılır; yerel ürün akışı tekrarlanır |
| 4 | P08–P09: U13–U21 | Bağlam, RAG, izin, loop, harness ve kurtarma | Kaynak desteği, durma koşulları ve kesintiden devam gerçek senaryolarla sınanır |
| 5 | P10: U22–U28 | İş bölümü, değerlendirme, güvenlik, çok kipli kullanım ve birlikte çalışma | Yanıt kadar işlem izi ve yetki de değerlendirilir |
| 6 | P11: U29–U35 | Maliyet, işletim, dağıtım ve ileri yöntem deneyleri | Karşılaştırmalar aynı görev seti ve kayıtlı bütçeyle yapılır |
| 7 | P12: U36 ve bütünlük | Kitap taslağı, mevcut kitap ekleri ve sürümlü companion | Kaynak hedefleri, başlangıç/çözüm dosyaları ve gerçek koşular birbirine bağlanır |

## Önce yapılacak üç iş

1. U01–U08'e bağlanan kaynak bölümleri öğrenme hedefi düzeyinde incelemek; kalan bölümlerin denetim sırasını kaydetmek.
2. İzlenebilirlik, ajan deneyimi ve skill taşınabilirliğini pilot promptlarına işlemek; diğer yeni yaklaşım önerilerini ilgili uygulamalara yerleştirmek.
3. Prompt, girdi, araç/model, çıktı ve doğrulama kayıtlarını bağlayan koşu düzenini kurmak; ardından U01'i boş ürün dizininde çalıştırmak.

## Üretim boyunca uygulanacak düzen

Her uygulama grubunda kaynak incelemesi, üretim, kabul deneyi, düzeltme ve bölüm yazımı tamamlanır. Mevcut kitaplara eklenecek anlatım aynı grubun sonuçlarına dayanır. Cilt/bölüm düzeyindeki ek önerisi ayrı kaydedilir; kitaplar arasındaki ortak kavramlar aynı anlamda kullanılır.

Araç karşılaştırmasının ilk grubu Codex, Claude Code, Qoder IDE/CLI ve ZCode'dur. Koşular erişilebilir araçlarda yürütülür; erişilemeyen araç için belge incelemesi başarı deneyi sayılmaz. Diğer araçlar sonraki uyumluluk teslimlerinde ele alınır.

Sonraki uygulamaya geçiş, gereken önceki çıktının kabulüne bağlıdır. Model erişimi, yeni kurulum veya yayın kararı gerektiren işler kendi yürütme aşamasında değerlendirilir. Bu plan, canlı yayın onayı veya yapılmamış deneylerin sonucu değildir.

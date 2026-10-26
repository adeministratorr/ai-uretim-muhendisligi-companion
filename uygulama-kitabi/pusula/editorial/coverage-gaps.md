# Öğretim açıkları ve sonraki kaynak okumaları

P01’de 100 kaynağın revizyon envanteri çıkarıldı ve ilk sekiz uygulamayla ilişkili 31 bölüm baştan sona okundu. Bu okumalardan 299 öğrenme hedefi ve 299 önerilen kabul vakası çıkarıldı. P02 sonrasında 206 pilot hedef öğretim tasarımında eşlenmiştir; bunların çalışma sonuçları henüz yoktur.

İlk 27 açığın 25’i pilot promptlarında karşılandı. Süreli GUI prototipi U11’e, harici tasarım skill’i karşılaştırması U33’e taşındı. Önceki açık gerekçeleri ve yeni prompt/vaka bağlantıları [hedef kayıtlarında](learning-objectives.json) korunur. `mapped` yalnız öğretim eşlemesidir; `runtime_status` değerleri `not_run`, gözlemler `null` kalır.

İleri uygulamalara ayrılan 93 hedefin 50 tanesi öğretim veya kabul tasarımı bekler. Kalan 69 kaynağın tam okuması yapılmadı. Bu nedenle bütün kitap içeriğinin uygulandığı veya denetlendiği söylenemez.

## Açık kalan ileri hedefler

| Hedef | Uygulama | Yapılacak iş |
|---|---|---|
| C2-B01-O08 | U34 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O03 | U11 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O05 | U34 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O06 | U34 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O07 | U11 | U11 çalıştırma kaydı içeriyor; akış hâli ve kesinti karşılaştırması ölçütü yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O08 | U12 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O09 | U11 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O10 | U25 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O13 | U20 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O16 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O18 | U20 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O19 | U17 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O20 | U24 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O02 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O06 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O07 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O08 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O09 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O16 | U13 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O18 | U13 | U13 bağlam seçimini içeriyor; kod bağımlılığı çizgesinin türlendirilmiş kenarları ve kaynağı için çıktı/kabul koşulu yok. U16 belge bilgi grafı bu kod inceleme hedefinin yerine geçmez. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O19 | U13 | U13 içinde eski kod çizgesi, sembol kaynağı ve kapsam eksikliği senaryoları tanımlanmamış. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B04-O07 | U12 | U12 hata ayıklama döngüsü içeriyor ancak ACP/LSP ayrımı ve aynı adlı sembol bulma karşılaştırması için çıktı ve vaka yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B04-O09 | U11 | U11 tek çalışan uygulamayı hedefliyor; iki IDE için aynı görevle beş sütunlu karşılaştırma çıktısı yok. Seçim gerekçesi U01e uyarlanabilir ancak deney pilota taşınmamalı. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B05-O06 | U11 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B06-OBJ-09 | U11, U12 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B06-GAP-6-9 | U11, U12 | CLI ajanlarının aynı hatada diff/onay/test karşılaştırması U11/U12de açık çoklu araç kabulü olarak tanımlanmamış; isteğe bağlı erişilebilirlik kolu gerekir. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-08 | U35 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-09 | U35 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-10 | U24, U29 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-10 | U20, U25 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-12 | U17, U25 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-13 | U31 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-GAP-9-13 | U31 | U31 ci-plan çıktısı mimari bağımlılık denetiminde olumlu/olumsuz örnek ve zorunlu check atlama sınamasını açıkça istemiyor. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-OBJ-11 | U33 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-OBJ-12 | U33, U32 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-GAP-10-12 | U33, U32 | U08 iki Pusula skilline odaklanıyor; kaynak Lab 10daki üç hazır skill kurma-karşılaştırma ayrı kabulü kapsam dışı kalıyor. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-03 | U32, U36 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-04 | U36 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-05 | U31 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-06 | U31, U36 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-GAP-1-6 | U31, U36 | Müfredatta süreli geçiş kararı, C4 açık iş envanteri ve sekiz kullanıcı durumunu birleştiren bağımsız hazırlık teslimi açıkça yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-03 | U20, U30 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-04 | U21 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-05 | U30 | İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-GAP-2-4 | U21 | U21 kesintiden sürdürme var; bağımsız yerel alıcıda sabit kimlik/içerik/makbuz ve kesinti sonrası ikinci etki sayısını sınayan açık kabul yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-GAP-2-3 | U20, U30 | U30 kapasite genel; iki müşteri için sınırlı/sınırsız kontrol koşulu ve insan bekleme yuvasının serbestliği açık kabul değil. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| CC-B16-O08 | U33 | U33 genel uyumluluk/güncelleme içerir; özel komuttan göç vakası needs_design. |
| CC-B17-O06 | U33 | U33 dağıtım hedefi var; Pusula doğrulayıcı betiği ve yürütülebilir sözleşmesi henüz tasarlanmamış. needs_design. |
| CC-B29-O03 | U26 | U26 görsel/PDF/ses ve tarayıcıyı kapsar; Figma entegrasyonu için karşılık yok, ihtiyaç varsa needs_design. |
| CC-B29-O07 | U11 | U11 tarayıcı gözlemi ister; sabit viewport, insan referans kabulü ve ikinci görsel koşu açık zorunluluk değil. |

## Tam okuma bekleyen kaynaklar

Her grup başlamadan bu kaynaklar baştan sona okunacak; başlık envanteri tam okuma yerine geçmez.

| Grup | Kaynaklar |
|---|---|
| U09-U16 | C1-B04, C1-B06, C1-B07, C1-B08, C1-B10, C1-B11, C2-B11, C2-B12, C3-B05, C3-B06, C4-B04, C4-B07, C4-B09, CC-B05, CC-B06, CC-B08, CC-B09, CC-B30, CC-B36, CC-B38 |
| U17-U24 | C1-B13, C1-B14, C2-B13, C3-B01, C3-B02, C3-B03, C3-B04, C3-B08, C3-B10, C3-B13, C4-B05, C4-B14, CC-B11, CC-B18, CC-B19, CC-B20, CC-B22, CC-B23, CC-B24, CC-B25, CC-B26, CC-B27, CC-B31, CC-B32, CC-B33 |
| U25-U32 | C1-B09, C1-B12, C1-B16, C2-B14, C3-B09, C3-B11, C3-B12, C3-B14, C4-B03, C4-B08, C4-B10, C4-B11, C4-B12, C4-B13, C4-B15, CC-B12, CC-B34, CC-B35, CC-B37, CC-B39 |
| U33-U36 | C1-B15, C1-B17, CC-B28, CC-B40 |

## Kaynak ve kanıt sınırı

Sekiz Claude Code kaynağının revizyonu başlangıç envanterinden farklıdır. Pilot içindeki CC-B17 güncel revizyonuyla okundu; diğer yedi değişmiş kaynağın tam okuması bekler. Başlangıç özetleri [kaynak envanterinde](source-map.json) korunur. Üç kaynak tutarsızlığı [kitap güncelleme önerilerine](book-updates.json) aktarıldı; ana kitaplara müdahale edilmedi.

Paket denetimi metnin anlamını veya promptların başarısını ispatlamaz. Kanonik kayıtlar editörün kaynak okuması ve düzenlemeleridir. Antigravity ile kaynak denetimi için bağımsız örneklem incelemesi yapıldı; bu inceleme U01–U36 model deneyi değildir.

# P01 kapsam açıkları ve sıradaki denetim

P01 kaynak denetimi `audit_complete`:100 kaynağın revizyon envanteri ve pilot31 kaynağın tam okuması tamamlandı. Öğretim geçidi `pilot_gap_resolution_pending`:pilot208 hedefin181i eşlendi,27si açık. İleri uygulamalara ayrılan91 hedefin41i somut eşleme,50si öğretim veya kabul tasarımı açığıdır. Toplam299 hedef ve299 önerilen sentetik vaka vardır. Bütün runtime alanları `not_run`, gözlemler `null`dır.

`mapped` öğretim tasarımıdır; uygulama koşusu değildir. `needs_design` olan ileri vakalar o grup başlamadan somut girdiye ve yanlış adaya bağlanmalıdır. Tam okuma69 kaynak için hâlâ beklenir; dosya envanterini hedef denetimi saymadık. Kapsam dışı karar alınmadı.

## Pilot: P02de kapatılacak öğretim açıkları

| Hedef | Kaynak başlığı | Uygulama | Açık gerekçesi |
|---|---|---|---|
| C1-B01-P01-01 | 1.1 Yapay Zekâ, Makine Öğrenmesi ve Derin Öğrenme Ayrımı | U01 | U01 görevinde AI/ML/DL karşılaştırması açık öğretilmiyor; vision.md içinde kısa karşılaştırma alıştırması eklenmeli. |
| C1-B05-P01-05 | 5.9 Çakışan Talimatlar Nasıl Çözülür? | U07 | Kaynak 5.9-5.10 tasarım katmanlarını evrensel öncelik sırası gibi anlatıyor. U07 içinde araca özgü resmi belgeyle nitelendirilmeden doğrudan aktarılmamalı. |
| C2-B01-O06 | 1.6 Junior, Mid-Level ve Senior Geliştirici İçin Yeni Beceri Setleri | U01 | Müfredatta kıdem bazlı beceri gelişim matrisi bulunmuyor. |
| C2-B01-O09 | 1.9 Bu Kitabın Kullanım Yöntemi | U01 | U01 rolleri ayırıyor ancak bölüm laboratuvarındaki 5–8 satırlık üç sütunlu sorumluluk matrisi çıktısı tanımlı değil. |
| C2-B05-O08 | 5.8 GUI Araç Seçim Matrisi | U03 | U03 tasarım belgesi üretiyor; U11 çalışan uygulamaya daha yakın olsa da süreli GUI prototipi ve müdahale günlüğü müfredatta tanımlı değil. U26 çok kipli/tarayıcı test hedefi bu MVP deneyinin yerine geçmez. |
| C2-B09-OBJ-15 | 9.15 Laravel/React/Flutter Örnekleri | U07 | U07 ortak sınırları ve komutları ister; kaynağın üç yasak, üç doğrulama ve PR devre kesici sayıları açık alıştırma/kabul koşulu olarak tanımlı değil. P02 sayıların öğretim gerekçesini ve gerekecek prompt ekini değerlendirmeli. |
| C4-B01-OBJ-02 | 1.2 Kullanıcı Etkisi ve Hizmet Sınırı | U03 | U03 bekleme, iptal ve eski kaynak durumlarını ister; kaynağın sekiz kullanıcı durumunun tamamını ve özellikle kısmen tamamlandı/sonuç belirsiz ayrımını açık kabul koşuluna bağlamaz. P02de durum karşılaştırma alıştırması ve beklenen ekran kanıtı netleştirilmeli. |
| CC-B03-O03 | Native kurulum | U01 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B03-O04 | Paket yöneticisiyle kurulum | U01, U04 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B03-O09 | Kurulum laboratuvarı | U01 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B10-O02 | Manuel mod: Düzenleme yapılmadan önce karar verin | U07 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B10-O03 | `acceptEdits`: Dosya düzenlemelerinde tek tek durmadan ilerleyin | U07 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B10-O10 | Modları değiştirme ve doğrulama | U07 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B10-O11 | Laboratuvar: Aynı görevi iki başlangıç biçimiyle inceleme | U06, U07 | İlgili ders kavramsal karşılık sağlıyor; bu Claude Code kurulum/mod laboratuvarının ayrı çalışma kaydı, dosya çıktısı ve olumlu/olumsuz runtime kabul deneyi mevcut müfredatta açıkça tanımlı değil. |
| CC-B15-O01 | Ayar kapsamı kararın sahibini gösterir | U01, U07 | U07 yönerge kapsamını işler; ayar kapsamı/sahibi karar matrisi açık çıktı değildir. |
| CC-B15-O02 | Dosya yollarını çalışılan ortamla birlikte okuyun | U01, U07 | U07 sürüm ve alt dizin yönerge testleri var; settings keşif farkı açıkça kapsanmıyor. |
| CC-B15-O03 | Öncelik ile birleşme aynı şey değildir | U07 | Çelişen yönerge testi ayar dizilerinin birleşmesi testi değildir; U07 kabulüne ayrı koşul gerekir. |
| CC-B15-O08 | Laboratuvar: Proje standardı ile yerel istisnayı ayırmak | U07 | U07 tam ayar laboratuvarı ve geri dönüş adımlarını tanımlamıyor; pilot için ek kurulum zorunluluğu yapılmamalı. |
| CC-B16-O03 | Skill kapsamı kararın sahibini belirler | U07, U08 | U08 keşif ve davranış ayrımını ister; kapsam çakışması ve gerçek hedef dizin örneği henüz verilmemiş. |
| CC-B17-O02 | Bilgiyi gerektiği anda yükleyin | U08 |  Ayrıntılı references/belge-iliskileri.md çıktısı U08 müfredat/prompt çıktı listesinde yok; P02de açık çıktı veya SKILL.md içi başvuru kararı gerekli. |
| CC-B17-O03 | Skill kaynağı ile proje kökünü ayırın | U08, U33 | U08 uygulama kökünü belirler; taşınmış paket kökü ve ürün/sürüm farklılığı için somut vaka eklenmeli. |
| CC-B17-O05 | Yardımcı dosyalarla yeni yapı | U08 | U08 paket biçimi/skill seçimini ayırıyor; çıktı biçimi ile anlamsal destek için bağımsız doğrulama ve yardımcı betik sözleşmesi yok. |
| CC-B17-O07 | Dinamik `!` yerleştirme bir ön işlemdir | U08 | U08 kaynak içi talimatı veri sayar; modelden önce çalışan dinamik kabuk ön işlemi açık denetim maddesi değil. |
| CC-B17-O10 | Skill kullanılmadan karşılaştırma sonucunu alın | U08, U24 | U08 ve U24 Skill kullanılan/kullanılmayan karşı koşulu zorunlu kılmıyor; CC-B17 güncel kaynağındaki önemli açık hedef. |
| CC-B17-O14 | Doğrulama döngüsüne sınır koyun | U08, U19 | U08 Skill düzeltme bütçesi tanımlamıyor; ayrıntı U19a bırakılmalı, pilotta sınırsız iyileştirme sözü verilmemeli. |
| CC-B21-O08 | Sekiz senaryoyu en küçük katmana yerleştirin | U07, U19, U20 | Müfredatta kavram ayırımı ilgili derslerde var; Pusulaya özgü sınıflandırma alıştırması yok, kısa köprü etkinliği eklenebilir. |
| CC-B29-O04 | Tasarım Skill'lerini görevlerine göre ayırın | U03, U07, U08 | U03/U08 Pusula Skillleri var; harici tasarım Skill seçimi pilot müfredatının doğrudan amacı değil. |

## Tam okunan kaynaklardaki ileri uygulama açıkları

| Hedef | Uygulama | Durum/gerekçe |
|---|---|---|
| C2-B01-O08 | U34 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O03 | U11 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O05 | U34 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O06 | U34 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O07 | U11 | needs_design: U11 çalıştırma kaydı içeriyor; akış hâli ve kesinti karşılaştırması ölçütü yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O08 | U12 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O09 | U11 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O10 | U25 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O13 | U20 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O16 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O18 | U20 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O19 | U17 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B02-O20 | U24 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O02 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O06 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O07 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O08 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O09 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O16 | U13 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O18 | U13 | needs_design: U13 bağlam seçimini içeriyor; kod bağımlılığı çizgesinin türlendirilmiş kenarları ve kaynağı için çıktı/kabul koşulu yok. U16 belge bilgi grafı bu kod inceleme hedefinin yerine geçmez. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B03-O19 | U13 | needs_design: U13 içinde eski kod çizgesi, sembol kaynağı ve kapsam eksikliği senaryoları tanımlanmamış. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B04-O07 | U12 | needs_design: U12 hata ayıklama döngüsü içeriyor ancak ACP/LSP ayrımı ve aynı adlı sembol bulma karşılaştırması için çıktı ve vaka yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B04-O09 | U11 | needs_design: U11 tek çalışan uygulamayı hedefliyor; iki IDE için aynı görevle beş sütunlu karşılaştırma çıktısı yok. Seçim gerekçesi U01e uyarlanabilir ancak deney pilota taşınmamalı. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B05-O06 | U11 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B06-OBJ-09 | U11, U12 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B06-GAP-6-9 | U11, U12 | needs_design: CLI ajanlarının aynı hatada diff/onay/test karşılaştırması U11/U12de açık çoklu araç kabulü olarak tanımlanmamış; isteğe bağlı erişilebilirlik kolu gerekir. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-08 | U35 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-09 | U35 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B07-OBJ-10 | U24, U29 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-10 | U20, U25 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-12 | U17, U25 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-OBJ-13 | U31 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B09-GAP-9-13 | U31 | needs_design: U31 ci-plan çıktısı mimari bağımlılık denetiminde olumlu/olumsuz örnek ve zorunlu check atlama sınamasını açıkça istemiyor. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-OBJ-11 | U33 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-OBJ-12 | U33, U32 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C2-B10-GAP-10-12 | U33, U32 | needs_design: U08 iki Pusula skilline odaklanıyor; kaynak Lab 10daki üç hazır skill kurma-karşılaştırma ayrı kabulü kapsam dışı kalıyor. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-03 | U32, U36 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-04 | U36 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-05 | U31 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-OBJ-06 | U31, U36 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B01-GAP-1-6 | U31, U36 | needs_design: Müfredatta süreli geçiş kararı, C4 açık iş envanteri ve sekiz kullanıcı durumunu birleştiren bağımsız hazırlık teslimi açıkça yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-03 | U20, U30 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-04 | U21 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-OBJ-05 | U30 | needs_design:  İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-GAP-2-4 | U21 | needs_design: U21 kesintiden sürdürme var; bağımsız yerel alıcıda sabit kimlik/içerik/makbuz ve kesinti sonrası ikinci etki sayısını sınayan açık kabul yok. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| C4-B02-GAP-2-3 | U20, U30 | needs_design: U30 kapasite genel; iki müşteri için sınırlı/sınırsız kontrol koşulu ve insan bekleme yuvasının serbestliği açık kabul değil. İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir. |
| CC-B16-O08 | U33 | öğretim açığı: U33 genel uyumluluk/güncelleme içerir; özel komuttan göç vakası needs_design. |
| CC-B17-O06 | U33 | öğretim açığı: U33 dağıtım hedefi var; Pusula doğrulayıcı betiği ve yürütülebilir sözleşmesi henüz tasarlanmamış. needs_design. |
| CC-B29-O03 | U26 | öğretim açığı: U26 görsel/PDF/ses ve tarayıcıyı kapsar; Figma entegrasyonu için karşılık yok, ihtiyaç varsa needs_design. |
| CC-B29-O07 | U11 | öğretim açığı: U11 tarayıcı gözlemi ister; sabit viewport, insan referans kabulü ve ikinci görsel koşu açık zorunluluk değil. |

## Kalan69 kaynağın okuma sırası

Bu gruplar mevcut bölüm eşlemesindeki ilk uygulamaya göre planlanır; grup başlamadan bölüm baştan sona okunmalı ve bütün hedefleri yeniden ayrıştırılmalıdır. Kaynakta bir kavram bulunması veya bir başlığın çıkarılması, hedefin öğretildiği kabul edilmez.

| Planlanan grup | Tam okuma bekleyen kaynaklar |
|---|---|
| U09-U16 | C1-B04, C1-B06, C1-B07, C1-B08, C1-B10, C1-B11, C2-B11, C2-B12, C3-B05, C3-B06, C4-B04, C4-B07, C4-B09, CC-B05, CC-B06, CC-B08, CC-B09, CC-B30, CC-B36, CC-B38 |
| U17-U24 | C1-B13, C1-B14, C2-B13, C3-B01, C3-B02, C3-B03, C3-B04, C3-B08, C3-B10, C3-B13, C4-B05, C4-B14, CC-B11, CC-B18, CC-B19, CC-B20, CC-B22, CC-B23, CC-B24, CC-B25, CC-B26, CC-B27, CC-B31, CC-B32, CC-B33 |
| U25-U32 | C1-B09, C1-B12, C1-B16, C2-B14, C3-B09, C3-B11, C3-B12, C3-B14, C4-B03, C4-B08, C4-B10, C4-B11, C4-B12, C4-B13, C4-B15, CC-B12, CC-B34, CC-B35, CC-B37, CC-B39 |
| U33-U36 | C1-B15, C1-B17, CC-B28, CC-B40 |

## Revizyon ve kaynak sorunları

Değişen8 kaynak: CC-B17, CC-B25, CC-B28, CC-B30, CC-B34, CC-B37, CC-B39, CC-B40. Pilotun değişmiş kaynağı CC-B17 güncel SHA ile okundu. Diğer7 kaynağın yeni revizyonları envantere işlendi; tam okuma yapılmış sayılmadı. Eski hashler [source-map.json](source-map.json) ve coverage kaydında korunur.

Yazar incelemesine ayrılan3 tutarsızlık [source-issues.json](source-issues.json) içindedir: C1-B05te tasarım hiyerarşisinin evrensel ürün kuralı gibi görünmesi; C2-B10da skill tasarımına yanlış bölüm numarasıyla yönlendirme; C1-B02nin hassas veri veto sorusunda liste ile örneğin sıra farkı. Ana kitaplara müdahale edilmedi.

## Kanıt ve üretim sınırı

Okuma araştırmacılarının özgün önerileri ilk P01 commit geçmişinde ve yerel `.superpowers` scratch arşivinde korunur. Birleştirme sırasında hedefe özgü kabul adayları somutlaştırıldı; çıktı üreticisi yanlış uygulamaya bağlanan yerler hedeflerin `editorial_intervention` alanında açıkça kaydedildi; ara birleştirme girdileri yerel scratch arşivindedir. Tanımsız yeni referans dosyası mevcut çıktı gibi sunulmadı. Bunlar editörün müdahaleleridir; bir üretim promptunun tek başına gözlenmiş başarısı değildir.

Paket yapısı ve editoryal bağ kontrolleri anlam incelemesinin yerine geçmez. Pilot31 kaynak metni tam okundu, hedefler kendi kısa cümlelerimizle yazıldı, pilot kabul örnekleri bağımsız ana ajan geri bildirimiyle hedefe özgü hâle getirildi. Araçların güncel resmî davranışını doğrulama ve gerçek oturum/model koşuları bu denetimin çalışma sonucu değildir.

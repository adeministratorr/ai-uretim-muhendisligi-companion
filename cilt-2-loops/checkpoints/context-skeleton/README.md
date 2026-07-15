# Context İskeleti Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 3 — Context Engineering, 3.11-3.17
(Lab 3 — Laravel + Flutter Projesi İçin Context İskeleti).

```yaml
volume: 2
chapter: 03
book_section: "3.11-3.17 Context'i Yazılı Hâle Getirme ve Proje Hafızası"
concepts:
  - codified context
  - PRD
  - TASKS.md
  - hot memory
  - cold memory
objectives:
  - "LO-3.4"
  - "LO-3.5"
last_verified: "2026-07"
```

## Ne Yapar?

Kurgusal bir Laravel backend ve Flutter mobil istemci projesi için dört başlangıç
dosyasını kurar: `PRD.md`, `TASKS.md`, `CLAUDE.md` ve `rules.md`. Doğrulayıcı şu
koşulları denetler:

- Dört dosyanın her biri en az üç madde içerir.
- En az dört bilgi hot memory veya cold memory olarak etiketlenir.
- Her hafıza etiketi kısa bir gerekçe taşır.
- Aynı hafıza maddesi iki kez yazılmaz.
- Metinde e-posta adresi veya açıkça yazılmış gizli bilgi (secret) bulunmaz.

Amaç dört dosyayı eksiksiz bir proje belgesine dönüştürmek değildir. Lab, sohbet
geçmişine bırakılan proje bilgisini küçük ve denetlenebilir bir dosya iskeletine taşır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/context-skeleton/context_skeleton.html>
İsterseniz `context_skeleton.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Dört dosyanın
maddelerini ve hafıza etiketlerini düzenleyip **İskeleti Doğrula** düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 context_skeleton.py
python3 context_skeleton.py --output ornek-context
python3 -m pytest test_context_skeleton.py
```

İlk komut gömülü örneği denetler. İkinci komut dört context dosyasını ve
`MEMORY_MAP.md` etiketleme tablosunu seçtiğiniz boş klasöre yazar. Üçüncü komut kabul
ve ret durumlarını sınar.

## Beklenen Çıktı

```text
Context İskeleti — 4 dosya / 16 madde
Hafıza Etiketleri — 5 madde (hot=4, cold=1)
Kabul kriteri karşılandı: Context iskeleti doğrulandı.
```

Tarayıcı sürümünde aynı sonuç yeşil bir kutuda gösterilir. Eksik dosya maddesi, gerekçesiz
hafıza etiketi veya hassas veri örüntüsü varsa ilgili alan açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 context_skeleton.py`).
- [x] İskelet dosyaları isteğe bağlı olarak boş bir klasöre yazılabiliyor.
- [x] Test komutu var (`pytest`, 9 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Başlangıç projesi ve bütün maddeler temsilîdir. Gerçek bir klinik, ekip veya kullanıcı
  verisi içermez; kendi iskeletinize gerçek kişisel veri eklemeyin.
- Doğrulayıcı, e-posta adreslerini ve yaygın gizli bilgi atama biçimlerini yakalar. Bir kurum
  adının veya serbest metnin gerçek kişisel veri taşıyıp taşımadığını kesin olarak
  belirleyemez; insan incelemesi gerekir.
- Bir maddenin hot veya cold olarak işaretlenmesi, onun doğru yerde tutulduğunu tek başına
  kanıtlamaz. Sık kullanılan kısa bilgiler hot; ayrıntılı karar geçmişi gerektiğinde
  çağrılan cold katmanda tutulmalıdır.
- Bu dosyalar başlangıç iskeletidir. Tam PRD ve kural dosyası tasarımı Cilt 2, Bölüm 8 ve
  Bölüm 9'un kapsamındadır.

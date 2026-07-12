---
volume: 1
chapter: 16
book_section: "AI Odaklı Kültür"
concepts:
  - AI okuryazarlığı seviyeleri
  - rol bazlı yetkinlik haritası
  - kurum çapında prompt kütüphanesi
  - iç şampiyon
objectives:
  - "LO-16.2"
  - "LO-16.3"
  - "LO-16.4"
last_verified: "2026-07"
---

# Ekip Yetkinlik Matrisi Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 16 — AI Odaklı Kültür, 16.2, 16.3 ve 16.4
(rol bazlı yetkinlik haritası, beş rol ailesi için beceri setleri, kurum çapında prompt
kütüphanesi).

## Ne Yapar?

Bölüm 16'nın dersi, bir kurumdaki AI okuryazarlığının tek bir eşik değil, role göre
değişen kademeli bir harita olduğudur. 16.2-16.3, her rolü (öğretmen, yönetici, analist,
geliştirici, operasyon) günlük işinde gerçekten ihtiyaç duyduğu beceriyle ve hedeflenen
okuryazarlık seviyesiyle eşleştirir; 16.4 bu bilginin ekip düzeyinde kalmaması için
kurum çapında yönetilen bir prompt kütüphanesi kurar.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, bu iki fikri iki bağımsız denetime
dönüştürür:

- `competency_matrix.py` / `evaluate_team`: ekip üyesi × yetkinlik alanı ızgarasını
  tarar; her yetkinlik alanı için hiç kimsenin hedef seviyeye ulaşmadığı **boşlukları**
  ve yalnızca tek kişinin karşıladığı **tek nokta risklerini** (o kişi ayrılırsa alan
  boşalır) listeler.
- `competency_matrix.py` / `validate_library_entry`: 16.4'teki kurum çapında prompt
  kütüphanesi kaydının **başlık**, **sahip**, **kullanım alanı** ve **son doğrulama
  tarihi** zorunlu alanlarını denetler; tarih biçimini ve 16.5'teki yıllık gözden
  geçirme ilkesiyle tutarlı bir güncellik penceresini (365 gün) kontrol eder.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/exercises/competency-matrix/competency_matrix.html>
İsterseniz `competency_matrix.html` dosyasını indirip çift tıklayarak da açabilirsiniz;
kurulum, terminal veya internet bağlantısı gerekmez. Örnek ekibi/kayıtları yükleyin veya
kendi ekibinizin adlarını ve seviyelerini girin; boşluk, tek nokta riski ve kayıt eksikleri
canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `competency_matrix.py` dosyasındadır.
Şablonları kopyalayıp kendi ekibinizi ve kayıtlarınızı doldurun:

```bash
cp team_template.json benim_ekibim.json
cp library_template.json benim_kutuphanem.json
python3 competency_matrix.py benim_ekibim.json --library benim_kutuphanem.json
```

Hazır örneği görmek için:

```bash
python3 competency_matrix.py
python3 -m pytest -q
```

## Beklenen Çıktı (özet)

```text
Ekip Yetkinlik Matrisi:
TEK NOKTA RİSKİ — Ders materyali ve etkinlik hazırlama: yalnızca Elif Turan hedefi karşılıyor.
YETERLİ — Rapor, yazışma ve veli iletişimi: 2 kişi hedefi karşılıyor.
TEK NOKTA RİSKİ — Veri yorumu ve doğrulama disiplini: yalnızca Selen Kaya hedefi karşılıyor.
BOŞLUK — Model/araç seçimi ve entegrasyon: hedef 'sistematik_entegrasyon', ekipte hiç kimse bu seviyeye ulaşmıyor.
YETERLİ — Standart yazışma, form ve özet metni üretme: 2 kişi hedefi karşılıyor.

Prompt Kütüphanesi Kayıtları:
[geçti] Ders Planı Taslağı Standardı
[revizyon gerekli] Veli Bilgilendirme Yazışması Standardı
  - `son_dogrulama_tarihi` 365 günden eski; yıllık gözden geçirmeden geçmemiş olabilir.
[revizyon gerekli] Dönem Başarı Eğilimi Analizi Standardı
  - `sahip` alanı boş bırakılmamalıdır.
[revizyon gerekli] (başlıksız kayıt)
  - `baslik` alanı boş bırakılmamalıdır.
  - `kullanim_alani` alanı boş bırakılmamalıdır.
  - `son_dogrulama_tarihi` YYYY-AA-GG biçiminde geçerli bir tarih olmalıdır.
```

Örnek ekipte hiç kimse "model/araç seçimi ve entegrasyon" alanında değerlendirilmemiş —
bu, tek bir okulun kadrosunda ayrı bir BT/geliştirici kaynağı bulunmadığında ortaya çıkan
gerçekçi bir boşluk örneğidir. Örnek kütüphanede dört kayıttan yalnızca biri tüm
kontrollerden geçer; diğerleri eksik alan, eski tarih veya bozuk tarih biçimi taşır.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3, gerçek API çağrısı yok).
- [x] Örnek çalışıyor (`python3 competency_matrix.py`).
- [x] Test/doğrulama komutu var (`pytest`, 11 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu araç bir kurumun AI kültürünü veya eğitim programını otomatik onaylamaz; yalnızca
  doldurduğunuz ızgaradaki boşlukları, tek nokta risklerini ve kayıt eksiklerini
  görünür kılar.
- "Tek nokta riski" tespiti yalnızca doldurulan hücrelere bakar; hiç değerlendirilmemiş
  bir ekip üyesi "farkındalık" değil, "değerlendirilmedi" sayılır — bu, gerçek bir
  eksikliği yanlışlıkla "boşluk" olarak büyütmemek içindir, ama ekibinizi tam
  doldurmazsanız sonuç iyimser görünebilir.
- Prompt kütüphanesi denetiminde kullanılan referans tarih (2026-07-01) ve 365 günlük
  güncellik penceresi temsilîdir; Python sürümünde `--today` bayrağıyla gerçek tarihi
  geçebilirsiniz, HTML sürümü ise sabit referans tarihle çalışır.
- Yetkinlik alanları, 16.3'teki beş rol ailesinin "temel AI becerisi" sütunundan
  türetilmiş beş temsilî alandır; gerçek bir kurumun yetkinlik haritası daha fazla
  alan ve alt beceri içerebilir.

# GUI Araçla MVP Deneyi Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 5 — GUI Tabanlı AI Geliştirme Araçları, 5.8
(Lab 5 — 45 Dakikada Bir MVP Prototipi).

```yaml
volume: 2
chapter: 05
book_section: "5.8 GUI Araç Seçim Matrisi"
concepts:
  - GUI coding agent
  - MVP prototipleme
  - müdahale noktası
  - teknik borç
objectives:
  - "LO-5.1"
  - "LO-5.2"
  - "LO-5.3"
  - "LO-5.4"
  - "LO-5.5"
  - "LO-5.6"
last_verified: "2026-07"
```

## Ne Yapar?

Bir GUI coding agent ile yürüttüğünüz 45 dakikalık MVP denemesini ortak bir kayıt
biçimine dönüştürür. Doğrulayıcı şu koşulları denetler:

- MVP fikri 3-4 tamamlanmış cümleyle tarif edilmiştir.
- En az bir otomatik tamamlanan adım ve bir müdahale noktası kaydedilmiştir.
- İstenen küçük değişiklik ile aracın bu isteğe verdiği sonuç yazılmıştır.
- Kodun incelenip incelenemediği ve bu kararın gerekçesi belirtilmiştir.
- Deney 45 dakika sürmüştür; kota nedeniyle erken bittiyse bu durum ayrıca işaretlenmiştir.
- Araç için tek cümlelik bir dikkat noktası yazılmıştır.

Laboratuvar araca genel bir puan vermez. Kayıt, hızın yanında müdahale ve denetlenebilirlik
maliyetini de gösterir; araç seçimi yine insanın vereceği bir karardır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/gui-mvp-evaluation/gui_mvp_lab.html>
İsterseniz `gui_mvp_lab.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Kendi denemenizdeki
gözlemleri yazıp **Deney Kaydını Doğrula** düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 gui_mvp_lab.py
python3 -m pytest test_gui_mvp_lab.py
```

İlk komut temsilî bir deney kaydını denetler. İkinci komut eksik gözlemin, geçersiz
sürenin ve gerekçesiz kod inceleme kararının reddedildiğini sınar.

## Beklenen Çıktı

```text
GUI Araçla MVP Deneyi — Örnek Araç / 45 dakika
Otomatik tamamlanan adım: 2
Müdahale gereken nokta: 1
Küçük değişiklik sonucu: uygulandı
Kod inceleme durumu: incelendi
Dikkat noktası: Hesap ayrımını yalnızca önizlemeden değil, kod ve veri kurallarından da doğrulamak gerekir.
Kabul kriteri karşılandı: Deney kaydı tamam.
```

Tarayıcı sürümünde aynı özet yeşil bir sonuç kutusunda gösterilir. Eksik veya geçersiz
bir alan varsa ilgili ölçüt açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 gui_mvp_lab.py`).
- [x] Test komutu var (`pytest`, 18 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü araç adı ve gözlemler temsilîdir. Gerçek bir ürün denemesi, performans ölçümü
  veya benchmark değildir; kendi kaydınızla değiştirilmelidir.
- Laboratuvar bir GUI aracı çalıştırmaz ve dış servise bağlanmaz. Prototipi seçtiğiniz
  araçta üretir, gözlemleri burada kaydedersiniz.
- Kodun incelendiğini işaretlemek güvenlik denetiminin tamamlandığını kanıtlamaz.
  Kimlik doğrulama, veri ayrımı, gizli anahtarlar ve bağımlılıklar ayrıca sınanmalıdır.
- Ücretsiz planların kota ve özellikleri değişebilir. Güncel koşulları aracın resmî
  sayfasından kontrol edin. Son doğrulama: 2026-07.
- Gerçek kişisel veri, müşteri verisi veya gizli anahtar deneme aracına yüklenmemelidir.

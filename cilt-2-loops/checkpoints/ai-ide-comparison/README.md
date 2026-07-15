# AI IDE Karşılaştırma Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 4 — AI IDE'ler, 4.9
(Uygulama 4 — Aynı Özelliği Birden Fazla AI IDE'de Denemek).

```yaml
volume: 2
chapter: 04
book_section: "4.9 AI IDE Seçim Matrisi"
concepts:
  - AI IDE
  - ortak görev tarifi
  - diff okunabilirliği
  - insan karar noktası
objectives:
  - "LO-4.4"
  - "LO-4.5"
  - "LO-4.6"
last_verified: "2026-07"
```

## Ne Yapar?

Aynı geliştirme görevini 2 veya 3 AI IDE'de denedikten sonra sonuçları ortak
bir kayıt altında toplar. Doğrulayıcı şu koşulları denetler:

- Bütün araçlarda aynı görev tarifi ve en az 2 ortak kabul ölçütü kullanılmıştır.
- Araç adları birbirinden farklıdır.
- İlk taslağın ortak testten geçip geçmediği kaydedilmiştir.
- Düzeltme turu sayısı 0 veya daha büyük bir tam sayıdır.
- Diff okunabilirliği 1-5 aralığında değerlendirilmiştir.
- Her araç için bir sürpriz veya hata ile tek cümlelik öne çıkan özellik yazılmıştır.

Doğrulama geçerse ilk testi geçen araçlar, en az düzeltme turu ve en yüksek diff
okunabilirliği ayrı ayrı gösterilir. Laboratuvar bu ölçümleri tek puanda birleştirmez;
araç seçimi, görev ve veri politikasıyla birlikte insanın vereceği bir karardır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/ai-ide-comparison/ide_comparison_lab.html>
İsterseniz `ide_comparison_lab.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Görev tarifini,
kabul ölçütlerini ve iki araçtaki gözlemlerinizi yazıp **Karşılaştırmayı Doğrula**
düğmesine basın. Üçüncü araç isteğe bağlıdır.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 ide_comparison_lab.py
python3 -m pytest test_ide_comparison_lab.py
```

İlk komut temsilî iki araç kaydını denetler. İkinci komut eksik alanın, yinelenen araç
adının ve geçersiz ölçümün reddedildiğini sınar.

## Beklenen Çıktı

```text
AI IDE Karşılaştırması — 2 araç / 3 ortak kabul ölçütü
Araç A: ilk test=geçmedi, düzeltme turu=1, diff okunabilirliği=4/5
Araç B: ilk test=geçti, düzeltme turu=0, diff okunabilirliği=3/5
En az düzeltme turu: Araç B (0)
En yüksek diff okunabilirliği: Araç A (4/5)
Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.
```

Tarayıcı sürümünde aynı sonuç yeşil bir kutuda gösterilir. Eksik veya geçersiz bir alan
varsa ilgili araç ve alan adı açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 ide_comparison_lab.py`).
- [x] Test komutu var (`pytest`, 13 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü araç adları ve sonuçlar temsilîdir; gerçek bir ürün karşılaştırması veya
  benchmark değildir. Kendi denemenizde bu kayıtları silip gözlemlerinizi yazın.
- Adil bir karşılaştırma için görev tarifi, başlangıç kodu ve test komutu bütün araçlarda
  aynı tutulmalıdır. Model, plan, uzantı ve izin farkları ayrıca not edilmelidir.
- Diff okunabilirliği öznel bir değerlendirmedir. Farklı geliştiriciler aynı diff'e farklı
  puan verebilir.
- İlk testin geçmesi, kodun güvenli veya üretime hazır olduğunu kanıtlamaz. Diff incelemesi,
  ek testler ve insan onayı korunmalıdır.
- Hassas kodu veya kişisel veriyi bir araca yüklemeden önce kurumun veri politikasını ve
  aracın güncel kullanım koşullarını kontrol edin.

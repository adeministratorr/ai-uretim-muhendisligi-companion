# Sorumluluk Matrisi Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 1 — Yazılım Dünyasının Dönüşümü, 1.9
(Uygulama 1 — Sorumluluk Matrisi).

```yaml
volume: 2
chapter: 01
book_section: "1.9 Bu Kitabın Kullanım Yöntemi"
concepts:
  - Sorumluluk Matrisi
  - insan denetimi
  - onay noktası
objectives:
  - "LO-1.6"
last_verified: "2026-07"
```

## Ne Yapar?

Bir geliştirme sürecindeki görevleri beş başlık altında sınıflandırır: görev, yapay zekâya
devredilen iş, geliştiricide kalan sorumluluk, birlikte yürütülen iş ve insan denetiminin
gerekçesi. Doğrulayıcı şu koşulları denetler:

- Matris 5-8 görev içerir.
- Her görevde üç sorumluluk alanı da doldurulmuştur.
- Geliştiricide kalan her sorumluluk için bir gerekçe cümlesi vardır.
- Aynı görev iki kez yazılmamıştır.

Bu sınıflandırma bir onay noktasıdır (checkpoint). Araç görevi yürütebilir; kabul veya ret
kararının kimde kaldığı matris üzerinden açıkça görülür.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/responsibility_matrix.html>
İsterseniz `responsibility_matrix.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Örnek satırları kendi
iş akışınıza göre değiştirip **Matrisi Doğrula** düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 responsibility_matrix.py
python3 -m pytest test_responsibility_matrix.py
```

İlk komut temsilî matrisi denetler. İkinci komut geçerli matrisin kabul edildiğini ve eksik,
kısa ya da yinelenen kayıtların reddedildiğini sınar.

## Beklenen Çıktı

```text
Sorumluluk Matrisi — 6 görev
Kabul kriteri karşılandı: 6 görevin sorumluluk alanları ve gerekçeleri tamam.
```

Tarayıcı sürümünde aynı denetim yeşil bir sonuç kutusuyla gösterilir. Eksik bir alan varsa
ilgili satır ve alan adı açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 responsibility_matrix.py`).
- [x] Test komutu var (`pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Örnek satırlar temsilîdir. Her ekip kendi veri hassasiyetine, yetki sınırlarına ve
  üretim riskine göre matrisi yeniden doldurmalıdır.
- Matris bir güvenlik denetimi veya yetki sistemi değildir; sorumluluk dağılımını görünür
  kılan bir karar tablosudur.
- Bir hücrenin dolu olması, görevin doğru yürütüldüğünü kanıtlamaz. Diff incelemesi, test
  ve insan onayı ayrı doğrulama adımları olarak korunmalıdır.
- Araç, proje veya ekip değiştiğinde matris yeniden gözden geçirilmelidir.

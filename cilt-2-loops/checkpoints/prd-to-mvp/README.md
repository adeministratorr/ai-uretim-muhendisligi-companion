# PRD'den MVP'ye Araç Zincirleme Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 11 — Gerçek Dünya Vibe Coding İş Akışları,
11.1 ve 11.4 (Lab 11 — PRD'den Çalışan MVP'ye).

```yaml
volume: 2
chapter: 11
book_section: "11.1 Sıfırdan MVP Geliştirme"
concepts:
  - araç zincirleme
  - kabul kriteri
  - insan denetimi
  - yapılandırılmış hata
objectives:
  - "LO-11.1"
  - "LO-11.3"
  - "LO-11.5"
last_verified: "2026-07"
```

## Ne Yapar?

Bir PRD kabul kriterini iskelet, derinleştirme ve test aşamalarından geçirir. Örnek
kriter şudur: "Aynı çalışana çakışan iki vardiya atanamaz." Laboratuvar iki parçayı
birlikte çalıştırır:

- Saf Python uygulaması, çakışan vardiyayı reddeder; geçersiz alanı ve sonraki adımı
  ayrı alanlarda taşıyan yapılandırılmış hata üretir.
- Araç zincirleme (tool chaining) kaydı, GUI aracı → AI IDE → CLI ajan sırasındaki
  görev, süre, gözlem ve insan kararını denetler.

Kayıt ya üç araç kategorisinin tamamını sırasıyla kullanmalıdır ya da erişiminiz olan
tek kategoriyle üç aşamayı yürütmelidir. Her iki yolda da en az bir araç çıktısı
düzeltilmeli veya reddedilmeli, en az iki test çalışmalı ve bütün testler geçmelidir.

Laboratuvar araçları kendi başına çağırmaz. Kendi aracınızda yaptığınız denemenin
sonucunu forma siz yazarsınız; doğrulayıcı kaydın eksik bırakılıp bırakılmadığını ölçer.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/prd-to-mvp/prd_to_mvp_lab.html>
İsterseniz `prd_to_mvp_lab.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Önce vardiya
kuralını deneyin. Ardından üç aşamadaki gerçek görev ve gözlemlerinizi yazıp
**Kaydı Doğrula** düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterini ve örnek araç zincirini saf Python ile
çalıştırın.

```bash
python3 prd_to_mvp_lab.py
python3 -m pytest test_prd_to_mvp_lab.py
```

İlk komut üç kabul senaryosunu çalıştırır, aşama kaydını denetler ve çakışan vardiya
için örnek hata gövdesini gösterir. İkinci komut çakışma kuralını, tek araç seçeneğini,
üç araç sırasını, düzeltme zorunluluğunu ve HTML eşleniğini sınar.

## Beklenen Çıktı

```text
PRD'den MVP'ye Araç Zincirleme Kaydı
PRD kabul kriteri: Aynı çalışana çakışan iki vardiya atanamaz.
Aşama kaydı: 3/3
Araç yolu: GUI aracı → AI IDE → CLI ajan
Düzeltilen veya reddedilen çıktı: 1
Kabul testleri: 3/3 geçti
Kabul kriteri karşılandı: Üç aşama kaydedildi, bir çıktı düzeltildi ve testler geçti.
Örnek hata gövdesi:
{
  "error": "shift_overlap",
  "field": "start_minute,end_minute",
  "message": "Aynı çalışana çakışan iki vardiya atanamaz; başlangıç veya bitiş saatini değiştirin.",
  "expected": "Mevcut vardiyalarla örtüşmeyen zaman aralığı"
}
```

Tarayıcı sürümü, vardiya kararını ve aşama kaydının sonucunu ayrı kutularda gösterir.
Eksik aşama, doğrulanmamış çıktı veya geçmeyen test varsa nedeni açıkça yazar.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 prd_to_mvp_lab.py`).
- [x] Test komutu var (`pytest`).
- [x] Beklenen çıktı ve yapılandırılmış hata örneği gösteriliyor.
- [x] Üç aşamanın görev, süre, gözlem ve insan kararı kaydediliyor.
- [x] Üç kategorili yol ile tek kategorili alternatif ayrı ayrı doğrulanıyor.
- [x] En az bir düzeltme veya ret ve en az iki geçen test zorunlu tutuluyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü araç adları, süreler ve aşama sonuçları temsilîdir. Bir ürünün hızını veya
  başarısını ölçmez.
- Formdaki "çıktı doğrulandı" seçimini araç denetlemez. Diff'i, ekranı ve test
  çıktısını insan inceleyip kaydeder.
- Vardiya örneği tek gün içindeki dakika aralıklarını işler. Gece yarısını aşan
  vardiyalar, saat dilimleri ve veri tabanı eşzamanlılığı kapsam dışıdır.
- Yapılandırılmış hata, bir API sözleşmesinin küçük örneğidir; kimlik doğrulama,
  yetkilendirme ve HTTP durum kodlarının yerini tutmaz.
- Testlerin geçmesi, PRD'nin bütün kapsamının tamamlandığını kanıtlamaz. İnsan onayı
  ve diff incelemesi ayrı adımlar olarak korunmalıdır.

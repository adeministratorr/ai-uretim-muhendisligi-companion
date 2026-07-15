# Bakım Loop'u Tasarım Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 13 — Loop Engineering: Ajan Döngüleri
Tasarlamak, 13.3, 13.12-13.15 ve 13.24-13.26 (Lab 13 — Bir Bakım Loop'u
Tasarlamak).

```yaml
volume: 2
chapter: 13
book_section: "13.3 Loop Specification ve 13.12-13.15 Doğrulama, Durdurma ve İz"
concepts:
  - loop specification
  - verification ladder
  - terminal state
  - bütçe
  - trace
objectives:
  - "LO-13.2"
  - "LO-13.3"
  - "LO-13.4"
  - "LO-13.5"
  - "LO-13.6"
  - "LO-13.7"
last_verified: "2026-07"
```

## Ne Yapar?

Kurgusal Vardiya projesinin haftalık bakım işi için tam bir loop specification
(döngü tanımı) kurar ve beş terminal state'i aynı kurallarla değerlendirir:

- Tetikleyici, hedef, doğrulama merdiveni, durdurma kuralları ve hafıza alanlarının
  eksiksiz yazıldığını denetler.
- En az iki kademeli doğrulama merdivenini tanımlı sırayla işletir.
- `done`, `blocked`, `needs-review`, `unsafe` ve `budget-exceeded` durumlarını
  birbirinden ayırır.
- Teknik kontroller geçtiği hâlde hedef davranış karşılanmadıysa sonucu `done`
  saymaz; insan incelemesine gönderir.
- Her değerlendirmeyi, kararın gerekçesini taşıyan kısa bir trace (iz) kaydına
  dönüştürür.

Python ve HTML sürümleri aynı temsilî specification'ı kullanır. Dış servis çağrısı,
model veya API anahtarı gerekmez.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/debug-loops/maintenance-loop/maintenance_loop.html>
İsterseniz `maintenance_loop.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Beş koşuldan birini seçip **Koşulu Değerlendir** düğmesine basın. Doğrulama
merdiveninin sonucunu, terminal state'i ve insan onayı kararını karşılaştırın.

**Kod biliyorsanız:** Aynı kuralları saf Python ile çalıştırın.

```bash
python3 maintenance_loop.py
python3 -m pytest test_maintenance_loop.py
```

İlk komut beş terminal state için birer temsilî koşul üretir. İkinci komut eksik
specification'ın reddedildiğini, doğrulama sırasının korunduğunu, bütçe sınırının
çalıştığını ve yüzeysel test başarısının hedef davranışın yerine geçmediğini sınar.

## Beklenen Çıktı

```text
Bakım Loop'u Karar Raporu
done: test paketi ve davranış kontrolü geçti.
blocked: paket kayıt defterine erişilemiyor.
needs-review: teknik kontroller geçti; iş mantığı yorumu gerekiyor.
unsafe: yetkilendirme dosyasına dokunuldu; otomatik işlem durdu.
budget-exceeded: 3 deneme veya 30 dakika sınırı aşıldı.
Terminal state kapsamı: 5/5
```

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile
  çalışıyor.
- [x] Specification; tetikleyici, hedef, doğrulama, durdurma kuralı ve hafıza
  alanlarını taşıyor.
- [x] Doğrulama merdiveni en az iki kademeden oluşuyor ve sıra değişikliği
  reddediliyor.
- [x] Beş terminal state ayrı koşullarla üretilebiliyor.
- [x] `needs-review` ve `unsafe` otomatik geçilmeyen insan onay noktaları olarak
  tanımlanıyor.
- [x] Deneme ve süre bütçesi `budget-exceeded` durumunu tetikliyor.
- [x] Başarısız kontrol bütçe dolmadan önce yeni tur için `running` durumunda
  kalıyor; sonsuz döngüye izin verilmiyor.
- [x] Teknik kontroller geçse bile hedef davranış karşılanmadığında `done`
  üretilmiyor.
- [x] Test komutu ve beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Senaryo ve eşikler temsilîdir. Üç deneme ile 30 dakika her bakım işi için uygun
  değildir; sınırlar işin kapsamına ve riskine göre belirlenmelidir.
- Laboratuvar gerçek bir zamanlayıcı, Git worktree veya CI sistemi başlatmaz.
  Yazılı specification'ın ve çalışma gözleminin tutarlılığını gösterir.
- Formdaki kontrol sonuçları gerçek test komutlarından okunmaz. Gerçek projede her
  kademe, ilgili komutun çıkış kodu ve kanıtıyla beslenmelidir.
- `unsafe` sınıflandırması yalnızca örnekteki hassas alan işaretine dayanır. Gerçek
  izin ve güvenlik kuralları ayrıca uygulanmalıdır.
- Testlerin geçmesi, iş mantığı ve güvenlik incelemesinin yerini tutmaz. İnsan onay
  noktaları otomatik olarak geçilmemelidir.

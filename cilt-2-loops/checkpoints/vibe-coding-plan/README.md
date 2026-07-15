# Plan Karşılaştırma Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 2 — Vibe Coding Felsefesi, 2.9 ve 2.15-2.20
(Lab 2 — Geleneksel Plan ile Vibe Coding Planı Karşılaştırması).

```yaml
volume: 2
chapter: 02
book_section: "2.9 İterasyon Döngüsü"
concepts:
  - vibe coding
  - mise en place
  - insan onay noktası
  - verification-driven development
objectives:
  - "LO-2.3"
  - "LO-2.6"
last_verified: "2026-07"
```

## Ne Yapar?

Aynı geliştirme görevi için geleneksel planı ve vibe coding planını yan yana kurar.
Doğrulayıcı şu koşulları denetler:

- İki plan da 5-8 benzersiz adım içerir.
- Her adımın açıklaması, süre tahmini ve belirsizlik düzeyi vardır.
- Vibe coding planında en az bir mise en place adımı bulunur.
- Vibe coding planında en az bir test/doğrulama adımı bulunur.
- Vibe coding planında en az bir insan onay noktası bulunur.

Doğrulama geçerse iki planın toplam süre tahmini, ortalama belirsizlik düzeyi ve vibe
coding planındaki denetim işaretleri özetlenir. Amaç en kısa planı seçmek değildir;
niyetin, doğrulamanın ve insan sorumluluğunun planda açıkça yer alıp almadığını görmektir.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/vibe-coding-plan/plan_comparison.html>
İsterseniz `plan_comparison.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Örnek adımları kendi
görevinize göre değiştirin, gerekli denetim işaretlerini seçin ve **Planları Doğrula**
düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 plan_comparison.py
python3 -m pytest test_plan_comparison.py
```

İlk komut, telefon alanı doğrulaması için hazırlanmış temsilî iki planı denetler. İkinci
komut eksik adımın, geçersiz süre tahmininin ve atlanan denetim noktasının reddedildiğini
sınar.

## Beklenen Çıktı

```text
Plan Karşılaştırması — Geleneksel: 5 adım / 95 dakika
Plan Karşılaştırması — Vibe coding: 5 adım / 50 dakika
Vibe coding denetim işaretleri: mise en place=1, doğrulama=1, insan onayı=1
Kabul kriteri karşılandı: İki plan da karşılaştırmaya hazır.
```

Tarayıcı sürümünde aynı sonuç, iki planın süre ve belirsizlik özetleriyle birlikte yeşil
bir sonuç kutusunda gösterilir. Eksik bir ölçüt varsa ilgili plan ve adım açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 plan_comparison.py`).
- [x] Test komutu var (`pytest`, 9 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Örnek planlar, süreler ve belirsizlik düzeyleri temsilîdir. Bir ekip ölçümü veya
  verimlilik karşılaştırması değildir.
- Düşük süre tahmini, planın daha güvenli ya da daha doğru olduğunu göstermez. Kritik bir
  görevde test, diff incelemesi ve insan onayı ayrıca uygulanmalıdır.
- Denetim işaretinin seçilmesi, adımın gerçekten yürütüldüğünü kanıtlamaz. Laboratuvar
  planın yapısını denetler; uygulama sonucunu denetlemez.
- Human-out-of-the-loop düzeyi bu örneğin kabul kriteri değildir. Üretime gidecek kodda
  insan onayı korunmalıdır.

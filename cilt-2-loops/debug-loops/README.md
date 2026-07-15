# Minimal Repro'dan Düzeltmeye Hata Ayıklama Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 12 — Hata Ayıklama ve Versiyon Kontrolü,
12.5 ve 12.9 (Uygulama 12 — Lab 12: Bozuk Bir Vardiya Projesini Ayıklama).

```yaml
volume: 2
chapter: 12
book_section: "12.5 Minimal Repro Hazırlama ve 12.9 Testle Doğrulama"
concepts:
  - minimal repro
  - açıkla-hipotez kur-kanıt göster
  - failing test
  - fix
  - regression
objectives:
  - "LO-12.2"
  - "LO-12.3"
  - "LO-12.4"
last_verified: "2026-07"
```

## Ne Yapar?

Kurgusal Vardiya projesindeki değişebilir varsayılan argüman (mutable default
argument) hatasını küçük ve tekrarlanabilir bir örneğe indirger. Aynı işlem iki ayrı
plan için çalıştırıldığında bozuk sürümün tek bir listeyi paylaştığını gösterir:

- Minimal repro, ikinci planın neden birinci planın vardiyasını da taşıdığını üretir.
- Hata izi, iki planın bellekte aynı listeyi kullandığını kimlik karşılaştırmasıyla
  kanıtlar.
- Düzeltilmiş sürüm, `assigned=None` kalıbını kullanır ve çağıranın verdiği boş listeyi
  korur.
- Rapor, failing test ile fix için iki ayrı commit önerir; regresyonu commit değil,
  doğrulama notu olarak kaydeder.

Python ve HTML sürümleri aynı senaryoyu çalıştırır. Dış servis çağrısı, model veya API
anahtarı gerekmez.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/debug-loops/debug_loop_lab.html>
İsterseniz `debug_loop_lab.html` dosyasını indirip çift tıklayarak da açabilirsiniz.
Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez. Önce **Hatayı Yeniden
Üret**, ardından **Düzeltmeyi Doğrula** düğmesine basın. İki planın vardiya listelerini
ve aynı listeyi paylaşıp paylaşmadıklarını karşılaştırın.

**Kod biliyorsanız:** Aynı minimal repro'yu ve güvenli düzeltmeyi saf Python ile
çalıştırın.

```bash
python3 debug_loop_lab.py
python3 -m pytest test_debug_loop_lab.py
```

İlk komut beklenen davranış, gerçek davranış, hata izi, hipotez, kanıt ve düzeltme
sonucunu gösterir. İkinci komut hatanın yeniden üretildiğini, güvenli düzeltmenin planları
ayırdığını, çağıranın verdiği boş listenin korunduğunu ve HTML eşleniğinin gerekli
açıklama ile bağlantıları taşıdığını sınar.

## Beklenen Çıktı

```text
Minimal Repro'dan Düzeltmeye Hata Ayıklama Döngüsü
Beklenen davranış: ikinci plan yalnızca B vardiyasını içerir.
Gerçek davranış: ikinci plan A, B vardiyalarını içeriyor.
Hata izi: birinci ve ikinci plan aynı listeyi kullanıyor: evet
Hipotez: değişebilir varsayılan liste çağrılar arasında paylaşılıyor.
Kanıt: assigned listesi fonksiyon oluşturulurken bir kez üretildi.
Düzeltme: assigned=None; yalnızca None geldiğinde yeni liste oluştur.
Düzeltme sonrası: ikinci plan yalnızca B vardiyasını içeriyor.
Regression: 3/3 kontrol geçti.
Commit 1: test: ayrı planların vardiya listesini paylaşmadığını kanıtla
Commit 2: fix: varsayılan vardiya listesini her çağrıda oluştur
```

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Hata iki ayrı plan ve iki vardiyadan oluşan minimal repro ile yeniden üretiliyor.
- [x] Beklenen davranış, gerçek davranış ve hata izi ayrı ayrı gösteriliyor.
- [x] Hipotez, iki planın aynı listeyi paylaştığı gözlemiyle kanıtlanıyor.
- [x] Düzeltme `assigned=None` kalıbını kullanıyor; `assigned = assigned or []`
  kullanılmıyor.
- [x] Failing test ve fix için iki ayrı commit öneriliyor; regresyon için boş commit
  önerilmiyor.
- [x] Test komutu ve beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Senaryo temsilîdir. Gerçek projelerde aynı belirti önbellek, uygulama genelinde
  paylaşılan durum veya veri tabanı oturumu gibi başka kaynaklardan da doğabilir.
- Bozuk fonksiyon, her denemede boş bir listeyle başlamak için laboratuvar içinde yeniden
  oluşturulur. Uygulama kodunda kullanılmamalıdır.
- Laboratuvar Git commit'i oluşturmaz. Önerilen iki mesajı kendi çalışma dalınızda,
  önce failing test sonra fix sırasıyla siz uygularsınız.
- Testlerin geçmesi yalnızca bu küçük davranışı doğrular. Diff, güvenlik ve mimari
  incelemesinin yerini tutmaz.
- HTML sürümü Python kodunu çalıştırmaz; aynı durumu tarayıcıda JavaScript ile yeniden
  kurar. Python sürümü test edilmiş başvuru uygulamasıdır.

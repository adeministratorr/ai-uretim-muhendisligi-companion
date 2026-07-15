# Model Çıktısı Karşılaştırma Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 7 — Güncel Model Ekosistemi, 7.10
(Lab 7 — Aynı Görevi Modellerle Karşılaştırmak).

```yaml
volume: 2
chapter: 07
book_section: "7.10 Kod Benchmark'larının Sınırları"
concepts:
  - ortak görev tarifi
  - model karşılaştırması
  - bağlam penceresi
  - insan denetimi
objectives:
  - "LO-7.1"
  - "LO-7.2"
  - "LO-7.3"
  - "LO-7.5"
  - "LO-7.6"
last_verified: "2026-07"
```

## Ne Yapar?

Aynı `normalize_labels` refactor görevini iki veya üç model ya da model katmanıyla
çalıştırdıktan sonra gözlemleri ortak bir kayıtta toplar. Doğrulayıcı şu koşulları
denetler:

- Her deneme aynı hedef fonksiyon için bir diff içerir.
- Test sonucu, değişen dosya sayısı ve dışa açık arayüzün korunup korunmadığı yazılmıştır.
- Okunabilirlik puanı kısa bir gerekçeyle desteklenmiştir.
- Çağrı sayısı ve bağlamın yeterli olup olmadığı ayrı ölçütler olarak kaydedilmiştir.
- Tercih notu test, arayüz, okunabilirlik, çağrı ve bağlam gözlemlerine dayanır.

Laboratuvar genel bir benchmark skoru üretmez. Karar, kendi görev setinizde gözlediğiniz
sonuçlara dayanır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/model-comparison/model_comparison_lab.html>
İsterseniz `model_comparison_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Örnek kayıtları kendi denemelerinizle değiştirip **Karşılaştırmayı Doğrula** düğmesine
basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 model_comparison_lab.py
python3 -m pytest test_model_comparison_lab.py
```

İlk komut iki temsilî deneme kaydını doğrular. İkinci komut eksik diff'in, yinelenen
deneme etiketinin, geçersiz ölçütlerin ve gözleme dayanmayan tercih notunun
reddedildiğini sınar.

## Beklenen Çıktı

```text
Model Çıktısı Karşılaştırması — 2 deneme
Deneme A: test=geçti, dosya=1, arayüz=korundu, okunabilirlik=4/5, çağrı=2, bağlam=yeterli
Deneme B: test=geçti, dosya=1, arayüz=korundu, okunabilirlik=5/5, çağrı=3, bağlam=yeterli
Testleri geçen deneme: 2/2
Arayüzü koruyan deneme: 2/2
Bağlamı yeterli deneme: 2/2
Karar notu: Deneme B'yi seçtim; testler geçti, dışa açık arayüz korundu ve okunabilirlik notu daha güçlüydü. İki denemede de bağlam yeterliydi; Deneme A daha az çağrı kullansa da bu fark tek başına kararı belirlemedi.
Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.
```

Tarayıcı sürümünde aynı özet yeşil bir sonuç kutusunda gösterilir. Eksik veya geçersiz
bir alan varsa ilgili deneme ve ölçüt açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 model_comparison_lab.py`).
- [x] Test komutu var (`pytest`).
- [x] Beklenen çıktı gösteriliyor.
- [x] İki veya üç deneme aynı görev ve kabul ölçütleriyle karşılaştırılıyor.
- [x] Bölüm 7.7'den en az iki seçim ölçütü kaydediliyor: çağrı sayısı ve bağlam yeterliliği.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü diff'ler ve ölçümler temsilîdir. Gerçek bir model denemesi, performans ölçümü
  veya benchmark değildir; kendi denemenizde bu kayıtları değiştirin.
- Laboratuvar bir model çağırmaz ve yapıştırılan diff'i çalıştırmaz. Diff'i ayrı bir
  çalışma dalında uygulayın, testleri orada çalıştırın ve sonucu forma kendiniz yazın.
- Okunabilirlik puanı öznel bir gözlemdir. Puanın yanına somut gerekçe yazılması bu
  öznelliği azaltır, ortadan kaldırmaz.
- Testlerin geçmesi, değişikliğin güvenli veya üretime hazır olduğunu tek başına
  kanıtlamaz. Diff incelemesi ve insan onayı ayrı adımlardır.
- Hassas kodu, gerçek kişisel veriyi veya gizli anahtarı forma ya da bir modele
  yapıştırmayın.

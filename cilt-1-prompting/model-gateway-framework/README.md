# Model Gateway İhtiyaç Çerçevesi Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 17 — Prompt Mühendisliğinin Geleceği, 17.5
(KAVRAM — Model Gateway).

```yaml
volume: 1
chapter: 17
book_section: "Açık Modeller, Yerel Çalıştırma ve Sağlayıcı Bağımsızlığı: Model Gateway ve Maliyet Farkındalığı"
concepts:
  - model gateway
  - sağlayıcı bağımsızlığı
  - maliyet farkındalığı
  - toplam sahip olma maliyeti
objectives:
  - LO-17.5
last_verified: "2026-07"
```

## Ne Yapar?

Bölüm 17.5'teki KAVRAM kutusunun tanımı şudur: *"Model gateway, birden fazla
yapay zekâ sağlayıcısını tek bir ortak noktadan çağırmayı sağlayan ara
katmandır: hangi sağlayıcının kullanılacağına o karar verir, kullanımı ve
maliyeti de tek yerden kaydeder."* Bu laboratuvar, gerçek bir sağlayıcı
çağırmadan, bu tanımı bir kurumun mevcut durumunu soran bir kontrol listesine
çevirir:

- `OrganizationProfile`: kaç farklı sağlayıcı/model kullanıldığını, maliyet
  izleme, yedek sağlayıcı ve tek noktadan yönlendirmenin olup olmadığını,
  göreve göre elle sağlayıcı değiştirilip değiştirilmediğini ve gizlilik
  nedeniyle yerel çalıştırma gerekip gerekmediğini temsil eder.
- `evaluate_need`: bu durumdan "gateway'e ihtiyacınız var mı" sorusuna
  kanıta dayalı bir cevap (`dogrudan_api_yeterli` /
  `gateway_degerlendirilebilir` / `gateway_onerilir`), gerekçe listesi ve
  KAVRAM kutusundaki "nerede yanılabiliriz" uyarılarına karşılık gelen
  dikkat notları üretir.
- `demo_profiles`: Bölüm 17.5'teki Deniz örneğine karşılık gelen dört profili
  (hukuk bürosu, tekstil atölyesi, takibi zaten kurulu küçük bir ekip, Deniz'in
  üç müşterisinin toplamı) çalıştırır.

Değerlendirme yalnızca sağlayıcı sayısına bakmaz: iki sağlayıcı kullanılsa
bile maliyet izleme, yönlendirme ve yedekleme zaten elde tutuluyorsa sonuç
yine "doğrudan API yeterli" çıkar — kitabın "gateway kullanmak maliyeti
otomatik olarak düşürmez" uyarısıyla tutarlı bir tasarım.

Bu laboratuvar hiçbir model, araç veya sağlayıcı adı, fiyat ya da benchmark
iddiası üretmez; 17.5'in kendi vurguladığı "isimler eskir, çerçeve kalıcıdır"
ilkesine göre tasarlanmıştır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü
tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/model-gateway-framework/model_gateway_framework.html>
İsterseniz `model_gateway_framework.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Sağlayıcı
sayısı kaydırıcısını ve durum kutucuklarını değiştirdikçe sonuç, gerekçe ve
dikkat notları canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü
`model_gateway_framework.py` dosyasındadır. Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/model-gateway-framework
python3 model_gateway_framework.py
python3 -m pytest
```

## Beklenen Çıktı (özet)

```text
== Hukuk burosu (tek yerel model, gizli veri) ==
Sonuc: dogrudan_api_yeterli
Sinyal sayisi: 0

== Tekstil atolyesi (gorev karmasikligina gore model degistiriyor) ==
Sonuc: gateway_onerilir
Sinyal sayisi: 4

== Kucuk ekip (iki saglayici, ama takip zaten kurulu) ==
Sonuc: dogrudan_api_yeterli
Sinyal sayisi: 0

== Deniz'in toplami (uc musteri, uc saglayici) ==
Sonuc: gateway_onerilir
Sinyal sayisi: 4
```

Tek sağlayıcılı hukuk bürosu ve takibi zaten kurulu küçük ekip için gateway
gereksiz ek karmaşıklıktır; elle sağlayıcı değiştiren tekstil atölyesi ve üç
sağlayıcıyı tek başına takip eden Deniz için ise sinyal sayısı eşiği aşar ve
gateway önerilir — kitaptaki 17.5 anlatısıyla birebir örtüşür.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 model_gateway_framework.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu bir karar destek örneğidir; gerçek bir gateway kurulumu, güncel
  sözleşme koşulları ve kurumun kendi güvenlik/uyumluluk kuralları kontrol
  edilmeden yapılmaz.
- Sinyaller ve eşikler (2+ sağlayıcı, 3 sinyal) temsilîdir; gerçek bir
  kurumun karar eşiği ekip büyüklüğüne, sektöre ve risk iştahına göre
  değişebilir.
- Bu laboratuvar model adı, fiyat, benchmark veya sağlayıcı karşılaştırması
  içermez; bu tür hızla eskiyen bilgiler için
  [docs/model-watch](../../docs/model-watch/) ve resmî dokümantasyon ayrıca
  kontrol edilmelidir.
- "Gateway kullanmak maliyeti otomatik olarak düşürür" varsayılmamalı; ara
  katmanın kendi gecikmesi olabilir ve bazı sağlayıcıya özgü bir özellik
  gateway üzerinden tam desteklenmeyebilir (bkz. kitaptaki KAVRAM kutusu).
- Gizlilik nedeniyle yerel çalıştırma seçilse bile bu güvence yalnızca
  çıkarım adımı için geçerlidir; loglama, izleme veya harici bir arama/RAG
  servisi kurum dışı bir sunucuya bağlıysa veri o bileşen üzerinden dışarı
  çıkabilir.

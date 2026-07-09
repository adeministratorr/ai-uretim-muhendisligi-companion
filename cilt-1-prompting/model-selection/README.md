# Model Seçimi — Karar Matrisi Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 2 — Yapay Zekâ Araçlarını ve Model Ekosistemini
Tanımak, 2.1, 2.4, 2.10 ve 2.13.

```yaml
volume: 1
chapter: 02
book_section: "Yapay Zekâ Araçlarını ve Model Ekosistemini Tanımak"
concepts:
  - model / mod / araç ayrımı
  - standart model / akıl yürütme modeli
  - açık ağırlıklı model
  - model seçim kriterleri
objectives:
  - LO-2.1
  - LO-2.3
  - LO-2.4
  - LO-2.5
last_verified: "2026-07"
```

## Ne Yapar?

Bölümün temel ayrımı üç katmandır. Model, üretimi yapan çekirdektir; mod, aynı
modelin standart veya akıl yürütme gibi çalışma biçimidir; araç ise modeli sohbet
arayüzü, kod yardımcısı ya da ajan olarak paketleyen üründür. Doğru seçim model
adını ezberlemekle değil, görevin gereksinimlerini (veri hassasiyeti, güncellik,
hız, maliyet) sıralamakla başlar.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, Bölüm 2'deki "hangi iş için hangi
araç" karar çerçevesini küçük bir Python kontrol listesine çevirir:

- `TaskProfile`: görevin hassas veri, güncellik, kaynak, eylem, hız ve maliyet
  gereksinimlerini temsil eder.
- `decide`: bu gereksinimlerden model/mod/araç katmanını, standart/akıl yürütme
  modunu, ekosistem/dağıtım tercihini, veto noktalarını ve doğrulama kontrollerini
  üretir.
- `demo_profiles`: kitaptaki üç operasyon müdürü senaryosuna karşılık gelen
  örnekleri çalıştırır.

Bu laboratuvar model adı, fiyat, benchmark skoru veya lisans iddiası üretmez.
Güncel model/araç adları için güncel referans
[docs/model-watch](../../docs/model-watch/) altında tutulur. Son doğrulama: 2026-07.

## Nasıl Kullanılır?

Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/model-selection
python3 model_selection_lab.py
python3 -m pytest
```

## Beklenen Çıktı (özet)

```text
== Gunluk sohbet ve ozet ==
Katman: arac
Mod: standart
Ekosistem: kapali_api_veya_sohbet_araci_yeterli_olabilir
Dagitim: bulut_api_kabul_edilebilir

== Kod tabaninda hata duzeltme ==
Katman: arac
Mod: akil_yurutme
Arac gereksinimi: rag_belge_arama, ajan_tabanli_arac_diff_ve_test_onayi

== Gizli muhasebe verisi ozeti ==
Katman: model_dagitim
Mod: standart
Dagitim: yerel_oncelikli
Veto: ucretsiz_genel_sohbet_arayuzu
```

Gizli veri içeren basit bir özetleme işi, teknik olarak standart modla çözülebilir;
ama veri hassasiyeti dağıtım kararını değiştirir. Kod değişikliği ise yalnızca model
seçimi değil, ajan tabanlı araç ve insan diff/test review akışı gerektirir.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 model_selection_lab.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 5 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu bir karar destek örneğidir; gerçek tedarikçi seçimi, güncel sözleşme ve kurum
  güvenlik kuralları kontrol edilmeden yapılmaz.
- Kategoriler temsilîdir; model adı, fiyat, benchmark veya lisans bilgisi içermez.
  Bu tür hızla eskiyen bilgiler için [docs/model-watch](../../docs/model-watch/) ve
  resmî dokümantasyon ayrıca kontrol edilmelidir.
- Hassas veri senaryosunda "yerel öncelikli" sonucu, loglama, telemetri ve harici
  RAG/arama servisleri de kurum içinde tutulduğunda anlamlıdır.

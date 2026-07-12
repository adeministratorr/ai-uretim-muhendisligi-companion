# Prompt Versiyon Günlüğü Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 7 — Prompt Geliştirme, Test ve Belgeleme, 7.10
(Prompt Log Şablonu) ve 7.11 (Prompt Sürümleme).

```yaml
volume: 1
chapter: 07
book_section: "Prompt Geliştirme, Test ve Belgeleme"
concepts:
  - prompt log
  - prompt sürümleme
  - test seti
  - gerileme (regression) tespiti
objectives:
  - LO-7.6
last_verified: "2026-07"
```

## Ne Yapar?

Bölüm 7, bir promptu tek seferlik bir çözüm değil, ölçülerek geliştirilen ve
belgelenen bir sistem olarak ele alır. Bu laboratuvar, o disiplinin son iki
adımını (7.10'daki prompt log ve 7.11'deki sürümleme) çalışan bir araca çevirir.

Kaan'ın Hasar Özet Asistanı için tuttuğu günlük temel alınır: A/B/C sürümleri
(7.9'daki karşılaştırma tablosuyla birebir aynı puanlar), ardından üretime alınan
C'nin v1 olarak adlandırılması, biçim düzeltmesiyle v1.1'e çıkması ve tutar arama
stratejisinin kökten değiştirildiği v2'nin üretimde beklenmedik bir hataya yol
açması (7.11'deki anlatım). Her sürüm, 7.3'teki kolay/orta/zor test dosyalarından
temsilî bir alt kümede (`dosya_15_zor` gibi, 7.3'te tarif edilen "çelişkili
ekspertiz raporu içeren" zor dosya türü) ve 7.5'teki dört metrikte (D=Doğruluk,
E=Eksiksizlik, B=Biçim uyumu, K=Kullanılabilirlik) puanlanır.

- `format_log_table`: 7.10'daki günlük tablosunu (Tarih/Sürüm/Değişiklik
  özeti/Test seti/Model sürümü/Puan/Karar) üretir.
- `detect_test_regressions`: ardışık sürüm çiftlerinde, bir önceki sürümde geçen
  bir test dosyasının yeni sürümde başarısız olduğu durumları listeler.
- `detect_score_regressions`: bir metriğin, metrik başına tanımlı tolerans
  payını (D/E/B için 1,0 puan, K için 0,15 puan) aşacak biçimde düştüğü
  durumları listeler; küçük düşüşler 7.9'da anlatılan "tek çalıştırma gürültüsü"
  kabul edilip gerileme sayılmaz.
- `validate_entry` / `validate_log`: bir günlük satırının 7.10 şablonundaki
  zorunlu alanları (değişiklik özeti, gerekçe, test seti, model sürümü, en az
  bir test sonucu, en az bir metrik puanı, karar) taşıyıp taşımadığını denetler.

Bu laboratuvar modelin gizli değerlendirmesini taklit etmez; tamamen yerel ve
şeffaf kurallarla, elle girilmiş test sonuçları ve puanlar üzerinde çalışır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/prompt-log/prompt_log.html>
İsterseniz `prompt_log.html` dosyasını indirip çift tıklayarak da açabilirsiniz;
kurulum, terminal veya internet bağlantısı gerekmez. Bir sürüm rozetine tıklayıp
test sonuçlarını (GEÇTİ/BAŞARISIZ) veya metrik puanlarını değiştirdikçe günlük
tablosu ve gerileme raporu canlı güncellenir; kırmızı çerçeveli rozetler en az
bir gerileme taşıyan sürümleri işaretler.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `prompt_log.py` dosyasındadır.
Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/prompt-log
python3 prompt_log.py
python3 -m pytest
```

İnternet bağlantısı veya API anahtarı gerekmez. Testler yalnızca Python standart
kütüphanesi ve `pytest` ile çalışır.

## Beklenen Çıktı (özet)

```text
== Prompt log tablosu ==
| Tarih | Sürüm | Değişiklik özeti | Test seti | Model sürümü | Puan (D/E/B/K) | Karar |
|---|---|---|---|---|---|---|
| 2026-06-02 | A | İlk taslak (rol tanımı yok, serbest metin çıktı) | test-30 | temel model v1 | 61/58/40/1,8 | Elendi |
...
| 2026-07-01 | v2 | Hasar tutarı arama stratejisi kökten değiştirildi (iki adımlı çıkarım) | test-30 | temel model v1 | 88/90/97/2,5 | Geri alındı (v1.1'e dönüldü) |

== Gerileme raporu ==
[TEST GERİLEMESİ] dosya_15_zor: v1.1 sürümünde geçti, v2 sürümünde başarısız oldu.
[PUAN GERİLEMESİ] B: v1.1 sürümünde 99, v2 sürümünde 97 (düşüş: 2).
[PUAN GERİLEMESİ] D: v1.1 sürümünde 91, v2 sürümünde 88 (düşüş: 3).
[PUAN GERİLEMESİ] E: v1.1 sürümünde 93, v2 sürümünde 90 (düşüş: 3).
```

Gerileme raporu, 7.11'deki "v2'nin üretimde beklenmedik bir hataya yol açtığı"
anlatımının somut kanıtıdır: dosya_15_zor testi v1.1'de geçmişken v2'de
başarısız olmuştur; bu tek satır, ekibin neden v1.1'e geri döndüğünü açıklar.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 prompt_log.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 10 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu laboratuvar test sonuçlarını ve metrik puanlarını gerçek bir model
  çağrısından değil, elle girilen değerlerden alır; gerçek bir değerlendirme
  hattı değildir.
- Gerileme eşikleri (D/E/B için 1,0 puan, K için 0,15 puan) temsilîdir; gerçek
  bir ekip kendi test setinin gürültü düzeyine göre kendi toleransını belirlemelidir
  (7.9'da anlatıldığı gibi, kritik kararlarda her dosyanın birkaç kez çalıştırılıp
  ortalamasının alınması bu gürültüyü azaltır).
- `detect_test_regressions` ve `detect_score_regressions` yalnızca *ardışık*
  sürüm çiftlerini karşılaştırır; iki sürüm arasında atlanan bir ara sürüm varsa
  (örneğin günlükten silinmiş bir deneme) gerileme gözden kaçabilir.
- Model adı, fiyat veya benchmark iddiası içermez; güncel model bilgisi için
  [docs/model-watch](../../docs/model-watch/) kullanılmalıdır.

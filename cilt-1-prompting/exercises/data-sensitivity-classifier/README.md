---
volume: 1
chapter: 12
book_section: "Sorumlu ve Etik Kullanım"
concepts:
  - kişisel veri
  - hassas veri
  - kurum içi bilgi
  - anonimleştirme
  - maskeleme
  - yeniden kimliklendirme riski
objectives:
  - "LO-12.1"
  - "LO-12.3"
last_verified: "2026-07"
---

# Veri Hassasiyeti Sınıflandırıcı Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 12 — Sorumlu ve Etik Kullanım, 12.1-12.5
(dur-sınıflandır-anonimleştir-izin kontrol et refleksi; kişisel veri, hassas veri ve
kurum içi bilgi ayrımı; anonimleştirme ve maskeleme teknikleri).

## Ne Yapar?

Bölüm 12.1'in dersi, bir bilginin yapay zekâ aracına gönderilip gönderilemeyeceğine
karar vermeden önce dur-sınıflandır-anonimleştir-izin kontrol et sırasının izlenmesi
gerektiğidir. Bu laboratuvar, gerçek bir API çağrısı yapmadan, bu dört adımdan
**sınıflandırma** ve **anonimleştirme önerisi** kısmını küçük bir denetim aracına
dönüştürür:

- `data_sensitivity_classifier.py`: bir veri açıklamasını 12.2'deki tabloyla aynı
  öncelik sırasıyla üç kategoriden birine ayırır — **doğrudan gönderilebilir**,
  **anonimleştirilerek gönderilebilir** veya **hiç gönderilemez**.
- Kişisel veri tespit edilirse 12.5'teki maskeleme tablosuna (isim → kod, doğum
  tarihi → sınıf seviyesi, adres → mahalle düzeyi, T.C. kimlik/öğrenci numarası →
  tamamen çıkarma) uygun somut öneriler üretir.
- Metinde "tek öğrenci", "yalnızca bir" gibi kendine özgü bir ayrıntı da geçiyorsa,
  12.5'teki DİKKAT kutusundaki yeniden kimliklendirme (re-identification) uyarısını
  ekler.

Sınıflandırma önceliği kitaptaki sırayla aynıdır: hassas veri veya kurum içi bilgi
işareti bulunursa (anonimleştirilse bile) sonuç her zaman "hiç gönderilemez" olur;
yalnızca kişisel veri işareti varsa "anonimleştirilerek gönderilebilir"; hiçbiri
yoksa metin 12.1'deki "genel/herkese açık bilgi" sayılır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/exercises/data-sensitivity-classifier/data_sensitivity_classifier.html>
İsterseniz `data_sensitivity_classifier.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Hazır
örneklerden birini yükleyin veya kendi veri açıklamanızı yazın; karar ve maskeleme
önerileri canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `data_sensitivity_classifier.py`
dosyasındadır.

```bash
python3 data_sensitivity_classifier.py                      # kitaptaki 5 örnek senaryo
python3 data_sensitivity_classifier.py "Öğrencinin adı ve bu dönemki notu."
python3 -m pytest -q                                         # testler (9 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
Veri: 7. sınıf fen bilgisi müfredatının bu haftaki konusu fotosentez.
Karar: Doğrudan gönderilebilir
Gerekçe: Metinde kişisel veri, hassas veri veya kurum içi bilgi işareti bulunamadı; 12.1'e göre genel/herkese açık bilgi doğrudan gönderilebilir.
---
Veri: Öğrencinin rehberlik görüşme notu: ailede boşanma süreci yaşanıyor.
Karar: Hiç gönderilemez
Gerekçe: Metinde hassas veri işareti bulundu (rehberlik görüşme notu); 12.2'ye göre hassas veri kişisel veriden daha sıkı korunur ve çoğu kurumda hiçbir şekilde gönderilmez.
---
Veri: Ayşe Yılmaz'ın bu dönem matematik notu 72; veli telefon numarası 0532 xxx xx xx.
Karar: Anonimleştirilerek gönderilebilir
Maskeleme önerileri:
- Telefon numarasını tamamen çıkarın; gerekirse kurumun ilgili biriminde ayrı ve güvenli saklayın.
- Veli telefon numarasını tamamen çıkarın; gerekirse kurumun ilgili biriminde ayrı ve güvenli saklayın.
```

Bu çıktı, girilen veriyi gerçekten anonimleştirmez; yalnızca hangi kategoriye
girdiğini ve hangi somut adımın (kod, çıkarma, bölge daraltma) uygulanması
gerektiğini gösterir. Gerçek maskeleme, 12.5'te anlatıldığı gibi yapay zekâ
aracına hiçbir şey gönderilmeden önce elle veya kurumun kendi aracıyla yapılır.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3, gerçek API çağrısı yok).
- [x] Örnek çalışıyor (`python3 data_sensitivity_classifier.py`).
- [x] Test/doğrulama komutu var (`pytest`, 9 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu bir gerçek veri sınıflandırma/DLP (Data Loss Prevention) sistemi değildir;
  yalnızca önceden tanımlı Türkçe anahtar sözcükleri arar. Gerçek adları, bağlamı
  veya cümlenin anlamını anlamaz — "Ali'nin notu" ifadesindeki "Ali" bir isim
  olarak tanınmaz, yalnızca "ad soyad", "isim" gibi açık ifadeler tetikleyicidir.
- Anahtar sözcük listesi kitaptaki 12.2 tablosu ve 12.4-12.5'teki örneklerle
  sınırlıdır; kapsamadığı hiçbir kişisel/hassas veri türü "doğrudan gönderilebilir"
  yanlış kararına yol açabilir. Gerçek kullanımda bu araç bir başlangıç kontrolüdür,
  son karar değildir — 12.1'deki dur-sınıflandır-anonimleştir-izin kontrol et
  sırasının insan tarafından tamamlanması gerekir.
- Yeniden kimliklendirme (re-identification) uyarısı yalnızca birkaç sabit ifadeyi
  arar; 12.5'teki DİKKAT kutusunun belirttiği gibi gerçek yeniden kimliklendirme
  riski çok daha geniş bir bağlam değerlendirmesi gerektirir.
- Bu araç bir hukuki görüş değildir; KVKK, GDPR veya AB Yapay Zekâ Yasası
  kapsamındaki nihai karar için 12.3'teki REFERANS kutusunda belirtildiği gibi
  güncel resmî kaynaklara ve gerektiğinde bir hukuk danışmanına başvurulmalıdır.

# Multimodal Çıktı Denetimi — Betimleme, Yorum ve Varsayım Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 9 — Çok Kipli (Multimodal) Prompting, 9.3,
9.6, 9.11 ve 9.12.

```yaml
volume: 1
chapter: 09
book_section: "Çok Kipli (Multimodal) Prompting"
concepts:
  - ekran görüntüsü analizi
  - PDF/doküman üzerinden çalışma
  - gizlilik ve telif riski
  - multimodal çıktı doğrulama
objectives:
  - LO-9.2
  - LO-9.4
  - LO-9.7
last_verified: "2026-07"
```

## Ne Yapar?

Bölüm 9'un denetim disiplini dört adımdan oluşur: görselde ne göründüğünü aktaran
betimleme, bunun ne anlama geldiğini söyleyen yorum, doğrulama yolu gösterilmiş
varsayım listesi ve ayrı tutulan gizlilik/telif kontrolü. Betimleme ile yorumun
birbirine karışması, model cevabına duyulan güvendeki en yaygın tuzaktır; görünen
bilgi ile modelin tahmini aynı cümlede birleştiğinde okur ikisini de doğrulanmış
sanır.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, bu dört adımlı disiplini küçük
bir Python denetimine çevirir:

- `MultimodalReviewTask`: ekran görüntüsü, grafik, tablo veya PDF kesiti için
  görev bağlamını ve varsa dayanak dokümanını ayrı tutar.
- `render_review_prompt`: modelden dört ayrı başlık altında cevap isteyen bir
  prompt üretir.
- `audit_response`: model cevabında betimleme ile yorumun ayrılıp ayrılmadığını,
  varsayımların doğrulama yolu taşıyıp taşımadığını ve gizlilik/telif kontrolünün
  boş bırakılıp bırakılmadığını denetler.

Bu laboratuvar bir görseli okumaz ve model cevabının doğru olduğunu kanıtlamaz.
Yalnızca cevabın, Bölüm 9'da anlatılan denetlenebilir çıktı biçimine uyup
uymadığını kontrol eder.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/prompt-patterns/multimodal-output-review/multimodal_review_lab.html>
İsterseniz `multimodal_review_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Hazır cevaplardan
birini yükleyin veya kendi cevabınızı yapıştırın; denetim sonucu canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `multimodal_review_lab.py`
dosyasındadır. Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/prompt-patterns/multimodal-output-review
python3 multimodal_review_lab.py
python3 -m pytest
```

## Beklenen Çıktı (özet)

```text
== Zayıf cevap ==
Hazır: hayır
Eksik başlıklar: varsayım listesi, gizlilik ve telif kontrolü
Varsayım sayısı: 0
Doğrulanabilir varsayım: 0

== Denetlenebilir cevap ==
Hazır: evet
Eksik başlıklar: yok
Varsayım sayısı: 3
Doğrulanabilir varsayım: 3
```

Zayıf cevap, hata kodunu yorumla birlikte verir ve dayanak doküman yokken kesin
neden söyler. Denetlenebilir cevap önce görünen bilgiyi aktarır, sonra yorumun
sınırını çizer, varsayımları doğrulama yoluyla yazar ve gizlilik/telif kontrolünü
ayrı tutar.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 multimodal_review_lab.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu örnek görsel, ekran görüntüsü veya PDF içeriğini kendisi analiz etmez; yalnızca
  modelden gelen metin cevabın yapısını denetler.
- Basit metin işaretlerine bakar. Kritik üretim, sağlık, hukuk, finans veya güvenlik
  kararlarında insan denetimi ve bağımsız kaynak kontrolü gerekir.
- Model adı, fiyat, benchmark veya güncel yetenek iddiası içermez. Bu tür hızla
  eskiyen bilgiler için [docs/model-watch](../../../docs/model-watch/) ayrıca
  kontrol edilmelidir. Son doğrulama: 2026-07.

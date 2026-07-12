# Şablon Doğrulayıcı — Göreve Özel Şablon Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 8 — Prompt Atölyesi: Göreve Özel Şablonlar, 8.2
(beş alanlı iskelet) ve 8.14 (şablonların kalite kontrolü); Ek C — Prompt Şablon
Kütüphanesi (persona şablonları).

```yaml
volume: 1
chapter: 08
book_section: "Prompt Atölyesi: Göreve Özel Şablonlar"
concepts:
  - göreve özel şablon
  - beş alanlı iskelet (amaç, hedef kitle, kaynak, format, sınır)
  - bağlam eksikliği
  - kaynak sınırlama
objectives:
  - LO-8.1
  - LO-8.2
last_verified: "2026-07"
```

## Ne Yapar?

Bölüm 8.2, her göreve özel şablonu beş sabit alan (Amaç, Hedef Kitle, Kaynak,
Format, Sınır) etrafında kurar; bu alanlardan biri boş bırakıldığında model
boşluğu kendi varsayımıyla doldurur (8.2, 8.14 — Bağlam Eksikliği). Ek C
(Prompt Şablon Kütüphanesi), bu beş alanı beş farklı persona için köşeli
parantezli `[DEĞİŞKEN]` alanlarıyla somutlaştırır.

Bu laboratuvar gerçek bir API çağrısı yapmadan, kullanıcının doldurduğu bir
şablon metnini saf metin işlemeyle denetler:

- `parse_fields`: "Amaç: ... Hedef kitle: ... Kaynak: ... Format: ... Sınır: ..."
  biçimindeki bir metni alan adı → içerik sözlüğüne ayırır (büyük/küçük harfe
  duyarsız).
- `find_variables`: bir metindeki hâlâ doldurulmamış `[DEĞİŞKEN]` alanlarını
  bulur.
- `validate_template`: beş zorunlu alanın her biri için üç durumu ayrı ayrı
  işaretler — alan etiketi hiç **yok** (eksik), etiket var ama içerik **boş**,
  içerikte hâlâ doldurulmamış bir **değişken** var. İsteğe bağlı altıncı alanı
  (Başarı Kriteri, 8.2) tespit eder ama zorunlu saymaz.
- `format_report`: sonucu terminalde okunabilir bir metne çevirir.

Örnek veri olarak Ek C'nin beş personasından ikisi (**Öğretmen** — "Ders
Materyali Sadeleştirme" ve **Analist** — "Veri Yorumu ve Varsayım Listesi") ve
ayrıca **Geliştirici** — "Hata Açıklatma" şablonu kullanılır; her biri için hem
ham (hiç doldurulmamış) şablon hem de kullanıcının doldurduğu iki sürüm
(eksikli ve tam) tanımlıdır.

Bu laboratuvar model davranışını taklit etmeye çalışmaz. Amaç, bir şablonun
*eksiksiz doldurulup doldurulmadığını* denetlemektir; çıktının *doğruluğu*
ayrı bir konudur (bkz. 8.14 — doğruluk, gizlilik, telif, bağlam eksikliği).

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü
tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/task-templates/template_validator_lab.html>
İsterseniz `template_validator_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Açılır
listeden bir persona/durum seçin veya kendi doldurduğunuz şablonu metin
kutusuna yapıştırın; sonuç anında güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `template_validator_lab.py`
dosyasındadır. Terminalde bu klasöre geçin:

```bash
python3 template_validator_lab.py   # demo çıktısı (6 senaryo, terminalde metin olarak)
python3 -m pytest                   # testler (7 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
Şablon: Öğretmen — eksik dolu
  - Amaç: tamam
  - Hedef Kitle: doldurulmamış değişken var -> [yaş grubu]
  - Kaynak: tamam
  - Format: tamam
  - Sınır: BOŞ (etiket var, içerik yok)
Sonuç: HAZIR DEĞİL

Şablon: Öğretmen — tam dolu
  - Amaç: tamam
  - Hedef Kitle: tamam
  - Kaynak: tamam
  - Format: tamam
  - Sınır: tamam
Sonuç: HAZIR
```

Eksikli sürümde hem doldurulmamış bir değişken (`[yaş grubu]`) hem de tamamen
boş bırakılmış bir alan (`Sınır`) aynı anda görülebilir; tam sürümde beş alan
da doldurulduğu için sonuç "HAZIR" olur.

## Kabul Kriteri

- [x] Kurulum adımları açık (bağımlılık yok, saf Python 3).
- [x] Örnek çalışıyor (`python3 template_validator_lab.py`).
- [x] Test/doğrulama komutu var (`pytest`, 7 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] En az iki Ek C personası (Öğretmen, Analist; ayrıca Geliştirici) örnek
      veri olarak kullanıldı.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu doğrulayıcı yalnızca **biçimsel eksiksizliği** denetler (alan var mı,
  boş mu, değişken kalmış mı); bir alanın **içeriğinin doğru veya anlamlı**
  olduğunu denetlemez. "Sınır: evet" gibi anlamsız ama biçimsel olarak dolu bir
  içerik "tamam" sayılır.
- Alan ayrıştırma, Ek C'deki sabit kalıba ("Amaç: ... Hedef kitle: ... Kaynak:
  ... Format: ... Sınır: ...", tek paragraf, sırayla) dayanır; alan adları bu
  beş kelimenin dışına çıkarsa veya sıra bozulursa ayrıştırma yanlış
  sonuç verebilir.
- Bu laboratuvar 8.14'teki gizlilik ve telif kontrollerini yapmaz; yalnızca
  8.2'nin beş alanının doldurulup doldurulmadığını denetler. Bir şablona
  yapıştırılan verinin kişisel bilgi veya telifli içerik taşıyıp taşımadığı
  ayrıca ve elle kontrol edilmelidir.

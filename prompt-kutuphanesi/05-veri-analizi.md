# Veri Analizi Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Veri Analizi"
concepts:
  - keşifsel veri analizi (EDA)
  - SQL üretimi
  - bulgu raporlama
last_verified: "2026-07"
```

Veri promptlarında iki kritik kural:

1. **Veriyi tarif edin, sonra yapıştırın.** Kolon adları, tipler ve örnek
   satırlar olmadan model şema uydurur.
2. **Modelin aritmetiğine güvenmeyin.** Büyük tablolarda toplam/ortalama
   hesabını modele değil koda (code interpreter, pandas, SQL) yaptırın;
   modelden hesap değil hesap planı isteyin.

---

## 1. Keşifsel Veri Analizi (EDA) Planı

**Ne işe yarar:** Yeni bir veri setine nereden bakılacağını planlatır.

**Prompt:**

```text
Deneyimli bir veri analistisin. Şu veri seti için keşifsel analiz planı çıkar:

Veri: [ne verisi, kaç satır, hangi dönem]
Kolonlar: [ad: tip: kısa açıklama — liste]
Örnek 3 satır:
[örnek satırlar]
İş sorusu: [bu analizden ne öğrenmek istiyoruz]

Format:
1. Veri kalitesi kontrolleri: eksik değer, tekrar, aykırı değer, tutarsız
   kategori — her biri için çalıştırılacak somut kontrol (pandas koduyla).
2. İş sorusuna giden 3-5 analiz adımı; her adımda beklenen çıktı ve
   "bu çıktı X çıkarsa şu anlama gelir" yorumu.
3. Bu veriyle CEVAPLANAMAYACAK soruları açıkça listele (eksik kolon,
   örneklem sorunu vb.).
```

**Notlar:** 3. madde, analizin en değerli çıktısı olabilir; veri setinin
sınırını baştan görünür kılar.

---

## 2. SQL Sorgusu Yazdırma

**Ne işe yarar:** Şema + iş sorusu ikilisinden doğrulanabilir SQL üretir.

**Prompt:**

```text
[Veritabanı: PostgreSQL/BigQuery/...] için SQL yazan deneyimli bir
analistsin.

Şema:
[CREATE TABLE ifadeleri veya kolon listeleri — ilişkiler dahil]

İş sorusu: [örn. "son 90 günde kohort bazında ikinci sipariş oranı"]

Kurallar:
- Sorguyu yaz; her CTE'nin üstüne tek satır yorum koy (bu blok ne yapıyor).
- Kullandığın her varsayımı (zaman dilimi, null davranışı, tekrar eden
  kayıt kuralı) sorgunun altında "Varsayımlar" başlığıyla listele.
- Sonucun doğruluğunu elle kontrol etmek için 2 basit doğrulama sorgusu ekle
  (örn. toplamların çapraz kontrolü).
- Şemada olmayan kolonu icat etme; soru şemayla cevaplanamıyorsa söyle.
```

---

## 3. Grafik/Görselleştirme Seçimi

**Ne işe yarar:** "Bu veriyi nasıl göstereyim" sorusunu, mesaj odaklı
yanıtlar.

**Prompt:**

```text
Veri görselleştirme danışmanısın.

Veri: [ne var — değişkenler ve tipleri]
Vermek istediğim mesaj: [tek cümle: okuyan ne anlamalı]
Hedef kitle ve mecra: [rapor/sunum/dashboard; teknik mi değil mi]

Format:
1. Bu mesaj için en uygun grafik türü + gerekçe (neden alternatiflerden iyi).
2. Kaçınılması gereken 1-2 tür + neden yanıltıcı olur.
3. Uygulama detayı: eksen, sıralama, renk kullanımı, vurgu — mesajı
   güçlendirecek somut kararlar.
4. [Kütüphane: matplotlib/plotly/...] ile çalışır örnek kod.

Süsleme için değil mesaj için tasarla; grafik başına tek mesaj ilkesine uy.
```

---

## 4. Bulgu Raporu (Analiz → Karar Metni)

**Ne işe yarar:** Analiz çıktılarını, karar vericinin okuyacağı rapora
dönüştürür.

**Prompt:**

```text
Kıdemli bir veri analistisin; teknik olmayan yöneticilere rapor yazıyorsun.

Analiz çıktıları:
[bulgular — tablolar, rakamlar, grafik açıklamaları]
Analizin amacı: [hangi karar için yapıldı]

Format:
1. Ana mesaj (tek cümle, rakamlı).
2. Bulgular (en fazla 5 madde; her maddede rakam + iş anlamı).
3. "Bu veri şunu SÖYLEMEZ" bölümü: korelasyon/nedensellik ayrımı,
   örneklem sınırı, dönem etkisi gibi uyarılar.
4. Önerilen aksiyon ve izlenecek metrik.

Kurallar: verdiğim çıktılarda olmayan rakam kullanma; yuvarlama yaparsan
belirt; belirsizliği gizleme ("yaklaşık", "en az" gibi nitelemeleri koru).
```

---

## 5. Veri Temizleme Yardımcısı

**Ne işe yarar:** Kirli veri örneğinden temizleme kuralları ve kodu çıkarır.

**Prompt:**

```text
Veri mühendisisin. Aşağıdaki kirli veri örneğini incele ve temizleme
stratejisi çıkar.

Örnek satırlar (sorunlu olanlar dahil):
[10-20 satır]
Hedef kullanım: [analiz/ML/rapor — temizlik standardını bu belirler]

Format:
1. Tespit ettiğin sorunların listesi (her sorun için örnek satır referansı).
2. Her sorun için önerilen kural: düzelt / at / işaretle — ve gerekçesi.
   Veri atmayı gerektiren kurallarda kaç satırın etkileneceğini tahmin et
   ve "bu kayıp kabul edilebilir mi" sorusunu bana yönelt.
3. Kuralları uygulayan pandas kodu; her kural ayrı, test edilebilir bir
   fonksiyon olsun.
4. Temizlik sonrası doğrulama kontrolleri (satır sayısı mutabakatı, değer
   aralığı kontrolleri).
```

---

## 6. İstatistiksel Yorum Denetçisi

**Ne işe yarar:** Bir analiz yorumunun istatistiksel olarak savunulabilir
olup olmadığını denetletir.

**Prompt:**

```text
Titiz bir istatistikçisin. Aşağıdaki analiz yorumunu denetle:

Yorum: [örn. "X kampanyası satışları %12 artırdı"]
Dayanak veri/yöntem: [nasıl ölçüldü, örneklem, dönem, kontrol grubu var mı]

Denetim listesi:
1. Nedensellik iddiası veriyle destekleniyor mu, yoksa korelasyon mu?
2. Karıştırıcı değişken (confounder) adayları neler?
3. Örneklem ve dönem seçimi sonucu bükebilir mi (mevsimsellik, seçim yanlılığı)?
4. Bu iddiayı savunulabilir kılmak için hangi ek analiz gerekir?

Sonuç: yorumu "savunulabilir / şartlı savunulabilir / savunulamaz" diye
derecelendir ve savunulabilir yeniden yazımını öner.
```

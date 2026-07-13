# Yazılım Geliştirme Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Yazılım Geliştirme"
concepts:
  - code review
  - hata ayıklama (debugging)
  - birim testi (unit test)
  - refactoring
last_verified: "2026-07"
```

Metin tabanlı büyük dil modellerinin tümünde (Claude, ChatGPT, Gemini vb.)
küçük uyarlamalarla çalışır. Kod içeren promptlarda kodu her zaman üç tırnaklı
blok içinde verin; dil adını belirtin.

---

## 1. Kod İnceleme (Code Review)

**Ne işe yarar:** Bir değişikliği ya da dosyayı, insan reviewer'ın bakacağı
eksenlerde sistematik inceletir.

**Prompt:**

```text
Kıdemli bir [dil/çerçeve] geliştiricisisin ve bir pull request'i inceliyorsun.
Aşağıdaki kodu şu sırayla değerlendir:

1. Doğruluk: mantık hataları, sınır koşulları (edge case), null/boş girdi durumları.
2. Güvenlik: girdi doğrulama, injection riskleri, secret sızıntısı.
3. Performans: gereksiz döngü, N+1 sorgu, bellek kullanımı.
4. Okunabilirlik: adlandırma, ölü kod, tekrarlanan blok.

Her bulgu için: satır/işlev referansı, sorunun bir cümlelik açıklaması,
somut düzeltme önerisi (kod parçası). Bulgu yoksa "bulgu yok" yaz; sorun
üretmek için zorlamana gerek yok. Üslup tercihi ile gerçek hatayı ayır:
üslup notlarını en sona "İsteğe bağlı" başlığıyla koy.

Kod:
```[dil]
[kod]
```
```

**Notlar:** "Bulgu yoksa bulgu yok yaz" kısıtı önemlidir; bu kısıt olmadan
model, geçerli kodda bile sorun icat etme eğilimindedir.

---

## 2. Hata Ayıklama (Debugging) Yardımcısı

**Ne işe yarar:** Hata mesajı + kod + beklenti üçlüsünden kök neden analizi
ister; körlemesine yama önerisini engeller.

**Prompt:**

```text
Deneyimli bir hata ayıklayıcısın. Sana bir hata durumu vereceğim; hemen
düzeltme önerme. Önce şu sırayla ilerle:

1. Belirtiyi kendi cümlelerinle özetle (ben yanlış anlatmış olabilirim).
2. En olası 3 kök neden hipotezini, her birinin nasıl doğrulanacağıyla
   birlikte listele (hangi log, hangi print, hangi test).
3. Eldeki kanıtla hangi hipotezin öne çıktığını söyle.
4. Ancak ondan sonra düzeltme öner ve düzeltmenin yan etkilerini belirt.

Beklenen davranış: [ne olmalıydı]
Gözlenen davranış: [ne oluyor]
Hata çıktısı:
```text
[hata mesajı / stack trace]
```
İlgili kod:
```[dil]
[kod]
```
```

**Notlar:** Adım sırası bilinçli: modeli teşhisten önce tedaviye atlamaktan
alıkoyar. Cilt 2'deki debug loop bölümüyle birlikte kullanın.

---

## 3. Birim Testi Yazdırma

**Ne işe yarar:** Var olan bir işlev için sınır koşullarını da kapsayan test
seti üretir.

**Prompt:**

```text
[Test çerçevesi: pytest / Jest / JUnit] kullanan bir test mühendisisin.
Aşağıdaki işlev için test dosyası yaz.

Kapsam kuralları:
- Mutlu yol (happy path) için en az 2 test.
- Sınır koşulları: boş girdi, tek eleman, çok büyük girdi, yanlış tip.
- Hata yolu: işlevin hata fırlatması gereken her durum için ayrı test.
- Her testin adı, neyi doğruladığını okunur biçimde anlatsın.
- Test edilemeyen bir davranış görürsen (rastgelelik, saat, ağ), bunu
  yorum satırıyla işaretle ve nasıl izole edileceğini öner.

Yalnızca test kodu üret; işlevin kendisini değiştirme.

İşlev:
```[dil]
[kod]
```
```

**Notlar:** "İşlevi değiştirme" kısıtı olmadan model, testi geçirmek için
kodu "düzeltme" eğilimi gösterebilir. Üretilen testleri çalıştırmadan
geçerli saymayın.

---

## 4. Eski Kodu Açıklatma

**Ne işe yarar:** Dokümantasyonsuz/karmaşık bir kod parçasını farklı
seviyelerde açıklatır; devralınan projelerde ilk adım.

**Prompt:**

```text
Aşağıdaki kodu üç katmanda açıkla:

1. Tek cümle: bu kod ne işe yarar?
2. Akış: girdiden çıktıya ana adımlar (madde listesi, her madde satır
   aralığı referansıyla).
3. Dikkat noktaları: örtük varsayımlar, yan etkiler (dosya, ağ, global
   durum), kırılgan görünen yerler.

Bilmediğin bir bağlam varsa uydurma; "bu kısım dış bağlama bağlı" diye
işaretle ve hangi bilginin gerektiğini söyle.

```[dil]
[kod]
```
```

**Notlar:** "Uydurma, işaretle" kısıtı, modelin görünmeyen bağımlılıklar
hakkında kendinden emin ama yanlış açıklama üretmesini azaltır.

---

## 5. Refactoring Önerisi

**Ne işe yarar:** Davranışı değiştirmeden yapıyı iyileştirme önerileri alır;
kapsam sınırı koyar.

**Prompt:**

```text
Kıdemli bir yazılımcısın. Aşağıdaki kodu davranışını DEĞİŞTİRMEDEN daha
okunur ve bakımı kolay hale getirecek en fazla 3 refactoring öner.

Her öneri için:
- Sorunun adı (ör. uzun işlev, tekrarlanan blok, iç içe koşul).
- Önerinin kodu (yalnız değişen kısım, önce/sonra biçiminde).
- Bu değişikliğin hangi testle güvence altına alınacağı.

Kapsam dışı: mimari değişiklik, yeni bağımlılık, isimlendirme zevk
tartışması. Kod zaten yeterince iyiyse bunu söyle ve dur.

```[dil]
[kod]
```
```

---

## 6. Commit Mesajı ve PR Açıklaması

**Ne işe yarar:** Diff'ten kurallı commit mesajı ve PR açıklaması üretir.

**Prompt:**

```text
Aşağıdaki diff için:

1. `tip(kapsam): kısa açıklama` biçiminde tek satırlık commit mesajı yaz
   (tipler: feat, fix, docs, test, refactor, chore).
2. PR açıklaması yaz: "Ne değişti" (madde listesi), "Neden" (1-2 cümle),
   "Nasıl test edildi" (komut veya adım).

Diff'te görmediğin şeyi yazma; test bilgisi diff'ten anlaşılmıyorsa
"test bilgisi eklenecek" diye boş bırak.

```diff
[diff]
```
```

---

## 7. Teknik Tasarım Tartışma Partneri

**Ne işe yarar:** Bir tasarım kararını (kütüphane seçimi, şema tasarımı,
API biçimi) savunmalı biçimde tartıştırır.

**Prompt:**

```text
Deneyimli bir yazılım mimarısın. Şu kararı değerlendireceğiz:

Karar: [örn. "X servisinde kuyruk olarak Redis Streams mi RabbitMQ mu?"]
Bağlam: [takım büyüklüğü, ölçek, mevcut altyapı, kısıtlar]

Şu formatta ilerle:
1. Her seçenek için 3 güçlü, 3 zayıf yön — bu projenin bağlamına özgü olsun,
   genel geçer broşür maddeleri değil.
2. "Şu koşul doğruysa A, şu koşul doğruysa B" biçiminde karar kuralı öner.
3. Kararı bugün vermemek için geçerli bir neden var mı, söyle.
4. Bana pozisyonumu test eden 3 soru sor.

Benim eğilimim: [varsa]. Eğilimime katılmak zorunda değilsin; katılıyorsan
da nedenini bağımsız gerekçelendir.
```

**Notlar:** Son kısıt, modelin kullanıcı eğilimini onaylama (sycophancy)
eğilimine karşı korumadır.

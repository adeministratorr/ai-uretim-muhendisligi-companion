# Sosyal Medya Yönetimi Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Sosyal Medya Yönetimi"
concepts:
  - içerik stratejisi
  - rakip analizi
  - topluluk yönetimi
last_verified: "2026-07"
```

[09-sosyal-medya-trend-promptlari.md](09-sosyal-medya-trend-promptlari.md)
viral kalıpları belgeler; bu dosya ise sosyal medyayı **iş olarak
yönetenlerin** günlük promptlarını toplar. Genel ilke: modele hesabınızın
bağlamını (marka sesi, kitle, geçmiş performans) vermeden istenen hiçbir
içerik "sizin" olmaz — bağlamsız istek, jenerik içerik üretir.

---

## 1. İçerik Takvimi Planlayıcı

**Ne işe yarar:** Aylık içerik takvimini tema + format + platform
dengesiyle kurar.

```text
Deneyimli bir sosyal medya stratejistisin.

Marka: [ne satıyor, marka sesi 3 sıfatla]
Platformlar: [Instagram/LinkedIn/TikTok/X — hangileri aktif]
Hedef: [takipçi/etkileşim/trafik/satış — bu ay hangisi öncelikli]
Kapasite: haftada [n] içerik üretebiliyoruz (gerçekçi)
Sabitler: [kampanya, lansman, özel gün tarihleri]

Format: 4 haftalık takvim tablosu — tarih, platform, içerik teması,
format (reel/karusel/metin/story), amaç (değer/etkileşim/satış), CTA.

Kurallar:
- 80/20 kuralı: içeriğin en fazla %20'si doğrudan satış.
- Her hafta en az bir "konuşma başlatan" içerik (soru, anket, tartışma).
- Kapasiteyi aşma; kapasite hedefe yetmiyorsa neyin kırpıldığını söyle.
- Her içerik temasının yanına tek cümlelik "neden bu kitleye" gerekçesi.
```

---

## 2. Platforma Özel Gönderi Üretimi

**Ne işe yarar:** Tek fikirden, her platformun diline uygun ayrı gönderiler
üretir (çapraz yayın kopyala-yapıştır hatasını önler).

```text
Sosyal medya metin yazarısın. Şu fikri üç platforma uyarlayacaksın:

Fikir/mesaj: [tek cümle]
Marka sesi: [örn. bilgili ama samimi; emoji az; jargon yok]
Kanıt/detay: [varsa veri, örnek, görsel açıklaması]

Üret:
1. LinkedIn: 100-200 kelime; ilk cümle kaydırmayı durdursun ama clickbait
   olmasın; paragraflar kısa; sonda tartışma sorusu.
2. Instagram: ilk cümle + değer veren 3-5 kısa satır + CTA; 5 alakalı
   hashtag (jenerik #love tarzı değil, niş).
3. X/Twitter: 280 karakteri zorlamayan tek gönderi + istenirse 3 gönderilik
   flood versiyonu.

Kural: platformlar arası birebir kopya yasak; her sürüm o platformun okuma
alışkanlığına göre yeniden kurulur. Uydurma istatistik yok.
```

---

## 3. Rakip Analizi

**Ne işe yarar:** Rakip hesap verilerini yapılandırılmış karşılaştırmaya
çevirir. Not: model hesapları kendisi gezemez; veriyi siz toplar
(gönderi örnekleri, frekans, etkileşim sayıları) modele verirsiniz —
vermezseniz aldığınız analiz uydurmadır.

```text
Sosyal medya analisti olarak çalışıyorsun. Aşağıda [n] rakibin son 30
günlük verileri var:

<rakip_verileri>
[Her rakip için: takipçi, gönderi sıklığı, format dağılımı, en çok
etkileşim alan 3 gönderinin özeti/metni, etkileşim oranları]
</rakip_verileri>

Bizim durumumuz: [aynı metrikler]

Format:
1. Karşılaştırma tablosu (frekans, format karması, etkileşim oranı).
2. Her rakibin belirgin stratejisi (verilerden çıkan, tahmin değil) ve
   işleyen içerik kalıpları.
3. Boşluk analizi: rakiplerin girmediği, bizim kitleye uyan 3 içerik alanı.
4. "Taklit etme" uyarısı: rakipte işleyip bizde işlemeyecek şeyler ve neden.

Kural: verilen veride olmayan hiçbir metrik veya gönderi uydurma; veri
yetersizse hangi ek verinin toplanacağını söyle.
```

---

## 4. Video/Reel Senaryosu

**Ne işe yarar:** Kısa video için saniye saniye senaryo çıkarır; görsel ve
video üretim promptlarıyla (dosya 06-07) zincirlenebilir.

```text
Kısa video senaristisin. [Platform: Reels/TikTok/Shorts] için [süre: 30-60
sn] senaryo yaz.

Konu: [ne anlatılacak]
Hedef: [izleyici videodan ne alacak + bizden ne istenecek]
Format: [yüz kamerada anlatım / ekran kaydı / b-roll üstü seslendirme]

Çıktı tablosu: zaman aralığı | görüntü | konuşma/altyazı metni | ekran yazısı.

Kurallar:
- İlk 2 saniye kancası: merak uyandır, vaat et; ama videonun karşılayacağı
  bir vaat olsun.
- Her 5-7 saniyede görsel değişim (plan, açı veya ekran yazısı).
- Tek video = tek mesaj; sığmayan fikirleri "sonraki video önerisi" olarak
  ayır.
- Sonda net CTA (takip/kaydet/yorum — hedefe uygun tek bir tane).
```

---

## 5. Topluluk Yönetimi: Yorum ve DM Yanıtları

**Ne işe yarar:** Zor yorumlara (şikâyet, trol, kriz) marka sesinden çıkmadan
yanıt taslağı üretir.

```text
[Marka] hesabının topluluk yöneticisisin. Marka sesi: [tanım].

Gelen yorum/mesaj:
[metin]
Bağlam: [gönderi ne hakkındaydı; yorumcunun geçmişi biliniyorsa]

Üç yanıt seçeneği üret: (a) kısa ve sıcak, (b) açıklayıcı, (c) mizahlı
(markaya uygunsa). Her biri için tek cümlelik risk notu.

Kurallar:
- Savunmacılık yok; haklı eleştiride hatayı kabul et.
- Trol/hakaret ise: yanıtlamama veya tek nötr yanıt + sessize alma öner;
  tartışmaya girme.
- Kriz sinyali varsa (yaygınlaşan şikâyet, güvenlik iddiası) yanıt taslağı
  yerine ESKALASYON öner: kime, hangi bilgiyle.
- Kişisel veri isteme/verme yok; detay gerekiyorsa DM'e/destek kanalına yönlendir.
```

---

## 6. Performans Raporu Yorumlama

**Ne işe yarar:** Aylık metrik dökümünü strateji kararına çevirir.

```text
Sosyal medya analisti olarak aylık performansı değerlendir.

<veriler>
[gönderi bazlı: format, tema, erişim, etkileşim, kayıt, tıklama;
takipçi değişimi; geçen ay karşılaştırması]
</veriler>
Bu ayki hedefimiz: [neydi]

Format:
1. Hedefe göre durum (tek cümle, rakamlı).
2. En iyi/en kötü 3 gönderi ve ORTAK örüntüler (format mı, tema mı,
   zamanlama mı — veriye dayanarak ayrıştır).
3. Denenecek 3 hipotez: her biri "X yaparsak Y artar çünkü veri Z gösteriyor"
   kalıbında, gelecek ay ölçülebilir.
4. Bırakılacaklar: emek/getiri oranı kötü içerik türleri.

Kural: tek gönderilik başarıyı trend sanma; örüntü için en az 3 veri
noktası iste, yoksa "veri yetersiz" de.
```

---

## 7. Hashtag ve Keşfet Stratejisi

**Ne işe yarar:** Niş/orta/geniş hashtag karması ve arama görünürlüğü önerir.

```text
[Platform] için hashtag ve keşfedilebilirlik stratejisti olarak çalış.

Hesap: [konu, kitle, büyüklük]
İçerik: [bu gönderinin konusu]

Format:
1. 3 katmanlı hashtag seti: niş (düşük hacim, yüksek alaka) / orta /
   geniş — her katmanda 3-5 öneri ve neden.
2. Gönderi metnine doğal yerleşecek arama anahtar ifadeleri (platform
   içi arama için — hashtag dışında).
3. Kaçınılacaklar: spam görünen, alakasız-popüler, gölge yasak riskli
   etiketler.

Kural: hacim rakamı uydurma; "yüksek/orta/düşük" tahmin olduğunu belirt ve
platform içi doğrulama adımını tarif et.
```

---

## Kaynaklar

Şablonlar, prompts.chat / awesome-chatgpt-prompts koleksiyonundaki sosyal
medya ve pazarlama kalıplarından (CC0 1.0) esinlenerek kitabın prompt
anatomisine göre yeniden yazılmıştır. Rakip analizi ve performans raporu
şablonlarındaki "veri vermeden analiz isteme" ilkesi, Cilt 1'in
halüsinasyon bölümündeki doğrulama yaklaşımının uygulamasıdır.

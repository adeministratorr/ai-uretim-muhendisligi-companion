# Strateji ve Pazarlama Analizi Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Strateji ve Pazarlama"
concepts:
  - SWOT analizi
  - rakip ve pazar analizi
  - konumlandırma
last_verified: "2026-07"
```

Strateji promptlarının en büyük tuzağı: model, veri vermeseniz de size
dolu dolu bir analiz yazar — ve o analiz jeneriktir. Bu dosyadaki tüm
şablonlar aynı ilkeyle kurulmuştur: **girdiyi siz verirsiniz, model
yapılandırır ve sorgular.** Sosyal medya özelindeki rakip analizi için
bkz. [11-sosyal-medya-yonetimi.md](11-sosyal-medya-yonetimi.md); genel iş
kararı karşılaştırması için [03-is-ve-verimlilik.md](03-is-ve-verimlilik.md).

---

## 1. SWOT Analizi (Sorgulamalı)

**Ne işe yarar:** Klasik "SWOT yaz" promptunun jenerik çıktısını, iki
aşamalı sorgulamayla şirkete özgü hale getirir.

```text
Deneyimli bir strateji danışmanısın. [Şirket/ürün] için SWOT analizi
yapacağız — ama iki aşamada:

AŞAMA 1 (şimdi): Sana vereceğim bilgileri oku, SWOT yazmadan önce bana
en fazla 5 netleştirme sorusu sor — özellikle rakiplere göre konumumuz,
müşteri kaybı nedenleri ve bağımlılıklarımız (tek müşteri/tedarikçi/kanal)
hakkında.

AŞAMA 2 (cevaplarımdan sonra): SWOT tablosunu yaz. Kurallar:
- Her madde şirkete ÖZGÜ olmalı; sektördeki herkes için doğru olan maddeler
  ("rekabet yoğun", "ekonomik belirsizlik") yasak.
- Her maddenin yanına dayanağı (verdiğim hangi bilgiden çıktı).
- Güçlü yön ancak rakibe KIYASLA güçlüyse yazılır; içerik olarak iyi ama
  herkes yapıyorsa "sektör standardı" der geçersin.
- Sonda: SWOT'tan çıkan 3 stratejik hamle önerisi — her biri bir S/O
  eşleşmesi veya W/T savunması olarak gerekçeli.

Şirket bilgileri:
[ne satıyor, kime, kaç yıllık, ekip, gelir modeli, bilinen sorunlar,
ana rakipler hakkında bildikleriniz]
```

**Notlar:** "Sektördeki herkes için doğru madde yasak" kısıtı, SWOT
promptlarındaki en etkili tek cümledir.

---

## 2. Rakip Analizi (İş Geneli)

**Ne işe yarar:** Topladığınız rakip bilgilerini konumlandırma haritasına
ve aksiyona çevirir.

```text
Rekabet analisti olarak çalış. Aşağıda ana rakipler hakkında topladığım
bilgiler var:

<rakipler>
[Her rakip için: ürün/hizmet kapsamı, fiyatlandırma (biliniyorsa), hedef
segment, güçlü göründüğü yönler, müşteri yorumlarından notlar, son
hamleleri (lansman, fiyat değişikliği, ortaklık)]
</rakipler>

Biz: [aynı başlıklarla kendi durumumuz]

Format:
1. Karşılaştırma matrisi: fiyat konumu × hedef segment × ayırt edici
   özellik.
2. Her rakibin görünen stratejisi ve muhtemel sıradaki hamlesi — hangi
   kanıta dayandığını belirterek; kanıt zayıfsa "spekülatif" etiketi.
3. Bizim savunulabilir farkımız: rakiplerin kopyalaması zor olan ne?
   (Yoksa, bunu açıkça söyle — yanlış güven verme.)
4. Boşluk analizi: kimsenin iyi hizmet etmediği segment/ihtiyaç.
5. İzleme planı: her rakip için hangi sinyali (fiyat sayfası, iş ilanları,
   duyurular) hangi sıklıkla kontrol etmeliyim?

Kural: verdiğim bilgide olmayan pazar payı, gelir, kullanıcı sayısı
uydurma. Bilgim eksikse analizden önce hangi bilgiyi nereden toplamam
gerektiğini söyle.
```

---

## 3. Hedef Kitle Personası

**Ne işe yarar:** Gerçek müşteri verisinden (görüşme notları, yorumlar,
destek kayıtları) persona çıkarır — hayalî persona üretmez.

```text
Pazarlama araştırmacısısın. Aşağıdaki GERÇEK müşteri verilerinden persona
çıkaracaksın:

<veriler>
[müşteri görüşme notları / anket cevapları / destek talepleri /
satış görüşmesi özetleri / yorumlar]
</veriler>

Format:
1. Veride beliren 2-4 farklı müşteri tipi; her biri için: kim, hangi
   sorunu çözmeye çalışıyor, satın alma tetikleyicisi, tereddüt nedeni,
   bilgi aldığı kanallar — HER alanın yanında veriden alıntı/dayanak.
2. Veriden ÇIKMAYAN ama persona için önemli alanları "bilinmiyor" olarak
   işaretle ve nasıl öğrenileceğini öner (görüşme sorusu taslağı).
3. Her persona için "bu personaya YANLIŞ mesaj" örneği — neyin itici
   olacağı.

Kural: veriye dayanmayan demografik süsleme yok (yaş/meslek uydurma);
persona sayısını veri çeşitliliği belirler, zorla 4'e tamamlama.
```

---

## 4. Konumlandırma ve Değer Önerisi

**Ne işe yarar:** "Biz neyiz, kimin için, neden biz" cümlesini disiplinle
kurar.

```text
Konumlandırma stratejistisin (April Dunford'un yaklaşımıyla çalışırsın:
konumlandırma iddia değil, kanıtlanabilir bağlam seçimidir).

Girdiler:
- Ürün: [ne yapıyor — özellik düzeyinde]
- En iyi müşterilerimiz: [bizi çok sevenler kim, neden]
- Alternatifler: [müşteri bizi almasa ne yapardı — rakip ürün, Excel,
  hiçbir şey]
- Kanıtlar: [ölçülebilir sonuçlar, referanslar]

Format:
1. Rekabet alternatiflerine göre gerçekten farklı olduğumuz 2-3 yetenek.
2. Bu yeteneklerin en çok değer ürettiği müşteri segmenti.
3. Konumlandırma cümlesi: "[Segment] için, [alternatiflerin aksine],
   [kanıtlanabilir fark] sağlayan [kategori]" — 3 varyant.
4. Bu konumlandırmayı test edecek 3 soru (müşteriye sorulacak).
5. Kanıtsız iddiaları işaretle: hangi cümle şu an pazarlama temennisi,
   hangi kanıtla desteklenir hale gelir?
```

---

## 5. Pazarlama Kampanya Planı

**Ne işe yarar:** Kampanyayı hedef → mesaj → kanal → bütçe → ölçüm
zincirinde planlar.

```text
Performans odaklı bir pazarlama planlamacısısın.

Kampanya konusu: [lansman/sezon/kampanya]
Hedef: [SMART: hangi metrik, ne kadar, ne zamana]
Bütçe: [tutar] — kanal dağılımını sen önereceksin
Hedef kitle: [persona özeti — dosyadaki 3. şablonun çıktısı buraya girer]
Geçmiş veri: [önceki kampanyalardan ne öğrendik]

Format:
1. Ana mesaj ve 3 kanal-uyarlaması (bkz. dosya 11'in platform şablonu).
2. Kanal planı ve bütçe dağılımı — her kanala gerekçe: bu kitle orada mı,
   geçmiş veri ne diyor?
3. Zaman çizelgesi: hazırlık → lansman → optimizasyon fazları.
4. Ölçüm planı: hangi metrik başarıyı gösterir, hangi metrik erken uyarı
   verir, ne zaman "çalışmıyor" deyip keseriz (kill criteria).
5. Riskler: bütçenin çöpe gideceği 2-3 senaryo ve önlemleri.

Kural: sektör ortalaması CTR/CPC gibi rakamları kesin veri gibi sunma;
"kendi ilk haftanızın verisiyle kalibre edin" uyarısı ekle.
```

---

## 6. Pazar Büyüklüğü Tahmini (Fermi Disiplini)

**Ne işe yarar:** TAM/SAM/SOM tahminini şeffaf varsayımlarla kurar;
"pazar X milyar dolar" kopyala-yapıştırını engeller.

```text
Titiz bir pazar analisti olarak [ürün/hizmet] için pazar büyüklüğü
tahmini kur.

Bildiklerim: [hedef segment, coğrafya, fiyat, bilinen sektör verileri]

Format:
1. TAM/SAM/SOM tanımlarını BU işe özgü kur (jenerik tanım değil).
2. Her katman için Fermi hesabı: varsayım × varsayım × varsayım — her
   varsayımın yanında (a) dayanağı, (b) güven düzeyi (yüksek/orta/tahmin),
   (c) hangi kaynaktan doğrulanabileceği.
3. Duyarlılık: hangi varsayım %20 oynarsa sonuç en çok değişir?
4. Aralık ver, tek sayı verme: kötümser / baz / iyimser.

Kural: kaynağını bilmediğin sektör istatistiği kullanma; kullandıysan
[DOĞRULANMALI] etiketi koy. Yatırımcı sunumuna girecek her rakam için
birincil kaynak öner.
```

---

## Kaynaklar

Şablonlar; prompts.chat koleksiyonundaki pazarlama/strateji kalıpları
(CC0), Anthropic Prompt Library'nin (arşiv) "Brand builder" ve iş analizi
kalıpları ve yaygın strateji çerçeveleri (SWOT, TAM/SAM/SOM, April
Dunford'un "Obviously Awesome" konumlandırma yaklaşımı) üzerine, kitabın
prompt anatomisi ve doğrulama ilkeleriyle yeniden yazılmıştır.

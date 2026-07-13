# Günlük Hayat Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Günlük Hayat"
concepts:
  - satın alma araştırması
  - seyahat planlama
  - karşılaştırmalı karar verme
last_verified: "2026-07"
```

Prompt mühendisliği yalnız iş aracı değildir; en sık kullanım gerçek
hayattadır. Bu dosyadaki promptların ortak deseni şudur: **modeli satıcı
değil danışman konumuna koyun** — kriterlerinizi önce siz belirleyin,
modelden seçenekleri o kriterlere göre işlemesini isteyin.

> **Güncel bilgi uyarısı:** Fiyat, sefer, stok ve kampanya bilgisi hızla
> değişir. Web erişimi olmayan bir modelin verdiği fiyat/sefer bilgisi
> eğitim verisinden kalmadır; web erişimli araçlarda bile rezervasyon
> öncesi resmî site doğrulaması şarttır. Bu dosyadaki promptlar bu yüzden
> modelden "fiyat söylemesini" değil, "arama ve karar stratejisi
> kurmasını" ister.

---

## 1. Uçak Bileti / Seyahat Arama Stratejisi

**Ne işe yarar:** Bilet aramasını sistematikleştirir; web erişimli
araçlarda (veya aramayı kendiniz yaparken) neyi hangi sırayla
kontrol edeceğinizi netleştirir.

```text
Deneyimli bir seyahat planlamacısısın.

Rota: [nereden → nereye] (yakın alternatif havalimanları dahil öner)
Tarihler: [kesin / ± n gün esnek]
Yolcular ve bagaj: [kişi sayısı, kabin/check-in bagaj ihtiyacı]
Bütçe ve tercihler: [üst sınır; aktarma toleransı; saat tercihi]

Format:
1. Arama planı: hangi tarih kombinasyonları ve alternatif havalimanları
   denenecek; esneklik nerede en çok fiyat düşürür.
2. Karşılaştırma tablosu şablonu: fiyat + bagaj dahil TOPLAM maliyet +
   aktarma süresi + iptal/değişiklik koşulu (çıplak bilet fiyatına değil
   toplam maliyete göre karşılaştırılacak).
3. Tuzak listesi: temel/basic fare bagaj sürprizleri, kısa aktarma riski,
   ayrı biletle aktarma (self-transfer) riski, gece varış maliyeti.
4. Bana soracağın netleştirme soruları (varsa).

Kural: güncel fiyat/sefer bilgisi verme; verirsen tahminî olduğunu ve
doğrulanması gerektiğini açıkça yaz.
```

---

## 2. Satın Alma Araştırması (Büyük Alışveriş)

**Ne işe yarar:** "Hangi [ürün]ü alayım" sorusunu, ihtiyaç analizi →
kriter → kısa liste akışına çevirir.

```text
Tarafsız bir satın alma danışmanısın; hiçbir markadan komisyon almıyorsun.

Almak istediğim: [ürün kategorisi — örn. robot süpürge, dizüstü, klima]
Kullanım senaryom: [kim, ne sıklıkta, nerede, ne için]
Bütçe: [aralık] — aşmam gereken durumda gerekçesini isterim
Benim için önemli: [öncelik sırasıyla 3-5 kriter]
Umurumda olmayan: [pahalılaştıran ama işime yaramayacak özellikler]

Format:
1. Önce ihtiyacımı sorgula: senaryoma göre yanlış kategoriye bakıyor
   olabilir miyim? (örn. bu kullanım için X yerine Y sınıfı yeter/gerek)
2. Karar kriterleri tablosu: hangi spec benim senaryomda gerçekten fark
   yaratır, hangisi pazarlama süsü — gerekçeli.
3. Bu kriterlere göre pazardaki 3-5 güçlü aday tipi/segmenti ve her birinin
   ödünleşimi (trade-off).
4. Satın alma öncesi kontrol listesi: nereden doğrulanır (bağımsız test
   siteleri, kullanıcı yorumlarında nelere bakılır), garanti/iade koşulu.

Kural: model bilgin eğitim tarihinle sınırlı; güncel model adı/fiyat
verirken bunu belirt ve doğrulama adresi öner.
```

---

## 3. Ürün Performans Karşılaştırma

**Ne işe yarar:** Kısa listedeki 2-3 somut ürünü, sizin topladığınız
verilerle tarafsız karşılaştırır.

```text
Karşılaştırma analisti olarak çalış. Aşağıda kısa listemdeki ürünlerin
teknik özellikleri ve fiyatları var (kendim topladım):

<urunler>
[Ürün A: spec listesi, fiyat, garanti, satıcı]
[Ürün B: ...]
[Ürün C: ...]
</urunler>

Kullanım senaryom ve önceliklerim: [tekrar özetle]

Format:
1. Karşılaştırma tablosu — yalnız BENİM senaryomda fark yaratan satırlar;
   alakasız spec satırlarını "senaryonda önemsiz" diye ayrı listele.
2. Her ürün için: en güçlü olduğu senaryo + benim senaryomdaki zayıf yanı.
3. TL başına değer analizi: fiyat farkı, aldığım gerçek faydayı karşılıyor mu?
4. Kararı netleştirecek, verilerde OLMAYAN 2-3 kritik soru (örn. gürültü
   testi, gerçek pil ömrü) ve bunları nasıl doğrulayacağım.
5. Net öneri + hangi koşulda önerinin değişeceği.

Kural: verdiğim veride olmayan spec uydurma; iki ürün pratikte denkse
"denk, şuna göre seç" demekten çekinme.
```

---

## 4. Ev / Kira Kararı

**Ne işe yarar:** Duygusal ve büyük bir kararı kriter tablosuna döker.

```text
Konut kararlarında deneyimli, temkinli bir danışmansın.

Durum: [kiralık/satılık; bölge(ler); bütçe; ne zaman]
Zorunlular: [oda sayısı, ulaşım süresi, kat, ısınma tipi...]
Tercihler: [olursa iyi]
Adaylar (varsa):
[her aday için topladığım bilgiler]

Format:
1. Zorunlu/tercih listemi sorgula: unuttuğum tipik kriterler (aidat,
   depozito koşulları, bina yaşı/deprem, ses, internet altyapısı,
   güneş yönü) hangileri kritik olabilir?
2. Aday karşılaştırma tablosu + görüşte sorulacak sorular listesi.
3. Toplam maliyet hesabı şablonu: kira/taksit + aidat + ulaşım + ısınma
   (aylık gerçek maliyet, çıplak kira değil).
4. Kırmızı bayraklar: ilan/görüş sırasında vazgeçirtmesi gereken işaretler.

Kural: bölge fiyat seviyesi hakkında kesin rakam verme; piyasa doğrulama
yöntemi öner (benzer 10 ilan ortalaması gibi).
```

---

## 5. Sözleşme / Fatura / Resmî Belge Anlama

**Ne işe yarar:** Anlaşılmaz belgeyi sade dile çevirir ve risk noktalarını
işaretler. Hukuki danışmanlık DEĞİLDİR.

```text
Belgeleri sade dile çeviren bir asistansın (avukat değilsin ve hukuki
tavsiye vermiyorsun; bunu gerektiğinde hatırlat).

<belge>
[sözleşme/fatura/şartname metni — kişisel verileri çıkardıktan sonra]
</belge>

Format:
1. Bu belge ne diyor — 5 maddede, günlük dille.
2. Yükümlülüklerim: ne zaman, ne ödüyorum/taahhüt ediyorum; otomatik
   yenileme, cayma süresi, ceza koşulu var mı?
3. Dikkat çeken maddeler: standart dışı, tek taraflı veya belirsiz görünen
   hükümler — "bu maddeyi imzalamadan önce sor/netleştir" listesi.
4. Anlamadığın veya iki türlü okunabilen yerleri açıkça belirt.

Kural: "bu yasal mı/geçerli mi" sorularına kesin yanıt verme; önemli
tutarlarda uzman kontrolü öner.
```

**Not:** Belgeyi yüklemeden kişisel verileri (TC no, adres, hesap no)
maskeleyin.

---

## 6. Haftalık Yemek Planı + Alışveriş Listesi

**Ne işe yarar:** "Bu akşam ne pişirsem"i haftalık sisteme çevirir.

```text
Pratik bir ev yemekleri planlamacısısın (diyetisyen değilsin; sağlık
iddiası yerine genel denge gözet).

Hane: [kişi sayısı, çocuk var mı]
Kısıtlar: [alerji, beslenme tercihi, sevilmeyenler]
Zaman: hafta içi akşam en fazla [n] dakika pişirme
Elimde olanlar: [dolaptakiler]
Bütçe yaklaşımı: [ekonomik/normal]

Format:
1. 7 günlük akşam yemeği planı — her gün: yemek, süre, zorluk.
2. "Bir pişir iki gün ye" ve "artığı dönüştür" fırsatlarını işaretle.
3. Tek alışveriş listesi (reyonlara göre gruplu, eldekiler düşülmüş).
4. Hafta ortası B planı: en yorgun güne 10 dakikalık kurtarıcı alternatif.
```

---

## 7. Şikâyet / İade / Hak Arama Mektubu

**Ne işe yarar:** Tüketici sorunları için etkili, ölçülü ve belgeli
başvuru metni yazar.

```text
Tüketici hakları konusunda deneyimli bir yazışma asistanısın (hukuki
danışman değilsin).

Sorun: [ne oldu — tarih sırasıyla]
Elimdeki belgeler: [fatura, yazışma, fotoğraf...]
Talebim: [iade / değişim / onarım / bedel indirimi]
Muhatap: [satıcı müşteri hizmetleri / resmî başvuru]

Format:
1. Olayı tarih sıralı, duygusuz ve belgeye dayalı anlatan başvuru metni;
   talep net, süre belirtilmiş.
2. Eksik belge/bilgi uyarısı: başvuruyu güçlendirmek için ne toplamalıyım?
3. Sonuç alınamazsa sonraki kademe (Türkiye için: satıcı → Tüketici Hakem
   Heyeti/ilgili mercii) ve başvuru öncesi kontrol listesi.

Kural: yasal süre ve parasal sınır gibi güncellenen bilgileri kesin rakam
olarak verme; resmî kaynaktan kontrol edilmesini söyle.
```

---

## Kaynaklar

Şablonlar günlük kullanım senaryolarından derlenmiş, kitabın prompt
anatomisi (persona, görev, bağlam, format, kısıt, başarı kriteri) ve
Bölüm 7'deki halüsinasyon/doğrulama ilkeleriyle hizalanmıştır. prompts.chat
koleksiyonundaki (CC0) seyahat ve kişisel asistan kalıpları çıkış noktası
olarak kullanılmıştır.

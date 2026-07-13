# İş ve Verimlilik Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — İş ve Verimlilik"
concepts:
  - toplantı notu yapılandırma
  - karar analizi
  - pazarlama ve satış iletişimi
last_verified: "2026-07"
```

Bu bölümdeki promptlar şirket içi bilgiyle çalışır. İki uyarı:

1. Gizli/kişisel veriyi prompta yapıştırmadan önce kurumunuzun AI kullanım
   politikasını kontrol edin (bkz. Cilt 1'in veri hassasiyeti bölümü ve
   `../cilt-1-prompting/exercises/data-sensitivity-classifier/`).
2. Model çıktısı karar destek malzemesidir, karar değildir.

---

## 1. Toplantı Transkriptinden Aksiyon Çıkarma

**Ne işe yarar:** Ham toplantı notunu/transkriptini karar + aksiyon + açık
konu yapısına dönüştürür.

**Prompt:**

```text
Aşağıdaki toplantı transkriptini işle. Çıktı formatı:

## Kararlar
- [karar] — (dayanak: transkriptteki ilgili ifade)

## Aksiyonlar
| Aksiyon | Sahibi | Tarih |
|---|---|---|
(Sahibi veya tarihi söylenmemişse "belirtilmedi" yaz; tahmin etme.)

## Açık Konular
- Tartışıldı ama karara bağlanmadı: [liste]

## Belirsizlikler
- Transkriptte çelişkili veya anlaşılmaz bulduğun yerler.

Kurallar: transkriptte olmayan hiçbir kararı/aksiyonu yazma. Kim olduğu
belirsiz konuşmacıları "katılımcı" olarak geçir, isim uydurma.

Transkript:
[metin]
```

---

## 2. Karar Analizi (Seçenek Karşılaştırma)

**Ne işe yarar:** Bir iş kararını yapılandırılmış biçimde karşılaştırır;
etki/çaba matrisi mantığını uygular.

**Prompt:**

```text
Deneyimli bir strateji danışmanısın. Şu kararı analiz et:

Karar: [ne seçilecek]
Seçenekler: [A, B, C]
Kısıtlar: [bütçe, süre, ekip, mevzuat]
Başarı ölçütü: [6 ay sonra neye bakıp "doğru karardı" diyeceğiz]

Format:
1. Her seçenek için: beklenen etki (1-5), tahmini çaba (1-5), en büyük
   risk, riskin erken uyarı işareti.
2. Karşılaştırma tablosu.
3. "Bilmediklerimiz" listesi: analizi değiştirebilecek eksik bilgiler —
   bunlar öğrenilmeden karar verilmeli mi, söyle.
4. Önerin ve hangi koşulda önerinin değişeceği.

Puanları gerekçelendir; gerekçesiz sayı yazma.
```

**Notlar:** Çalışan bir etki/çaba aracı için bkz.
`../cilt-1-prompting/exercises/impact-effort-matrix/`.

---

## 3. Pazarlama Metni (Ürün/Kampanya)

**Ne işe yarar:** Özellik listesini fayda diline çevirir; hedef segmente göre
mesaj üretir.

**Prompt:**

```text
Deneyimli bir pazarlama metin yazarısın (copywriter).

Ürün: [ad ve tek cümlelik tanım]
Hedef segment: [kim; hangi sorunu yaşıyor]
Kanıtlar: [gerçek rakamlar, müşteri yorumları, sertifikalar — SADECE
gerçek olanlar]
Kanal: [web ana sayfa / e-posta / reklam metni]
İstenen aksiyon: [tıkla / kaydol / demo iste]

Format: 3 farklı açıyla (sorun odaklı, sonuç odaklı, karşılaştırma odaklı)
başlık + kısa metin + CTA üret.

Kurallar:
- Verdiğim kanıt setinin dışına çıkma; rakam ve müşteri yorumu uydurma.
- "Devrim", "çığır açan" gibi enflasyona uğramış kelimeler yasak.
- Hedef segmentin diliyle yaz, sektör jargonunu [uygunsa/uygun değilse] kullan.
```

---

## 4. Satış: İtiraz Karşılama Provası

**Ne işe yarar:** Satış görüşmesi öncesi, modeli zor müşteri rolüne sokarak
prova yaptırır.

**Prompt:**

```text
Rol yapacağız. Sen [sektör] sektöründe [unvan] pozisyonunda, bütçesi kısıtlı
ve mevcut çözümünden ayrılmaya isteksiz bir potansiyel müşterisin. Ben sana
[ürün] satmaya çalışan satışçıyım.

Kurallar:
- Gerçekçi ol: ne kolay ikna ol, ne kestirmeden reddet.
- Her cevabında en fazla 3-4 cümle; monolog yok.
- Ben "MOLA" yazınca rolden çık ve son turumu değerlendir: neyi iyi
  yaptım, hangi itirazı kaçırdım, ne demeliydim.
- Ben "DEVAM" yazınca role geri dön.

Sen başla: az önce demo izledin ve ikna olmamış görünüyorsun.
```

**Notlar:** MOLA/DEVAM anahtarı, tek oturumda hem prova hem koçluk almayı
sağlar; rol karışmasını önler.

---

## 5. İK: Mülakat Soru Seti

**Ne işe yarar:** Pozisyon tanımından, yetkinlik bazlı ve ayrıştırıcı mülakat
soruları üretir.

**Prompt:**

```text
Deneyimli bir işe alım uzmanısın. [Pozisyon] için mülakat soru seti hazırla.

Pozisyonun kritik yetkinlikleri: [3-5 yetkinlik]
Seviye: [junior/mid/senior]

Her yetkinlik için:
1. Bir davranışsal soru (geçmiş deneyim: "... bir durumu anlatın").
2. Bir senaryo sorusu (varsayımsal durum, bizim bağlamımızdan).
3. İyi cevabın işaretleri ve kırmızı bayraklar (madde listesi).

Kurallar:
- Google'lanabilir bilgi soruları sorma; düşünme biçimini ölçen sorular sor.
- Yasal olarak sorulmaması gereken alanlara (yaş, medeni durum, din vb.)
  girme.
- Aynı yetkinliği ölçen soruları çeşitlendir ki adaylar arası karşılaştırma
  yapılabilsin.
```

---

## 6. Haftalık Planlama / Önceliklendirme

**Ne işe yarar:** Dağınık görev listesini kapasiteye göre önceliklendirir.

**Prompt:**

```text
Pragmatik bir üretkenlik koçusun. Görev listemi önceliklendirmeme yardım et.

Görevlerim: [liste — mümkünse tahmini süre ve son tarihle]
Bu haftaki gerçek kapasitem: [saat]
Sabit taahhütlerim: [toplantılar vb.]
Haftanın tek kritik sonucu: [bu hafta tek şey biterse ne bitmeli]

Format:
1. Görevleri şu kovalara ayır: bu hafta / delege et veya kısalt / bilinçli
   ertele / hiç yapma.
2. "Hiç yapma" ve "ertele" kovalarındaki her görev için tek cümle gerekçe.
3. Kapasitemi aşan plan yapma; toplam süre kapasiteyi aşıyorsa neyin
   feda edildiğini açıkça söyle.
4. Bana sormam gereken 2 soruyla bitir (planın varsayımlarını test eden).
```

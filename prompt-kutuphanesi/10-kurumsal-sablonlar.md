# Kurumsal Şablonlar

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Kurumsal Şablonlar"
concepts:
  - müşteri desteği
  - kurumsal iletişim
  - PRD ve marka brifi
last_verified: "2026-07"
```

Bu dosya, bir şirketin günlük operasyonlarında tekrar tekrar kullanılacak
promptları toplar. [03-is-ve-verimlilik.md](03-is-ve-verimlilik.md) bireysel
iş akışlarına, bu dosya **kurumsal süreçlere** odaklanır. Tümü şablon
mantığıyla yazılmıştır: bir kez uyarlayın, ekipçe kullanın, sürümleyin
(prompt-as-config yaklaşımı için bkz. dosya 08).

> **Kurumsal kullanımda üç kural:**
> 1. Müşteri verisi/kişisel veri içeren promptlar için önce KVKK ve şirket
>    AI politikası kontrolü (bkz. `../cilt-1-prompting/exercises/data-sensitivity-classifier/`).
> 2. Dışarı çıkan her metin (müşteri yanıtı, duyuru, teklif) insan
>    onayından geçer; model taslak üretir, sorumluluk üstlenmez.
> 3. Aynı işi yapan promptu ekipte herkes kendine göre yazmasın; şablonu
>    ortak depoda tutun, iyileştirmeleri şablona işleyin.

---

## 1. Müşteri Destek Yanıtı (Bilgi Bankası Sınırlı)

**Ne işe yarar:** Destek ekibinin, şirket bilgi bankasının dışına çıkmayan
yanıt taslakları üretmesini sağlar. Halüsinasyon sınırı şablonun içindedir.

```text
[ŞİRKET] müşteri destek ekibi için yanıt taslağı hazırlayan asistansın.

Kurallar:
- YALNIZCA aşağıdaki bilgi bankasına dayan. Bilgi bankasında olmayan bir
  şey sorulursa "bu konuyu ekibimize iletiyorum" kalıbıyla eskale et;
  tahmin yürütme, politika uydurma.
- Ton: [profesyonel-sıcak / resmî]; müşteri öfkeliyse önce kabul cümlesi.
- Yanıt en fazla [n] cümle + gerekiyorsa numaralı adımlar.
- İade/ücret/hukuki taahhüt içeren cümleleri [ONAY GEREKLİ] etiketiyle
  işaretle — bunlar insan onayı olmadan gönderilemez.

Bilgi bankası:
[SSS, politika metinleri, ürün bilgisi]

Müşteri mesajı:
[mesaj]
```

---

## 2. Ürün Gereksinim Dokümanı (PRD)

**Ne işe yarar:** Dağınık özellik fikrini standart PRD yapısına döker.

```text
Deneyimli bir ürün yöneticisisin. Aşağıdaki özellik fikri için PRD taslağı
yaz. Başlıklar: Özet, Problem Tanımı, Hedefler ve Başarı Metrikleri,
Kullanıcı Hikâyeleri, Kapsam Dışı (açıkça), Teknik Gereksinimler,
Riskler ve Açık Sorular.

Kurallar:
- Bilmediğin iş bağlamını uydurma; karar gerektiren her boşluğu
  "AÇIK SORU:" etiketiyle bırak ve kime sorulacağını öner.
- Başarı metriklerini ölçülebilir yaz (hedef rakam + ölçüm yöntemi).
- "Kapsam Dışı" bölümünü boş geçme; en az 3 bilinçli dışlama yaz.

Özellik fikri: [açıklama]
Hedef kullanıcı: [kim]
İş hedefi: [neden şimdi]
```

---

## 3. Kurumsal Rapor → Yönetim Notu

**Ne işe yarar:** Uzun raporu (faaliyet raporu, denetim çıktısı, pazar
analizi) yönetim ekibine gidecek kısa nota çevirir. Uzun belgeyi
sınırlayıcı içinde verin:

```text
Aşağıdaki raporu analiz et:

<rapor>
[rapor metni]
</rapor>

Bu raporu ekibime göndereceğim kısa bir yönetim notuna dönüştür. Amaç:
ekibin [hangi konuda] güncel kalması ve önümüzdeki çeyrekte beklenen
[operasyonel/finansal] riskleri nitel olarak öngörmesi. Ana mesaj başta;
kilit eğilimler madde madde, her maddenin rapordan dayanağıyla; sonda
"izlenmesi gerekenler" listesi. Raporda olmayan hiçbir sayı veya iddia
ekleme.
```

---

## 4. Marka Kimliği / Kampanya Brifi

**Ne işe yarar:** Ajansa veya tasarım ekibine verilecek brifi yapılandırır.

```text
Deneyimli bir marka stratejistisin. Şu bilgilerle kapsamlı bir tasarım
brifi hazırla: marka adı önerileri, logo yönü, renk paleti, tipografi,
görsel stil, ses tonu (tone of voice) ve marka kişiliği — hepsi birbiriyle
tutarlı bir bütün olarak.

Marka bilgileri:
- Sektör ve ürün: [ne satıyor]
- Hedef kitle: [kim, hangi ihtiyaç]
- Değer önerisi: [tek cümle]
- Kaçınılacaklar: [rakip benzerliği, klişeler]

Her öneri için "neden bu kitleye uygun" gerekçesi ekle. Görsel üretim
aşaması için, brifin sonuna dosya 06'daki anatomiye uygun 3 örnek görsel
promptu ekle (İngilizce).
```

---

## 5. İş İlanı Yazımı

**Ne işe yarar:** Pozisyon gereksinimlerinden, ayrımcılık içermeyen ve
gerçekçi bir ilan üretir.

```text
Deneyimli bir işveren markası uzmanısın. [Pozisyon] için iş ilanı yaz.

Girdiler: sorumluluklar [liste], zorunlu yetkinlikler [liste], tercih
edilenler [liste], çalışma modeli [ofis/hibrit/uzaktan], ekip [büyüklük].

Kurallar:
- "Zorunlu" listesini 5 maddeyle sınırla; her eklenen zorunluluk aday
  havuzunu daraltır — gereksiz olanı "tercih edilen"e taşı ve belirt.
- Yaş, cinsiyet, askerlik, medeni durum iması yok; "genç ve dinamik ekip"
  gibi kodlanmış ifadeler de dahil.
- Rolü olduğundan parlak gösterme; ilk 90 günün gerçekçi özetini ekle.
- Şirketin vaadi (maaş aralığı, gelişim, esneklik) somut olsun; verilen
  bilgide yoksa [BİLGİ GEREKLİ] diye işaretle.
```

---

## 6. Teklif / RFP Yanıtı İskeleti

**Ne işe yarar:** Müşteri talebine (RFP/şartname) yanıt dokümanının
iskeletini kurar ve şartname maddeleriyle eşleme tablosu üretir.

```text
[Sektör] alanında teklif yazan deneyimli bir iş geliştirme uzmanısın.

Şartname/talep:
<sartname>
[metin]
</sartname>

Bizim yetkinliklerimiz: [ürün/hizmet, referanslar, ekip — SADECE gerçek
olanlar]

Çıktı:
1. Şartname maddesi ↔ bizim karşılığımız eşleme tablosu; karşılayamadığımız
   maddeleri gizleme, "kısmi/karşılanmıyor" olarak işaretle ve telafi
   stratejisi öner.
2. Teklif dokümanı iskeleti (yönetici özeti, çözüm yaklaşımı, iş planı,
   ekip, referanslar) — her bölümde yazılacakların madde listesi.
3. Kazanma temamız: bu müşteri için en güçlü 2-3 farklılaşma noktası.

Kural: yetkinlik listemizde olmayan hiçbir yeteneği "var" yazma.
```

---

## 7. İç Duyuru / Değişiklik İletişimi

**Ne işe yarar:** Zor iç duyuruları (reorganizasyon, politika değişikliği,
sistem geçişi) net ve güven koruyarak yazar.

```text
Kurumsal iletişim uzmanısın. Şu iç duyuruyu yaz:

Değişiklik: [ne değişiyor]
Neden: [gerçek gerekçe — süsleme yok]
Kimi nasıl etkiliyor: [gruplar ve etkiler]
Tarih ve geçiş planı: [somut adımlar]
SSS'de cevaplanacak muhtemel endişeler: [liste]

Kurallar:
- İlk paragrafta ne değiştiğini ve kimi etkilediğini söyle; gömme.
- Kurumsal klişe yasak ("heyecanla duyururuz", "yolculuğumuzda").
- Kötü haberi iyi haber cilasıyla kaplama; zorluğu kabul et, desteği söyle.
- Sonda: soru kanalı + tarihli sonraki adım.
```

---

## 8. Toplantı Gündemi ve Karar Şablonu

**Ne işe yarar:** Toplantıyı çıktı odaklı planlar; "bilgilendirme
toplantısı" israfını keser.

```text
Toplantı tasarım danışmanısın. Şu toplantı için gündem hazırla:

Amaç: [toplantı bitince elimizde ne olmalı — karar mı, plan mı, hizalama mı]
Katılımcılar: [roller]
Süre: [dakika]

Kurallar:
- Her gündem maddesine: süre + sahip + beklenen çıktı (karar/aksiyon/bilgi).
- Karar maddelerinde karar yöntemini yaz (sahibi karar verir / oy / consensus).
- Toplantı öncesi okunacakları ayır; toplantıda sunum yapılmaz, tartışılır.
- Amaç e-postayla çözülebiliyorsa bunu açıkça söyle ve e-posta taslağını ver.
```

---

## Kaynaklar

Bu dosyadaki şablonların bir bölümü şu koleksiyonlardaki İngilizce
promptlardan uyarlanmış ve kitabın prompt anatomisine göre yeniden
yazılmıştır:

- prompts.chat / awesome-chatgpt-prompts (github.com/f/awesome-chatgpt-prompts)
  — prompt içerikleri CC0 1.0 lisanslıdır (kamu malı); "PRD", "recruiter",
  "advertiser" kalıplarının çıkış noktası.
- Anthropic Prompt Library (2025'te yayından kaldırıldı; arşiv üzerinden) —
  "Corporate clairvoyant" (rapor→memo), "Meeting scribe", "Brand builder"
  kalıplarının çıkış noktası; uyarlanarak kullanılmıştır.

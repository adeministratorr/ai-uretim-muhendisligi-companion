# Yazma ve İçerik Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Yazma ve İçerik"
concepts:
  - üslup dönüştürme
  - özetleme
  - hedef kitle uyarlama
last_verified: "2026-07"
```

Metin modellerinin tümünde çalışır. Yazma promptlarında en sık yapılan hata,
hedef kitleyi ve başarı kriterini boş bırakmaktır: "blog yazısı yaz" diyen,
kime ve neden yazıldığını modele devretmiş olur.

---

## 1. Blog Yazısı / Makale Taslağı

**Ne işe yarar:** Konu + kitle + amaç üçlüsünden yapılandırılmış taslak, sonra
tam metin üretir. İki aşamalı olması bilinçlidir: taslağı onaylamadan tam
metne geçmeyin.

**Prompt:**

```text
[Alan] konusunda yazan deneyimli bir içerik yazarısın.

Konu: [konu]
Hedef kitle: [kim okuyacak; bilgi düzeyi ne]
Amaç: [okur yazıyı bitirince ne düşünmeli/yapmalı]
Ton: [örn. samimi ama yüzeysel olmayan; pazarlama dili yok]
Uzunluk: yaklaşık [n] kelime

Önce SADECE taslak ver: başlık önerisi (3 seçenek), bölüm başlıkları ve her
bölümün tek cümlelik özeti. Ben taslağı onaylayınca tam metni yazacağız.

Kurallar:
- Genel geçer giriş cümlesi yok ("Günümüzde teknoloji hızla gelişiyor" gibi).
- Her iddia ya somut örnekle ya veriyle desteklenir; veri uyduramazsın,
  kaynağını bilmediğin sayıyı [KAYNAK GEREKLİ] diye işaretlersin.
- Abartılı sıfatlardan kaçın; okurun zekâsına güven.
```

**Notlar:** `[KAYNAK GEREKLİ]` işaretleme kuralı, uydurma istatistiklerin
metne karışmasını önlemenin en pratik yoludur.

---

## 2. Zor E-posta

**Ne işe yarar:** Ret, gecikme bildirimi, fiyat artışı, hatırlatma gibi
hassas e-postaları tonu ayarlayarak yazar.

**Prompt:**

```text
Profesyonel iletişimde deneyimli birisin. Şu e-postayı yazmama yardım et:

Alıcı: [kim; ilişkimiz ne — müşteri/yönetici/tedarikçi]
Durum: [ne oldu / ne olacak]
Vermek istediğim mesaj: [özü tek cümle]
Korumak istediğim şey: [ilişki / güvenilirlik / sınırlarım]
Ton: [net ama sıcak / resmî / özür içeren ama ezik olmayan]

Kurallar:
- En fazla [n] cümle; dolgu cümlesi yok.
- Suçlayıcı dil yok, ama sorumluluğu belirsizleştiren edilgen çatı da yok.
- Somut bir sonraki adımla bitir (tarih, eylem, soru).

İki sürüm ver: biri daha kısa/doğrudan, biri daha yumuşak. Farklarını tek
cümleyle açıkla.
```

---

## 3. Yönetici Özeti / Uzun Metin Özetleme

**Ne işe yarar:** Rapor, transkript veya makaleyi karar vericinin
kullanabileceği yoğunlukta özetler.

**Prompt:**

```text
Aşağıdaki metni [kim için: örn. teknik olmayan yönetici] özetleyeceksin.

Format:
1. Tek cümlelik ana mesaj (BLUF — sonuç en başta).
2. En fazla 5 madde: temel bulgular; her madde metindeki dayanağıyla.
3. "Karar/eylem gerektirenler" başlığı altında, varsa bekleyen kararlar.
4. Özetin dışında bıraktığın önemli-orta düzey konuları tek satırda say.

Kurallar:
- Metinde olmayan hiçbir bilgi ekleme; yorum katman gerekiyorsa
  "yorum:" etiketiyle ayır.
- Metin bir görüş savunuyorsa, özetin bunu nötr aktarsın; sen taraf tutma.

Metin:
[metin]
```

**Notlar:** 4. madde ("dışarıda bıraktıkların") özetin ne kadar kayıplı
olduğunu görünür kılar; uzun belgelerde özellikle işe yarar.

---

## 4. Çeviri + Yerelleştirme

**Ne işe yarar:** Düz çeviri yerine, hedef dilde doğal duran ve terminolojiyi
koruyan çeviri üretir.

**Prompt:**

```text
[Kaynak dil] → [hedef dil] çevirisi yapan deneyimli bir çevirmensin.
Metin türü: [teknik doküman / pazarlama / sözleşme / arayüz metni]

Kurallar:
- Anlamı koru, kelimesi kelimesine çeviri yapma; hedef dilde doğal olsun.
- Şu terimleri sabit çevir: [terim listesi: X → Y].
- Çevrilmemesi gerekenler: [marka adları, kod, komutlar].
- Emin olamadığın kültürel referans veya deyim varsa çevirinin yanına
  [ÇN: ...] notu düş.

Çıktı: önce çeviri, sonra "Çevirmen notları" başlığıyla karar gerektiren
noktaların listesi.

Metin:
[metin]
```

---

## 5. Üslup Dönüştürücü

**Ne işe yarar:** Aynı içeriği farklı ton/mecralara uyarlar (rapor → LinkedIn
gönderisi, teknik doküman → müşteri duyurusu).

**Prompt:**

```text
Aşağıdaki metni [hedef mecra/tür: örn. LinkedIn gönderisi] olarak yeniden yaz.

Hedef kitle: [kim]
Korunacaklar: temel mesaj, teknik doğruluk, [varsa özel ifadeler].
Değişecekler: uzunluk (en fazla [n] kelime), ton ([örn. daha konuşkan]),
yapı (mecranın alışkanlıklarına uygun).

Kurallar:
- İçerik ekleme/çıkarma yapabilirsin ama anlamı bükemezsin.
- Clickbait yok; ilk cümle merak uyandırsın ama vaadini metin karşılasın.
- Orijinalde olmayan iddia ekleme.

Metin:
[metin]
```

---

## 6. Eleştirmen / Editör

**Ne işe yarar:** Kendi yazdığınız metni yayına göndermeden önce sert bir
editör gözünden geçirtir.

**Prompt:**

```text
Deneyimli ve açık sözlü bir editörsün. Aşağıdaki metni yayımlamadan önce
incele. Görevin beni mutlu etmek değil, metni iyileştirmek.

Sırayla:
1. Ana mesaj tek cümlede ne? (Sen söyle; benim kastımla uyuşmuyorsa
   sorun zaten orada.)
2. En zayıf 3 nokta: mantık boşluğu, desteksiz iddia, gereksiz bölüm.
3. Kesilebilecek cümleler/paragraflar (metni en az %[n] kısaltacak şekilde).
4. Somut yeniden yazım önerisi: en sorunlu 2 paragraf için önce/sonra.

Övgüyle başlama; doğrudan bulgulara geç. Metin gerçekten iyiyse nedenini
teknik olarak söyle, boş iltifat etme.

Metin:
[metin]
```

**Notlar:** "Beni mutlu etmek değil" ve "övgüyle başlama" kısıtları, modelin
varsayılan nezaket katmanını kırmak içindir; bu kısıtlar olmadan eleştiri
genellikle yüzeysel kalır.

# Video Üretim Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Video Üretim"
concepts:
  - kamera dili
  - native ses promptu
  - image-to-video
last_verified: "2026-07"
```

> **Sürüm uyarısı:** Video modelleri bu kütüphanenin en hızlı eskiyen
> alanıdır. Bilgiler 2026-07'de doğrulanmıştır. Prompt metinleri İngilizce
> verilmiştir (modeller ağırlıklı İngilizce sinematografi terimleriyle
> eğitilmiştir); video içindeki diyalog Türkçe yazılabilir.

---

## Üretim Modları Haritası

Video araçlarında prompt yazmadan önce hangi **modda** çalıştığınızı bilin;
aynı araçta bile mod değişince prompt kuralı değişir.

| Mod | Girdi → Çıktı | Prompt neyi tarif eder | Tipik kullanım |
|---|---|---|---|
| Text-to-video | metin → video | sahnenin ve hareketin tamamını | sıfırdan sahne |
| Image-to-video | görsel + metin → video | YALNIZ hareketi ve kamerayı | ürün görselini canlandırma, tutarlı karakter |
| İlk kare + son kare | 2 görsel + metin → video | iki kare ARASINDAKİ geçişi | plan bağlama, morph geçişleri |
| Video düzenleme / uzatma | video + metin → video | değişecek/eklenecek kısmı | mevcut klibi uzatma, öğe değiştirme |
| Dudak senkronu (lip sync) | video/avatar + ses veya diyalog metni | konuşmayı; tırnak içinde replik | konuşan kafa, dublaj, avatar sunum |

**Image-to-video örneği** (görsel: pencere kenarında bir kadın; görseli
yeniden TARİF ETMEYİN, sadece hareketi yazın):

```text
The camera slowly dollies in as she turns toward the window; her hair
moves in a light breeze.
```

**İlk kare + son kare örneği** (kare 1: sahnede önden söyleyen şarkıcı;
kare 2: arkasından seyirci görüntüsü — prompt geçişi tarif eder):

```text
The camera performs a smooth 180-degree arc shot, starting with the
front-facing view of the singer and circling around her to seamlessly
end on the POV shot from behind her on stage.
```

**Dudak senkronu örneği** (Veo 3 / Kling 3 gibi ses-native modellerde
tırnaklı diyalog senkronu tetikler; ayrı lip-sync araçlarında — HeyGen,
Hedra, Runway Act-One türü — replik metni ve ton ayrı alanlara girilir):

```text
Medium close-up of a friendly female presenter in a modern studio,
looking directly at the camera. She says in Turkish, warm and clear:
"Yapay zekâ araçlarını doğru kullanmak, doğru soru sormakla başlar."
Natural lip movement, subtle hand gesture, soft key light.
Ambient noise: quiet studio room tone.
```

Dudak senkronu kuralı: 4-8 saniyelik klibe 1-2 kısa replik; uzun cümle
senkronu bozar. Türkçe replikler tırnak içinde Türkçe yazılabilir — modele
"in Turkish" diye belirtmek telaffuz isabetini artırır.

---

## Ortak Prompt Anatomisi

Google'ın resmî formülü tüm araçlara genellenebilir:

**[Sinematografi] + [Özne] + [Eylem] + [Mekân] + [Stil ve Atmosfer] (+ [Ses])**

Yedi bileşenli hali: çekim ölçeği/kamera hareketi, stil, ışık, karakter
tarifi, mekân, eylem, diyalog. İlke: bir klip = bir plan (shot). 8 saniyelik
bir üretime iki sahnelik niyet sığdırmaya çalışmak en yaygın hatadır.

### Kamera hareketi sözlüğü

dolly in/out (yaklaş/uzaklaş) · pan (yatay çevrinme) · tilt (dikey) ·
tracking/follow shot (takip) · crane/boom (vinç) · orbit/arc (yörünge) ·
handheld (el kamerası) · Steadicam (akıcı) · FPV drone · POV · dolly zoom
(Vertigo etkisi) · static/locked-off shot (sabit — istiyorsanız açıkça
yazın, yoksa model kamerayı gezdirir).

---

## 1. Google Veo 3 / 3.1

Native sesli üretimin öncüsü. Ses istenmezse model rastgele müzik/mırıltı
ekler; her prompta en az bir ses satırı koyun.

**Ses sözdizimi (resmî):**

- Diyalog: tırnak içinde — `A woman says, "We have to leave now."`
  (dudak senkronunu tırnaklı diyalog tetikler)
- Efekt: `SFX: thunder cracks in the distance`
- Ortam: `Ambient noise: the quiet hum of a starship bridge`

**Atmosfer/stil örneği:**

```text
Medium shot, a tired corporate worker, rubbing his temples in exhaustion,
in front of a bulky 1980s computer in a cluttered office late at night.
The scene is lit by harsh fluorescent overhead lights and the green glow
of the monochrome monitor. Retro aesthetic, shot as if on 1980s color
film, slightly grainy.
```

**Kamera hareketi örneği:**

```text
Crane shot starting low on a lone hiker and ascending high above,
revealing they are standing on the edge of a colossal, mist-filled canyon
at sunrise, epic fantasy style, awe-inspiring, soft morning light.
```

**Zaman damgalı çok-planlı üretim (Veo 3.1'in güçlü tekniği):**

```text
[00:00-00:02] Medium shot from behind a young female explorer as she
pushes aside a large jungle vine to reveal a hidden path.
[00:02-00:04] Reverse shot of the explorer's face, her expression filled
with awe as she gazes upon ancient, moss-covered ruins. SFX: rustle of
dense leaves, distant exotic bird calls.
[00:04-00:06] Tracking shot following the explorer as she runs her hand
over the intricate carvings on a crumbling stone wall.
[00:06-00:08] Wide, high-angle crane shot revealing the lone explorer
standing small in the vast, forgotten temple complex. SFX: a swelling,
gentle orchestral score begins.
```

Veo 3.1 ayrıca referans görsellerle üretim ("ingredients to video") ve
ilk kare + son kare arası geçiş üretimi destekler; geçiş promptu kareleri
değil **aradaki hareketi** tarif eder.

---

## 2. Kling, Runway, Seedance, Pika, Luma

**Kling (2.1/3.0):** Resmî formül: özne + özne hareketi + mekân +
(kamera dili + ışık + atmosfer). 60-100 kelime ideal; ayrı negatif prompt
alanı vardır. Kling 3.0'da storyboard aracı ve dudak senkronlu ses geldi.

```text
Woman nods her head gently, maintains eye contact with camera, and
smiles warmly.
```

**Runway Gen-4/4.5:** Doktrin Veo'nun tersi: **basit başla, iterasyonla
ekle**. Image-to-video'da altın kural: görsel promptun parçasıdır;
görseldekini metinde TEKRAR TARİF ETMEYİN, yalnız neyin hareket edeceğini
ve kamerayı yazın.

```text
The camera slowly dollies in as she turns toward the window; her hair
moves in a light breeze.
```

**Pika (2.2+):** 1-3 cümlelik plan; Pikaframes (5 kareye kadar keyframe,
geçiş promptlu) ve hazır fizik efektleri (Melt, Explode, Squish...) ayırt
edici özellikleri.

```text
A premium black smartwatch on a clean pedestal, slow rotating product
reveal, studio lighting with soft reflections, shallow depth of field,
smooth dolly-in camera move.
```

**Seedance (ByteDance, 2.0):** Dreamina/CapCut ve API'ler (BytePlus, fal)
üzerinden erişilir; ayırt edici gücü **tek prompttan çok planlı anlatı**
kurması ve zaman çizelgeli prompt tekniğidir. Resmî formül: özne + eylem +
kamera + sahne/ışık + stil (50-150 kelime). Referanslar "@" ile anılır
(`@image1 as main character`, `@video1`'daki hareketi kopyala); gerçek
insan yüzü referansı politika gereği engellidir. Native ses (diyalog,
efekt, dudak senkronu) üretir. Seedance 2.5 duyuruldu ancak 2026-07
itibarıyla genel erişimde değildir.

```text
0-3s: extreme close-up on eyes widening; 3-7s: quick dolly out to medium
revealing rooftop standoff; 7-12s: orbiting arc around both characters.
```

```text
Use the stylized ronin from @image1 as protagonist, strictly preserve
facial structure, hair strands, clothing folds, accessory placement.
```

**Luma Dream Machine (Ray2/Ray3):** Sıra: özne → eylem → detay → mekân →
stil → kamera. Kamera anahtar kelimelerini en öngörülebilir uygulayan
modellerden. İlginç ayrıntı: "vibrant", "whimsical", "hyper-realistic"
gibi süslü sıfatlar Ray3'te sonucu bozabiliyor; somut tarif isteniyor.

```text
Medium shot of a coffee cup on a wooden table, steam rising from the
liquid, slow push-in camera movement, warm morning sunlight through a
window, cinematic look.
```

---

## 3. Avatar Video Platformları (HeyGen, Synthesia, Hedra)

Avatar platformlarında "prompt" iki parçaya ayrılır: **senaryo metni**
(avatarın söyleyeceği söz — TTS'e gider) ve **sahne/davranış talimatı**
(avatar seçimi, ton, jest, arka plan). Video modellerinden farkı: sahneyi
siz kurmazsınız, konuşmayı yönetirsiniz.

Senaryo metni kuralları:

- Konuşma dili yazın; yazı dili cümleleri seste robotik durur. Metni
  yüksek sesle okuyun — takıldığınız yerde avatar da takılır.
- Duraklamaları noktalama ile yönetin; vurgu için kısa cümle kullanın.
- Türkçe senaryolarda kısaltmaları açık yazın ("vb." değil "ve benzeri")
  — TTS kısaltmaları yanlış seslendirebilir.

**Senaryo + davranış talimatı örneği (eğitim videosu):**

```text
[Avatar: profesyonel, orta yaş, samimi gülümseme; ton: sıcak-öğretici;
tempo: orta; arka plan: sade ofis, hafif bulanık]

Merhaba! Bu kısa videoda, yapay zekâ araçlarına neden açık talimat
vermemiz gerektiğini göreceğiz. Bir örnekle başlayalım. ...
[duraklat] Şimdi aynı isteği bir de şöyle soralım. ...
```

**Fotoğraftan konuşan avatar (photo-to-avatar / Hedra, HeyGen Avatar IV
türü):** tek fotoğraf + ses/replik → konuşan video. Fotoğraf kuralları
görsel modlarla aynıdır: net, önden, iyi ışıklı yüz. Kimlik ve rıza
uyarısı geçerlidir — yalnız kendi fotoğrafınız veya yazılı izinli yüzler.
Son doğrulama: 2026-07.

---

## 4. OpenAI Sora 2 — Tarihî Not

Sora 2 (2025 sonu), "beat" tabanlı eylem yazımı (eylemi saniyelere bölerek
tarif etme), tek seferde tek değişken değiştiren remix yaklaşımı ve
"cameo" (doğrulanmış kendi görüntünü sahneye ekleme) özellikleriyle viral
oldu. **Sora uygulaması yayından kaldırılmaktadır** (uygulama 2026 başında
kapandı; API'nin de 2026 içinde sonlanması duyuruldu). Prompt teknikleri
— eylemi beat'lere bölmek, remix'te tek değişken değiştirmek — diğer
araçlarda da geçerliliğini korur. Son doğrulama: 2026-07.

---

## Sık Yapılan Hatalar

1. **Aşırı yüklü prompt:** ~175 kelimeyi aşınca model talimat düşürmeye
   başlar; plan başına tek niyet.
2. **Çelişen hareket:** "static shot" + "camera follows" bir arada olmaz;
   5 saniyeye sığmayacak eylem yazmak da aynı hata.
3. **Somut spesifikasyon yerine hava kelimeleri:** "cinematic, epic, high
   quality" az iş yapar; lens, ışık yönü ve renk paleti çok iş yapar.
4. **Image-to-video'da görseli yeniden tarif etmek:** hareketi öldürür.
5. **Klip süresine sığmayan diyalog:** 4-8 saniyeye 1-2 kısa replik;
   fazlası dudak senkronunu bozar.
6. **Sesi unutmak:** ses-native modellerde (Veo 3, Kling 3) en az bir
   `Ambient noise:` satırı yazın.
7. **Denemeler arasında çok değişken değiştirmek:** neyin işe yaradığını
   bilemezsiniz; tek seferde tek alan değiştirin.
8. **Olumsuzu düz cümleyle yazmak:** "no people" çoğu modelde görmezden
   gelinir; ayrı negatif prompt alanı varsa (Kling, Veo) onu kullanın.

JSON biçimli video promptları için bkz.
[08-json-yapilandirilmis-promptlar.md](08-json-yapilandirilmis-promptlar.md).

---

## Kaynaklar

- Google DeepMind Veo prompt guide: deepmind.google/models/veo/prompt-guide/
- Google Cloud — "Ultimate prompting guide for Veo 3.1":
  cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- OpenAI Cookbook — Sora 2 Prompting Guide:
  developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- Runway yardım merkezi — Gen-4 Video Prompting ve Image-to-Video
  rehberleri: help.runwayml.com
- Kling resmî prompt rehberi: kling.ai/blog/kling-ai-prompt-guide ve
  fal.ai Kling 3.0 rehberi: blog.fal.ai/kling-3-0-prompting-guide/
- Luma öğrenme merkezi: lumalabs.ai/learning-hub/
- Pika rehberleri: pikalabsai.org/pika-labs-prompting-guide/
- Seedance resmî prompt rehberleri (BytePlus ModelArk):
  docs.byteplus.com/en/docs/ModelArk/2222480 (2.0) ve fal.ai/seedance-2.0

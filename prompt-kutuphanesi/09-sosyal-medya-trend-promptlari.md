# Sosyal Medya Trend Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Trend Promptları"
concepts:
  - viral prompt kalıpları
  - kimlik tutarlılığı
  - filigran ve içerik kaynağı
last_verified: "2026-07"
```

Bu dosya 2025-2026'da sosyal medyada viral olan prompt kalıplarını,
dolaşımdaki halleriyle belgeler. İki amaçla: (1) çalışan kalıpları
kullanabilmeniz, (2) her kalıbın yanındaki hukuki/etik sınırı görmeniz.

> **Dört kesitsel uyarı (tüm trendler için):**
>
> 1. **Kimlik tutarlılığı:** Yüzün değişmemesi için standart ek cümle:
>    "Keep the facial features exactly the same so the person is clearly
>    recognizable."
> 2. **Filigran:** Google üretimleri görünmez SynthID taşır (ücretsiz
>    katmanda görünür logo da basılır); OpenAI video üretimleri görünür
>    filigran + meta veri taşırdı. Filigran silme araçları dolaşımda —
>    yani filigran YOKLUĞU "gerçek görüntü" kanıtı değildir.
> 3. **Telif/marka:** Stil taklidi (Ghibli) telifle korunmaz ama etik ve
>    itibar riski taşır; tescilli marka adları (Barbie, Pixar) prompta
>    yazıldığında reddedilebilir veya marka ihlali riski doğurur — markayı
>    adıyla değil tarifle isteyin.
> 4. **Kişilik hakları:** Gerçek bir kişiyle "birlikte çekilmiş gibi"
>    görsel üretmek, Türkiye'de KVKK ve TMK kişilik hakları kapsamında
>    sorun doğurabilir. Rızasız kullanmayın.

---

## 1. Koleksiyon Figürü ("1/7 scale figurine") — Nano Banana

Eylül 2025'te patlayan trend: fotoğrafını yükleyip masaüstünde duran
koleksiyon figürüne dönüştürme. Dolaşımdaki en yaygın sürüm:

```text
Create a 1/7 scale commercialized figurine of the characters in the
picture, in a realistic style, in a real environment. The figurine is
placed on a computer desk. The figurine has a round transparent acrylic
base, with no text on the base. The content on the computer screen is a
3D modeling process of this figurine. Next to the computer screen is a
toy packaging box, designed in a style reminiscent of high-quality
collectible figures, printed with original artwork.
```

**İpucu:** Net, iyi aydınlatılmış tek kişilik fotoğraf en iyi sonucu verir.

## 2. Aksiyon Figürü / Oyuncak Kutusu — ChatGPT (gpt-image)

Nisan 2025 dalgası. Doldurulabilir şablon halinde:

```text
A picture of a collectible action figure titled '[FIGURE NAME]' in a
sealed plastic blister pack on a cardboard backing. The figure is posed
confidently inside the transparent plastic shell, surrounded by three
accessories that reflect their personality or career. The character is
wearing [OUTFIT] and has a [EXPRESSION] expression. The packaging features
a [COLOR SCHEME] background with bold letters at the top displaying the
name '[FIGURE NAME]' and the subtitle 'ACTION FIGURE' beneath it. The
visual style is playful, minimal and toy-like, with smooth surfaces and
soft lighting that mimics the look of real plastic.
```

**Uyarı:** "Barbie" yerine "action figure/doll" deyin (tescilli marka).

## 3. Ghibli Tarzı Dönüştürme — ChatGPT

Mart 2025'in rekor trendi ("GPU'larımız eriyor" dönemi):

```text
Transform this photo into a Studio Ghibli-style portrait. Use soft
watercolor textures, warm golden-hour lighting, expressive eyes, and a
peaceful countryside background.
```

**Uyarı:** Trendin kendisi telif tartışmasıyla anılır (Miyazaki'nin AI
tepkisi + açılan davalar). Yaşayan bireysel sanatçı stili istekleri
reddedilebilir; "stüdyo stili" genelde geçer. Kurumsal işte kullanmayın.

## 4. Profesyonel LinkedIn Vesikalığı — Nano Banana / ChatGPT

```text
Transform this image into a professional LinkedIn headshot. Ensure the
person is looking directly at the camera with a confident yet
approachable expression. Replace their outfit with a tailored navy-blue
suit over a crisp white shirt. Blurred modern office background with
natural light, depth of field. Keep my face exactly the same, do not
alter facial features.
```

**İpucu:** Aşırı rötuş "AI vesikalığı" olarak fark edilir; doğal cilt
dokusu bırakmak daha inandırıcıdır. Bazı işverenler gerçeği yansıtmayan
fotoğrafı sorunlu bulur — makul sınırda kalın.

## 5. Cam Meyve ASMR — Veo 3

Veo'nun native sesini vitrine çıkaran format; ses tarifi promptun kalbidir:

```text
A hyper-detailed glass strawberry resting on a wooden cutting board under
warm soft lighting, with cinematic depth of field. A stainless steel
knife gently slices through the glass fruit, creating clean, slow-motion
cuts, and crisp, satisfying glass-shattering sounds. No background music.
```

Malzeme değiştirilerek seri üretilir: glass mango, crystal kiwi, lava cake.

## 6. Sokak Röportajı Formatı — Veo 3

Mekân + kamera stili + ortam sesi + iki karakter + tırnak içinde diyalog
formülü; tırnaklı diyalog dudak senkronunu tetikler:

```text
TikTok-style street interview video, night in Times Square, bright
flashing billboards, reflective pavement. Handheld camera with slight
motion shake. Audio: distant horns, footsteps, crowd chatter. A confident
woman in her late 20s in a red dress holds a microphone and stops a man
in layered streetwear. She asks: "[SORU]" He pauses, looks at the camera,
and answers: "[CEVAP]"
```

## 7. Bigfoot Vlog / Tutarlı Karakter Serisi — ChatGPT + Veo 3

İki aşamalı iş akışı; seri içeriğin temel tekniğini öğretir
(**çapa prompt / anchor prompt**):

1. Metin modeline karakter çapası yazdırın:

```text
Create a hyper-detailed, hyper-realistic Australian Bigfoot character.
He should be loud, over-the-top, and comically wise. Vlog-style tone.
Include physical description, attitude, and mannerisms.
```

2. Bu tanımı **her video üretiminin başına kelimesi kelimesine** yapıştırıp
   sahneyi ekleyin:

```text
[ÇAPA KARAKTER TANIMI]. Selfie-style vlog footage, he holds the camera at
arm's length, walking through a misty pine forest at dawn. Slight camera
shake, fisheye distortion. He whispers to the camera: "Day 47. The humans
still haven't found me." Ambient forest sounds, birdsong, heavy footsteps.
```

Çapa promptun aynen tekrarı, klipler arası karakter tutarlılığının en
güvenilir yoludur.

## 8. 90'lar Yıllık Fotoğrafı / Nostalji Kalıpları

```text
Turn this photo into a 1990s high-school yearbook portrait. Keep the
exact face. Wardrobe: collared shirt or simple sweater, period haircut.
Classic mottled blue-grey laser backdrop, soft studio key light with a
hair light, gentle soft-focus, slightly faded print color and fine
halftone texture from cheap printing.
```

Aynı ailenin diğer üyeleri: "Hug my younger self" (bugünkü + çocukluk
fotoğrafı birlikte yüklenir, "keep both faces exactly as they are"),
vintage polaroid, retro film estetiği.

## 9. 2026'nın Dikkat Çeken Akımı: Anti-AI Estetiği

Aşırı pürüzsüz "AI görünümünden" kaçış — kusuru bilinçli isteme:

```text
Take this crisp photo and age it like a forgotten 1990s Polaroid. Add
heavy film grain, a slight blur around the edges, and a faint yellow
light leak coming from the bottom right corner.
```

## 10. Tarihî Not: Sora "Cameo" Dalgası

Sora 2 uygulamasının cameo özelliği (doğrulanmış kendi görüntünü herhangi
bir sahneye ekleme, izin katmanlarıyla) 2025 sonunda App Store 1 numaraya
çıktı. **Uygulama yayından kaldırılmıştır** (2026); kalıcı dersleri:
(1) benzerlik/likeness izni kullanıcı kontrolünde olmalı, (2) filigran tek
başına güven zinciri kurmaz — lansmandan bir hafta sonra filigran silme
araçları yayılmıştı. Son doğrulama: 2026-07.

---

## Kaynaklar

Trend promptları sosyal medyada dolaşan halleriyle derlenmiştir; doğrulama
kaynakları: demandsage.com ve banananano.ai (figürin), CNN/Newsweek (Ghibli
trendi haberleri), nanobanana.im ve analyticsvidhya.com (LinkedIn
vesikalık), photogrid.app ve geeky-gadgets.com (ASMR), filmora.wondershare
ve PromptBase (sokak röportajı), filmit.io (Bigfoot vlog iş akışı),
iprompti.com (yıllık fotoğrafı), eweek.com 2026 trend derlemesi (anti-AI
estetiği, roast/chibi kalıpları), superprompt.com ve NewsGuard (Sora cameo
ve filigran analizi). Prompt metinleri topluluk kaynaklı olduğundan tek
tek lisanslanmaz; kalıp olarak kullanın, birebir ticari içerikte üstteki
dört uyarıyı uygulayın.

# Müzik ve Ses Üretimi Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Müzik ve Ses"
concepts:
  - stil promptu ve metatag
  - şarkı düzenleme iş akışları
  - ses klonlama etiği
last_verified: "2026-07"
```

> **Sürüm uyarısı:** Bilgiler 2026-07'de doğrulanmıştır. Müzik üretiminde
> güncel Suno modeli v5.5'tir (ücretsiz katman v4.5 ile sınırlı); Udio,
> lisans anlaşması sonrası dışa aktarım kapalı bir platforma dönüştüğünden
> artık Suno'nun birebir alternatifi değildir. Alternatifler: Eleven Music
> (YouTube para kazanımı için lisanslı), Mureka (ücretsiz planda dahi
> ticari kullanım), Riffusion (enstrümantal/elektronik).

---

## 1. Suno: Stil Kutusu ve Söz Kutusu Ayrımı

Suno'nun özel modunda iki ayrı alan vardır ve ikisinin işi farklıdır:

- **Stil alanı** (~1.000 karakter): tür + ruh hali + tempo + enstrümanlar +
  vokal tipi + prodüksiyon stili. İdeal yoğunluk **4-7 tanımlayıcı**; 10+
  tanımlayıcı bulanık sonuç verir.
- **Söz alanı** (~5.000 karakter): şarkı sözü + köşeli parantezli
  **metatag'ler**. Metatag yoksa yapıyı Suno tahmin eder; varsa aranjmanı
  siz yönetirsiniz.

**Stil promptu örneği:**

```text
Indie folk rock, mid-tempo, acoustic guitar and mandolin, warm female
vocals, lo-fi production, nostalgic and wistful
```

**Türkçe stil promptu örnekleri:**

```text
Turkish arabesque, emotional male vocals in Turkish, dramatic, string
section, melancholic, passionate, sweeping orchestral arrangement
```

```text
Anatolian rock, electric guitar, bağlama saz, psychedelic, male vocals
in Turkish, 70s rock fusion, Turkish folk melody, groovy
```

**Enstrümantal örneği** (Instrumental anahtarı açık):

```text
Lo-fi hip-hop beat, jazzy piano chords, vinyl crackle, mellow drums,
study music
```

---

## 2. Metatag'li Söz Şablonu

```text
[Intro: sparse, atmospheric]
[Verse 1]
(birinci kıta sözleri)
[Chorus]
(nakarat)
[Verse 2]
(ikinci kıta)
[Chorus]
(nakarat)
[Bridge: stripped down, different energy]
(kontrast bölümü)
[Guitar Solo]
[Chorus]
(nakarat)
[Outro: fade out]
[End]
```

Kurallar ve incelikler:

- Yapısal tag'ler: `[Intro] [Verse] [Pre-Chorus] [Chorus] [Bridge] [Outro] [End]`;
  enstrümantal: `[Instrumental Break] [Guitar Solo] [Piano Solo]`;
  vokal: `[Male Vocal] [Female Vocal] [Choir] [Rap] [Whisper]`.
- v5+ iki nokta üst üste ile parametreli tag anlar:
  `[Verse: whispered vocals, acoustic guitar only]`.
- Kıtaları numaralamak (`Verse 1`, `Verse 2`) farklı melodi sinyali verir;
  nakarat metnini birebir tekrar etmek melodik tekrarı teşvik eder.
- **Olumsuzlamayı stil alanına yazmayın** ("no drums" güvenilir çalışmaz);
  Gelişmiş Seçenekler'deki **Exclude Styles** alanını kullanın.

**Türkçe söz notları:** Sözleri Türkçe karakterlerle (ş, ç, ğ, ı, ö, ü)
yazın; stil alanına "singing in Turkish" ekleyin; enstrümanları adıyla
belirtin (bağlama, davul, zurna). Makam hassasiyeti kusurludur; "Turkish
makam, modal" ifadesi tonaliteyi yaklaştırır. Karışık dilli bölümleri net
ayırmazsanız telaffuz bozulur.

---

## 3. Düzenleme İş Akışları (Şarkıyı Değiştirme)

| İşlem | Ne yapar | Kullanım |
|---|---|---|
| **Extend** | şarkıyı belirtilen noktadan devam ettirir | kısa çıkan şarkıya yeni bölüm |
| **Replace Section** | seçilen zaman aralığını yeniden üretir | hatalı kelime/kıta onarımı |
| **Cover** | aynı söz ve melodiyi yeni stilde yorumlar | balad → rock, tarz denemeleri |
| **Remaster** | eski üretimi yeni modelle tazeler | v4 dönemi şarkıyı v5 kalitesine taşıma |
| **Stems** | 2-12 ayrı enstrüman/vokal izi verir | DAW'da miksleme, remix |
| **Kendi sesini yükleme** | kayıt üzerine vokal/enstrümantal ekler | kendi melodinizi tam aranjmana çevirme |

**Cover talimatı örneği** (şarkı → Create → Cover, yeni stil alanı):

```text
acoustic ballad, fingerpicked nylon guitar, intimate male vocals,
slow tempo, stripped-down, candlelit atmosphere
```

**Extend devam şablonu** (söz kutusuna):

```text
[Bridge: half-time, whispered vocals]
(yeni bölüm sözleri)
[Final Chorus: full band, key change up]
(nakarat tekrar)
[Outro: instrumental fade]
```

**Süreklilik:** Personas (v5 öncesi) ve Voices/Custom Models (v5.5) bir
şarkının vokal kimliğini sonraki şarkılara taşır. Persona/klon ses
kullanırken stil alanından cinsiyet tanımlayıcılarını çıkarın (çelişir).

---

## 4. ElevenLabs: Konuşma, Ses Tasarımı, Efekt ve Ötesi

2026 ortasında ElevenLabs üç ürün şemsiyesine ayrıldı: **ElevenCreative**
(stüdyo/yaratıcı araçlar), **ElevenAgents** (sesli ajan platformu) ve
**ElevenAPI**. Amiral gemisi konuşma modeli **Eleven v3**'tür (70+ dil,
Türkçe dahil); düşük gecikme için Flash v2.5, klasik iş yükleri için
Multilingual v2 sürer. Son doğrulama: 2026-07 — elevenlabs.io/docs.

**a) Konuşma (TTS, v3) — köşeli parantezli ses etiketleri.** Etiketler
İngilizce yazılır, metin Türkçe olabilir:

```text
[curious] Peki bu yöntem gerçekten işe yarıyor mu? [pause]
[excited] Sonuçlar geldi... ve HARIKA görünüyor! [laughs]
[whispers] Ama kimseye söylemeyin, henüz üretimde test etmedik.
```

Resmî etiket dağarcığından örnekler — duygu/ses: `[laughs] [whispers]
[sighs] [exhales] [sarcastic] [curious] [excited] [crying]
[mischievously]`; efekt: `[applause] [explosion] [gunshot]`; deneysel:
`[strong French accent] [sings]`. Liste açık uçludur; etiketin işlemesi
seçilen sese bağlıdır (sakin bir ses `[shouting]`'ı iyi oynamaz). Kurallar:

- 250 karakterden uzun metinler daha tutarlı sonuç verir; üç nokta
  duraklama, BÜYÜK HARF vurgu üretir.
- v3'te stability üç kiptir: **Creative** (en duygusal, halüsinasyona
  açık), **Natural** (dengeli), **Robust** (çok kararlı ama etiketlere
  duyarsız). Etiket kullanacaksanız Creative/Natural seçin.
- `<break time="1.5s" />` SSML duraklaması yalnız v2 ailesindedir; v3
  desteklemez (v3'te eğik çizgi içinde IPA telaffuz verilebilir).
- Sayı, tarih ve kısaltmaları okunuşuyla açık yazın ("14:30" değil
  "on dört otuz"); API'de sunucu taraflı normalizasyon da açılabilir.

**Çok konuşmacılı diyalog (Text to Dialogue, v3):** her konuşmacı ayrı
satırda, etiketler satır içinde:

```text
Speaker 1: [excitedly] Yeni sürümü denedin mi?
Speaker 2: [curiously] Az önce kurdum. Netlik inanılmaz — [whispers]
artık fısıldayabiliyorum bile.
```

**b) Ses tasarımı (Voice Design) — metinden yeni ses.** Resmî tarif kalıbı:
dil + cinsiyet + yaş aralığı + kayıt kalitesi + persona + duygu + tını/tempo:

```text
Native Turkish. Female, mid-30s. Perfect audio quality.
Persona: corporate e-learning narrator. Emotion: warm, confident, calm.
Clear diction, moderate pace, a slight smile in the voice.
```

Guidance Scale yüksek = tarife sıkı bağlılık (aksan isabeti), düşük =
daha doğal ses; önizleme metni tarif edilen personayla uyumlu olmalıdır.

**c) Ses klonlama.** İki yol: **Instant Voice Clone** (kısa örnekten,
eğitimsiz) ve **Professional Voice Clone** (özel model eğitimi, 3-6 saat;
temiz oda + iyi mikrofon ister — "model sesinizle ilgili her şeyi
klonlamaya çalışır"). PVC rıza doğrulaması ister: konuşmacı ekrandaki
metni sesli okuyarak sesin sahibi olduğunu kanıtlar. PVC henüz v3 için
tam optimize değildir; v3 projelerinde IVC veya tasarlanmış ses önerilir.

**d) Ses efekti (SFX).** 0,1-30 saniye; döngü (loop) seçeneği ve "prompt
influence" kaydırıcısı (yüksek = birebir, düşük = yaratıcı) vardır. Tek
vuruşlar için kısa somut tarif, olay dizileri için sıralı tarif:

```text
Glass shattering on concrete
```

```text
Heavy wooden door creaking open slowly in a large echoing hall,
followed by two slow footsteps on stone.
```

```text
Cinematic braam, deep brassy hit with long reverb tail, trailer style
```

**e) Eleven Music (v2).** Etiketlerle/yayıncılarla anlaşmalı — çıktılar
film, TV, podcast, reklam ve oyun dahil ticari kullanım için
temizlenmiştir (plan koşulları: elevenlabs.io/music-terms). Bölüm bazlı
yeniden üretim (inpainting) ve parça ortasında tür değişimi destekler.
Kısa, çağrışımlı promptlar çoğu zaman uzun teknik tariflerden iyi çalışır;
ton/BPM/enstrüman/vokal ve zamanlama ("lyrics begin at 15 seconds")
verilebilir:

```text
Dark synthwave, 110 BPM in A minor, analog synth arpeggios, driving
bass, retro drums, instrumental only, builds to an intense final
chorus. 90 seconds.
```

Türkçe şarkı sözü desteği resmî listede doğrulanmamıştır; yayın öncesi
deneyin.

**f) Dublaj.** Otomatik dublaj (tek tık, 90+ dil, duygu/zamanlama korunur)
veya Dubbing Studio (transkript/çeviri düzenleme, konuşmacı atama, klip
bazlı yeniden üretim). Prompt değil iş akışıdır; kaynak videonun temiz
sesi sonucu prompttan çok belirler. Ücretsiz katman çıktısı filigranlıdır.

**g) Sesli ajanlar (ElevenAgents).** Sesli ajan sistem promptunun resmî
iskeleti altı bloktur: `# Personality`, `# Environment`, `# Tone`,
`# Goal`, `# Guardrails`, `# Tools`. Sesli yanıtlar 2-3 cümlede tutulur;
2.000 token'ı aşan promptlar uzman ajanlara bölünür.

**h) 2026'nın diğer yüzeyleri (tek satırlık envanter):** Scribe v2
(konuşmadan metne, 90+ dil, gerçek zamanlı ~150 ms), Voice Changer
(kayıtlı sesi başka sesle yeniden seslendirme), Voice Isolator (gürültülü
kayıttan temiz konuşma), Image & Video (üçüncü taraf modellerle görsel/
video + dudak senkronu), Avatars (konuşan kafa videoları), Ads Engine.
Bunların çoğu prompt değil iş akışı araçlarıdır.

---

## 5. Konuşma Sesi: Genel TTS ve Ses Klonlama

Metinden ses (text-to-speech) promptlarında üç bileşen belirtin: **kim**
(ses karakteri: yaş, cinsiyet, enerji), **nasıl** (ton: sakin/coşkulu,
tempo, duraklar) ve **ne için** (belgesel anlatımı / reklam / eğitim
videosu — kullanım bağlamı tonlamayı ayarlar). Uzun metinlerde noktalama
tonlamayı yönetir; vurgu istediğiniz kelimeyi BÜYÜK yazmak çoğu araçta
işe yarar.

```text
Warm, mid-30s Turkish female voice, calm and confident, moderate pace
with natural pauses. Style: corporate training narration. Read the
following script in Turkish: [metin]
```

**Ses klonlama etiği:** Yalnız kendi sesinizi veya yazılı izni olan bir
sesi klonlayın. Türkiye'de başkasının sesi kişisel veridir (KVKK) ve
kişilik hakları kapsamındadır; ünlü taklidi içerik hem platform kurallarına
hem hukuka takılır. Suno'nun Voices özelliği bu yüzden sözlü doğrulama
ister ve klonu yükleyene özel tutar.

---

## 6. Telif ve Ticari Kullanım (Suno, 2026-07)

- **Ücretsiz katman:** ticari kullanım YOK; çıktının sahibi Suno;
  sonradan abone olmak geçmiş üretimlere ticari hak kazandırmaz.
- **Pro/Premier:** abonelikte üretilen şarkılar sizindir; abonelik
  bitince ticari haklar devam eder.
- **Sanatçı adı yazmayın:** "Tarkan gibi" tarzı istekler engellenir;
  stili tarif edin: "90s Turkish pop, energetic male vocals,
  Latin-influenced rhythm".
- Büyük plak şirketleriyle lisans anlaşmaları sonrası kurallar hızla
  değişiyor; yayınlamadan önce güncel koşulları suno.com üzerinden
  doğrulayın. Dağıtım platformlarının (Spotify vb.) AI beyan şartları
  ayrıca kontrol edilmelidir.

---

## Kaynaklar

- Suno resmî sürüm notları ve v5.5 duyurusu: suno.com/release-notes,
  suno.com/blog/v5-5; yardım merkezi: help.suno.com
- Suno prompt rehberleri: blakecrosley.com/guides/suno,
  openmusicprompt.com (metatag rehberi), hookgenius.app (v5.5 ve Türkçe
  prompt rehberleri)
- Lisans analizleri: dynamoi.com (Suno ticari haklar),
  musicbusinessworldwide.com ve billboard.com (Suno/Udio lisans
  anlaşmaları)
- Udio'nun platform değişikliği: billboard.com — UMG-Udio anlaşması
  haberleri
- ElevenLabs resmî dokümantasyonu (ses etiketleri, voice design, SFX,
  Eleven Music): elevenlabs.io/docs

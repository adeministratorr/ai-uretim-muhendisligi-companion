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

## 4. ElevenLabs: Konuşma, Ses Tasarımı ve Efekt

ElevenLabs üç ayrı üretim yüzeyi sunar ve promptlama her birinde farklıdır
(Son doğrulama: 2026-07 — etiket seti modele göre değişir, güncel
dokümandan kontrol edin: elevenlabs.io/docs).

**a) Konuşma (TTS) — köşeli parantezli ses etiketleri.** Güncel konuşma
modelleri, metnin İÇİNE yazılan duygu/eylem etiketlerini yorumlar:

```text
[warmly] Hoş geldiniz! Bu eğitimde üç adımı birlikte geçeceğiz.
[pause] İlk adım en önemlisi... [whispers] ve çoğu kişi bunu atlıyor.
[laughs] Merak etmeyin, biz atlamayacağız.
```

Yaygın etiketler: `[whispers] [laughs] [sighs] [excited] [sad] [angry]
[pause] [curious] [sarcastic]`. Kurallar:

- Etiketi cümlenin başına, etkilemesini istediğiniz yere koyun; aşırı
  etiket doğallığı bozar (paragraf başına 1-3 yeterli).
- Vurgu için BÜYÜK HARF, doğal duraklama için üç nokta işe yarar.
- Sayı, tarih ve kısaltmaları Türkçe okunuşuyla açık yazın ("1923'te"
  yerine "bin dokuz yüz yirmi üçte") — TTS normalizasyonu dile göre
  değişkendir.
- Ses ayarları (stability/similarity) prompt değil parametredir: düşük
  stability daha duygusal/değişken, yüksek stability daha tekdüze-tutarlı
  okuma verir.

**b) Ses tasarımı (Voice Design) — metinden yeni ses.** Var olmayan bir
sesi tarifle üretirsiniz; tarif yaş + cinsiyet + aksan/dil + ton + tempo +
kullanım bağlamı içermelidir:

```text
A warm, confident Turkish female voice in her mid-30s. Clear diction,
moderate pace, friendly but professional — suitable for corporate
e-learning narration. Slight smile in the voice.
```

**c) Ses efekti (SFX) üretimi.** Kısa, somut, fizik tarifli yazın:

```text
Heavy wooden door creaking open slowly in a large echoing hall,
followed by two slow footsteps on stone.
```

**d) Eleven Music.** Lisanslı müzik üretimi (YouTube para kazanımı için
temizlenmiş ilk büyük üreticilerden). Stil promptu Suno mantığıyla aynıdır:
tür + ruh hali + enstrümantasyon + tempo + vokal; sözlü/sözsüz seçimi
belirtin.

**Dublaj/çeviri notu:** ElevenLabs dublajı (bir videoyu başka dile aynı
ses karakteriyle çevirme) prompt değil iş akışıdır; kaynak videonun temiz
sesi, sonucun kalitesini prompttan çok belirler.

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

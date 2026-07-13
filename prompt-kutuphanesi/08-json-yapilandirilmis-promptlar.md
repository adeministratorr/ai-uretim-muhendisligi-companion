# JSON ve Yapılandırılmış Promptlar

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Yapılandırılmış Promptlar"
concepts:
  - structured output
  - talimat-veri ayrımı
  - prompt-as-config
last_verified: "2026-07"
```

"JSON prompt" 2025-2026'nın en çok konuşulan tekniklerinden. Bu dosya
tekniği üç kullanım alanında ele alır — metin görevleri, görsel üretim,
video üretim — ve en az teknik kadar önemli olan soruyu yanıtlar:
**yapı ne zaman işe yarar, ne zaman yüktür?**

---

## Yapı Ne Zaman İşe Yarar?

1. **Talimat-veri ayrımı.** Prompt hem talimat hem işlenecek metin
   içeriyorsa sınırlayıcılar (XML etiketi, kod bloğu) modelin veriyi
   talimat sanmasını engeller. Bu aynı zamanda prompt injection'a karşı
   ilk savunma hattıdır.
2. **Makinece okunacak çıktı.** Çıktı bir programa, tabloya veya başka bir
   prompta girecekse şema zorunludur; serbest metin güvenilir parse edilemez.
3. **Toplu işleme.** Aynı işlem 100 kayda uygulanacaksa numaralı/etiketli
   yapı, eşleştirme hatasını bitirir.
4. **Prompt-as-config.** Sabit şablon + değişken alanlar = sürümlenebilir,
   test edilebilir, ekipçe paylaşılabilir prompt.

**Ne zaman gerekmez:** tek seferlik sohbet, yaratıcı yazı, açık uçlu analiz.
Katı şema modelin düşünme alanını daraltabilir; bu yüzden karmaşık
çıkarımlarda şemaya bir `reasoning` alanı eklemek yaygın pratiktir.

---

## 1. Metin Görevlerinde Yapı

### JSON görev brifi (girdi tarafında yapı)

Serbest paragraf yerine görevi konfigürasyon gibi verin:

```json
{
  "gorev": "blog_yazisi_ozeti",
  "girdi_dili": "İngilizce",
  "cikti_dili": "Türkçe",
  "uzunluk": "en fazla 150 kelime",
  "hedef_kitle": "teknik olmayan yöneticiler",
  "yasakli": ["pazarlama dili", "birinci tekil şahıs"],
  "cikti_bicimi": "3 madde + 1 cümlelik sonuç"
}
```

Altına `Metin:` başlığıyla işlenecek içerik eklenir. Fayda: her alan tek
tek denetlenebilir; aynı brif farklı metinlerle yeniden kullanılır.

### Şema dayatmalı çıkarım (çıktı tarafında yapı)

"Yalnızca şu şemaya uyan JSON döndür" talimatı tek başına yeterince
güvenilir değildir; API düzeyinde şema zorlaması kullanın:

- **OpenAI**: Structured Outputs (`json_schema` + `strict: true`) — eski
  "JSON mode" yalnız geçerli JSON garantiler, şemaya uyum garantilemez.
- **Anthropic (Claude)**: Structured Outputs — şema bir gramere derlenir,
  model şemayı bozan token'ı üretemez (constrained decoding). Pydantic/Zod
  ile şema tanımı desteklenir.

Örnek şema (müşteri e-postasından şikâyet kaydı çıkarımı):

```json
{
  "name": "sikayet_kaydi",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "musteri_adi": { "type": ["string", "null"] },
      "urun": { "type": "string" },
      "sikayet_kategorisi": { "type": "string",
        "enum": ["kargo", "iade", "arıza", "fatura", "diğer"] },
      "aciliyet": { "type": "string", "enum": ["düşük", "orta", "yüksek"] },
      "ozet": { "type": "string", "description": "Tek cümle, Türkçe" }
    },
    "required": ["musteri_adi", "urun", "sikayet_kategorisi", "aciliyet", "ozet"],
    "additionalProperties": false
  }
}
```

İki incelik: `enum` değer uydurmayı keser; bilinmeyen değer için `null`'a
izin vermek, "bulamadıysan uydurma" kuralının şema karşılığıdır. Çalışan
örnekler için bkz. `../cilt-1-prompting/structured-outputs/`.

### Değişkenli şablon (prompt-as-config)

Anthropic'in `{{DEĞİŞKEN}}` + XML kalıbı:

```xml
Sen {{SIRKET_ADI}} için çalışan bir müşteri destek asistanısın.

<kurallar>
- Yalnızca <bilgi_bankasi> içindeki bilgiye dayan.
- Emin olmadığında "Bu konuda kayıtlı bilgim yok" de.
- Yanıtı en fazla {{MAKS_CUMLE}} cümlede ver.
</kurallar>

<bilgi_bankasi>
{{BILGI_BANKASI}}
</bilgi_bankasi>

<musteri_sorusu>
{{SORU}}
</musteri_sorusu>
```

Şablon sabit kalır, yalnız `{{...}}` alanları değişir: sürüm kontrolüne
girer, A/B testi yapılabilir. prompts.chat koleksiyonu benzer amaçla
`${degisken:varsayilan}` sözdizimi kullanır.

---

## 2. Görselde JSON Prompt

Alanlara ayırmak **kavram sızmasını** (concept bleeding — arka plan renginin
kıyafete bulaşması gibi) azaltır ve tek alan değiştirerek varyant üretmeyi
sağlar. Marka işleri ve seri üretimde değerlidir.

**Çalıştığı yerler:** Nano Banana Pro / Gemini 3 görsel ailesi (en güçlü
uyum), gpt-image-1.5/2 (Cookbook resmen destekler), FLUX.2 (resmî destek;
bölgesel prompt, referans ağırlığı, HEX renk dahil).

**Çalışmadığı yerler:** Midjourney (süslü parantezler düz metin olarak
okunur, token israfı — kontrol `--parametre`lerdedir), FLUX.1 ve Stable
Diffusion soyu (kodlayıcılar doğal cümle bekler). Basit tek özneli işlerde
de gereksiz yüktür.

**Ürün fotoğrafı şablonu:**

```json
{
  "subject": "matte black ceramic coffee mug with the word 'KAVRUK' embossed on the side",
  "environment": "polished walnut table, blurred cafe interior behind",
  "lighting": "soft window light from the left, gentle rim light on the mug's edge",
  "camera": { "lens": "85mm", "aperture": "f/2.8", "angle": "eye-level, slightly off-center" },
  "composition": "rule of thirds, mug on right third, negative space on left for ad copy",
  "color_palette": ["matte black", "warm walnut brown", "cream"],
  "style": "premium commercial product photography",
  "mood": "calm, artisanal",
  "restrictions": "no people, no text overlays except the embossed brand name"
}
```

**Metin işlemeli slayt/kapak şablonu (gpt-image-2 / Nano Banana Pro):**

```json
{
  "format": "16:9 presentation slide",
  "title_text": "YAPAY ZEKÂ İLE GÖRSEL ÜRETİM",
  "typography": "bold geometric sans-serif, white title top-left",
  "subject": "isometric illustration of a robot hand painting on a canvas",
  "layout": "title top-left, illustration right half, three small icon captions bottom-left reading 'PROMPT', 'MODEL', 'GÖRSEL'",
  "color_palette": ["deep navy background", "amber accents", "white text"],
  "style": "flat corporate illustration, subtle grain",
  "restrictions": "no photorealism, no watermark, Turkish characters must render correctly (ÂZÜĞİŞÇÖ)"
}
```

---

## 3. Videoda JSON Prompt

Veo 3 ile viral olan format. Önemli dürüstlük notu: **JSON, Veo'nun resmî
girdi biçimi değildir** — Google'ın kendi rehberleri düz cümle kullanır ve
modelin eğitildiği gizli bir şema yoktur. Bağımsız karşılaştırmalar
(VP Land A/B testi) JSON'un yapı disiplini sağladığını ama tek başına
kalite artışı garantilemediğini buldu. Kazanç modelde değil insandadır:

1. **Boş alan bırakmaz** — `lighting` alanı görünce doldurursunuz.
2. **Cerrahi iterasyon** — yalnız `camera.movement` değiştirip yeniden
   üretirsiniz; düz metinde küçük değişiklik bile ağırlıkları öngörülemez
   biçimde kaydırır.
3. **Şablonlaşma** — aynı şemada yalnız `subject`/`dialogue` değişerek
   tutarlı seri içerik üretilir.

Her iki biçimde de sınır aynıdır: ~175 kelimeyi aşan prompt talimat
düşürmeye başlar.

**Tam üretim şeması (Veo 3.1):**

```json
{
  "shot": {
    "type": "Medium shot",
    "lens": "35mm, shallow depth of field",
    "framing": "Subject centered, full upper body in frame",
    "movement": "Slow dolly-in"
  },
  "subject": "A woman in her 30s, short dark hair, olive trench coat",
  "action": "She turns a page of an old journal and pauses at a photograph",
  "scene": "A dim study lined with bookshelves, rain streaking the window",
  "lighting": "Warm desk lamp as key light, cool blue window light as fill",
  "style": "Photorealistic, cinematic tone, muted color grade",
  "audio": {
    "dialogue": "She whispers: 'I remember this day.'",
    "sfx": "SFX: paper rustling, rain tapping on glass",
    "ambient": "Ambient noise: low room tone, distant thunder"
  },
  "color_palette": "Amber and slate blue",
  "negative_prompt": "text overlays, extra people in the background",
  "technical": { "aspect_ratio": "16:9", "duration": "8 seconds" }
}
```

**Zaman çizelgeli ürün videosu şablonu:**

```json
{
  "scene": "A premium wireless headphone on a matte black surface in a dark studio",
  "timeline": [
    { "time": "0-3s", "action": "Headphone sits in soft silhouette. Camera holds steady, building anticipation." },
    { "time": "3-6s", "action": "A slow side-light sweep reveals form and texture as the camera gently pushes in." },
    { "time": "6-8s", "action": "Headphone lands fully in focus in a clean close-up. Camera settles on the final frame." }
  ],
  "audio": {
    "sfx": "SFX: a single low bass hit at the reveal",
    "ambient": "Ambient noise: subtle synth pad"
  }
}
```

---

## Kaynaklar

- OpenAI — Structured Outputs rehberi:
  platform.openai.com/docs/guides/structured-outputs
- Anthropic — XML etiketleri ve structured outputs dokümanları:
  platform.claude.com/docs (prompt engineering / structured outputs)
- OpenAI Cookbook — görsel modellerde prompt biçimleri:
  developers.openai.com/cookbook
- Black Forest Labs — FLUX.2 JSON prompt dokümanı:
  docs.bfl.ml/guides/prompting_guide_flux2
- Atlabs — Nano Banana Pro JSON prompting guide: atlabs.ai/blog
- imagine.art — Veo 3 JSON prompting guide (JSON'un resmî format olmadığı
  uyarısı dahil): imagine.art/blogs/veo-3-json-prompting-guide
- VP Land — "We Tested JSON Prompting in Veo 3" A/B testi: vp-land.com

Son doğrulama: 2026-07. Bloglarda dolaşan "JSON %92'ye karşı %68 isabet"
türü rakamlar bağımsız doğrulanmamıştır; bu dosya bilinçli olarak
aktarmamaktadır.

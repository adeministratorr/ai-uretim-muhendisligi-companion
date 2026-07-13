# Görsel Üretim Promptları

```yaml
volume: 1
book_section: "Prompt Kütüphanesi — Görsel Üretim"
concepts:
  - görsel prompt anatomisi
  - stil ve karakter tutarlılığı
  - negatif prompt
last_verified: "2026-07"
```

> **Sürüm uyarısı:** Görsel modellerin adları ve parametreleri metin
> modellerinden daha hızlı değişir. Bu dosyadaki bilgiler 2026-07'de resmî
> dokümanlardan doğrulanmıştır; kullanmadan önce aracınızın güncel sürüm
> notlarına bakın. Prompt metinleri İngilizce verilmiştir: görsel modeller
> ağırlıklı olarak İngilizce açıklamalarla eğitildiğinden Türkçe promptlarda
> isabet düşer. Görselin İÇİNDE görünecek metin elbette Türkçe yazılabilir.

---

## Üretim Modları Haritası

| Mod | Girdi → Çıktı | Prompt neyi tarif eder |
|---|---|---|
| Text-to-image | metin → görsel | sahnenin tamamını (aşağıdaki anatomi) |
| Image-to-image / talimatla düzenleme | görsel + metin → görsel | YALNIZ değişecek şeyi + korunacakları |
| Referanslı üretim | referans görsel(ler) + metin → görsel | yeni sahneyi; kimlik/stil referanstan gelir |
| Görsel → metin (analiz) | görsel → metin | modele sorulacak soruyu (bkz. kitap Bölüm 9.2-9.6) |

Image-to-image altın kuralı: "change only X, keep everything else the
same" kalıbı + korunacakların açık listesi (örnekleri Nano Banana ve
gpt-image bölümlerinde). Referanslı üretimde kimlik `--oref`/isimli
karakter/referans görselden gelir; prompt yalnız yeni sahneyi kurar.

---

## Ortak Prompt Anatomisi

Araç fark etmeksizin iyi bir görsel prompt şu bileşenleri kapsar:

**Özne → ortam/mecra (fotoğraf, yağlı boya, 3B render, düz vektör) →
stil → ışık → kamera/lens → kompozisyon → atmosfer/renk paleti**

İlke: "stok fotoğraf sitesine etiket yazar gibi değil, usta bir görüntü
yönetmenine sahneyi tarif eder gibi yazın." Güncel modellerin tümü
(Midjourney v7+, gpt-image, Nano Banana, Flux) doğal dil cümlelerini anahtar
kelime yığınından daha iyi anlar.

### Teknik sözlük (tüm modellerde işler)

| Kategori | İşe yarayan ifadeler |
|---|---|
| Işık | golden hour, blue hour, Rembrandt lighting, rim light, backlit, volumetric light, neon glow, high-key, low-key, candlelit |
| Kamera/lens | 85mm portrait lens, 35mm environmental, 24mm wide-angle, macro, f/1.8 shallow depth of field, bokeh, long exposure, drone top-down, tilt-shift |
| Çekim ölçeği | extreme close-up, close-up, medium shot, full-body, wide/establishing shot, low angle, high angle, Dutch angle |
| Kompozisyon | rule of thirds, centered symmetry, leading lines, negative space, foreground framing |
| Doku/final | 35mm film grain, Kodak Portra look, cinematic color grade, teal-and-orange, matte finish, shot on iPhone (gündelik gerçekçilik için) |

### Kullanım amacına göre en-boy oranı

1:1 sosyal medya/ürün/avatar · 4:5 Instagram portre · 9:16 story/reels ·
16:9 sunum/YouTube · 3:2 klasik fotoğraf/baskı · 2:3 poster/kitap kapağı ·
21:9 geniş banner.

---

## 1. Midjourney

Varsayılan sürüm 2026 ortasında V8.1'dir; V7'ye `--v 7` ile erişilir ve
`--oref` (karakter tutarlılığı) yalnız V7'de bulunur. Yapı: önce doğal dil
tarif, sona parametreler. İdeal uzunluk ~50-150 token; daha uzunu seyreltir.

Sık kullanılan parametreler: `--ar` (en-boy), `--stylize/--s` (0-1000;
fotogerçekçilik için ≤50, çoğu iş için 250-400), `--chaos` (grid çeşitliliği),
`--sref URL` (stil referansı; içerik değil görünüm kopyalar), `--oref URL`
(özne/karakter tutarlılığı, V7), `--no x, y` (negatif prompt), `--seed`
(tekrarlanabilirlik), `--style raw` (asgari güzelleştirme; ürün/foto işinde
düşük `--s` ile birlikte).

**Portre örneği:**

```text
Dramatic close-up portrait, young woman with pale skin and auburn hair,
intense green eyes staring directly at camera, wearing dark wool coat,
rain falling around her face, captured with 85mm f/1.8 lens, cold
blue-silver lighting with warm rim light, melancholic atmosphere
--ar 4:5 --s 150 --v 7 --no anime, cartoon, illustration
```

**Ürün fotoğrafı örneği:**

```text
Minimalist perfume bottle with gold cap on polished black marble surface,
gradient background from deep purple to black, dramatic rim lighting with
soft front fill, commercial photography, premium luxury aesthetic
--ar 1:1 --s 25 --style raw
```

**Karakter tutarlılığı örneği (V7):**

```text
Cheerful barista handing a paper cup to a customer, cozy Istanbul coffee
shop interior, morning light through steamy windows
--oref https://example.com/character.png --ow 300 --ar 3:2 --v 7
```

---

## 2. OpenAI gpt-image Ailesi

Soy: DALL-E 3 (2023; Mayıs 2026'da emekliye ayrıldı) → gpt-image-1
(Nisan 2025) → gpt-image-1.5 (Aralık 2025) → **gpt-image-2 (Nisan 2026,
güncel motor)**. Bu modeller dil modeli üzerine kuruludur: parametre
bayrağı yoktur, yaratıcı brif gibi konuşma dilinde yazılır. Önerilen sıra:
**sahne/arka plan → özne → kritik detaylar → kısıtlar**; görselin nerede
kullanılacağını söylemek ("bu bir reklam görseli / arayüz taslağı")
cilalama düzeyini ayarlar.

Ayırt edici gücü **görsel içinde metin işleme**: yazılacak metni tırnak
içinde verin, font/renk/konum belirtin; yanlış çıkan kelimeyi harf harf
yazdırın. Boyut/kalite/şeffaf arka plan prompt değil API parametresidir
(`size`, `quality`, `background: transparent`).

Düzenlemede kural: "yalnız X'i değiştir, geri kalan her şeyi koru" —
korunacakları açıkça listeleyin ve her iterasyonda tekrarlayın; aksi halde
görsel adım adım kayar (drift).

**İnfografik örneği:**

```text
Create a detailed infographic of the functioning and flow of an automatic
coffee machine. From bean basket, to grinding, to scale, water tank,
boiler, etc.
```

**Türkçe metinli poster örneği:**

```text
A minimalist poster for a tech conference. Large headline text
"YAPAY ZEKA ZİRVESİ 2026" in a bold geometric sans-serif, dark navy on
off-white. Below it, smaller text: "15-16 Eylül, İstanbul". A single
abstract circuit-line illustration in orange. Lots of negative space.
Keep all wording exactly as written.
```

**Notlar:** Türkçe karakter içeren metinlerde "Keep all wording exactly as
written" ve gerekirse harf harf yazım, aksan hatalarını belirgin azaltır.
Yoğun/küçük metinli işlerde API'de `quality: high` kullanın; çok yoğun
infografik metni gerekiyorsa metni üretim sonrası yerel araçla bindirmek
(örn. PIL) hâlâ en güvenilir yoldur.

### gpt-image-2 — güncel motor (Nisan 2026)

Öncekilerden farkı (Son doğrulama: 2026-07):

- **Çizmeden önce akıl yürütür**; gerekirse web araması yapar ("güncel
  ürünlerle bir katalog posteri yap" tarzı istekler çalışır).
- **Metin işleme** çok dilli ve yoğun metinde güvenilir hale geldi
  (üçüncü taraf ölçümlerde ~%99 doğruluk iddiası; temkinli aktarıyoruz).
- Doğal 2K çözünürlük, 16:9 desteği, tek geçişte hızlı üretim.
- **Yerleşim (layout) talimatlarını gerçekten uygular**: "başlık sol üstte,
  ürün sağda, marka işareti sağ altta" gibi konum belirtimleri artık
  isabetlidir — kısa/belirsiz prompt bu modelin kapasitesini boşa harcar.
- **Çoklu varlık**: tek prompttan tutarlı görsel setleri.

**Yerleşim kontrollü slayt örneği:**

```text
Design a 16:9 conference slide titled "YAPAY ZEKA ÜRETİM HATTI".
Left-aligned bold sans-serif headline at top, three labeled boxes across
the center reading "VERİ", "MODEL", "DAĞITIM" connected by arrows, brand
mark bottom-right, dark navy background with amber accents, flat corporate
illustration style.
```

**Tutarlı set örneği:**

```text
Create a matching set of 4 social media assets for a coffee brand called
"KAVRUK": a 1:1 post, a 9:16 story, a 16:9 banner, and a square logo tile.
Same color palette (cream, espresso brown), same hand-drawn style, the
brand name rendered identically on each.
```

---

## 3. Google Gemini Görsel Ailesi (Imagen / "Nano Banana")

Soy: Gemini 2.5 Flash Image (ilk "Nano Banana") → Gemini 3 Pro Image
("Nano Banana Pro"; metin işleme ve çok turlu iş için en güçlüsü) →
Gemini 3.1 Flash Image (güncel ekonomik model). Anahtar kelime listesi değil
**anlatı** ister; model akıl yürüttüğü için niyet ve bağlam verebilirsiniz.

DeepMind'ın kapsanacak 5 boyutu: stil · özne · mekân · eylem · kompozisyon.

**Resmî fotogerçekçilik şablonu:**

```text
A photorealistic [shot type] of [subject] in [setting].
[Lighting description]. Shot from [angle] with [lens].
```

**Örnek:**

```text
A photorealistic wide-angle shot of a vibrant coral reef teeming with
tropical fish. Crystal-clear turquoise water with sunbeams filtering down
from the surface, illuminating a sea turtle gliding over the coral. 16:9.
```

Ayırt edici gücü **konuşarak düzenleme**: görseli üretin/yükleyin, sonra
sohbet içinde hedefli talimat verin. Karakter tutarlılığı için referans
görsel yükleyip **her karaktere isim verin** ve promptta o isimle çağırın.

**Düzenleme talimatı örneği:**

```text
Using the image I provided, change only the background to a rainy Tokyo
street at night with neon reflections. Keep the subject, her pose,
clothing, the lighting on her face, and the camera angle exactly the same.
```

---

## 4. Flux (Black Forest Labs)

Soy: FLUX.1 → FLUX.1 Kontext (talimatla düzenleme) → FLUX.2 (10'a kadar
referans görsel; JSON promptu resmî destekler — bkz. dosya 08). Doğal dil
cümleleri ister; Stable Diffusion alışkanlıkları burada zararlıdır:

- `masterpiece, best quality, 1girl` tarzı etiket yığını düz cümle olarak
  okunur (kelime görselde bile belirebilir).
- `(kelime)++` tarzı ağırlık sözdizimi yok; "with emphasis on ..." yazın.
- Standart API'de negatif prompt alanı yok; olumlu ifadeyle kurun
  ("boş, ıssız bir cadde" — "insan yok" değil).
- Katmanlı kompozisyon iyi çalışır: ön plan → orta plan → arka planı
  açıkça sırayla tarif edin.

**Örnek:**

```text
In the foreground, a vintage car with a 'CLASSIC' plate is parked on a
cobblestone street. Behind it, a bustling market scene with colorful
awnings. In the background, the silhouette of an old castle on a hill,
shrouded in mist.
```

---

## Sık Yapılan Hatalar

1. Doğal dil modellerinde anahtar kelime çorbası (etiket yığını).
2. Çelişen tarifler ("dark, moody" + "bright, cheerful").
3. Özneden önce stille başlamak; özne her zaman önce gelir.
4. Var olmayan negatif prompt alanı beklemek (gpt-image/Nano Banana/Flux'ta
   dışlamayı cümleyle, tercihen olumlu ifadeyle yazın).
5. Görsel içi metni tırnaklamamak.
6. Düzenleme yeteneği olan modellerde (Nano Banana, gpt-image, Kontext)
   baştan üretmeyi tekrar tekrar denemek — iterasyonla düzenleme daha hızlı
   ve tutarlıdır.

---

## Kaynaklar

- Midjourney resmî parametre dokümanı: docs.midjourney.com → "Parameter
  List" ve "Style Reference" sayfaları
- OpenAI Cookbook — "GPT Image Generation Models Prompting Guide" ve
  "gpt-image-1.5 prompting guide": developers.openai.com/cookbook
- OpenAI — "Introducing ChatGPT Images 2.0" duyurusu (gpt-image-2) ve
  görsel üretim API dokümanı: openai.com/index/ +
  developers.openai.com/api/docs/guides/image-generation
- Google DeepMind — Nano Banana prompt guide:
  deepmind.google/models/gemini-image/prompt-guide/
- Google Cloud — "Ultimate prompting guide for Nano Banana":
  cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
- Gemini API görsel üretim dokümanı: ai.google.dev/gemini-api/docs/image-generation
- Black Forest Labs — FLUX prompting rehberleri: docs.bfl.ml/guides/

Son doğrulama: 2026-07. Midjourney doküman sayfaları otomatik erişime
kapalı olduğundan parametre tablosu iki bağımsız 2026 kaynağından çapraz
doğrulanmıştır; baskı öncesi resmî dokümandan göz kontrolü önerilir.

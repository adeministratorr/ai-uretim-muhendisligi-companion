# Model Watch

Aylık model/araç uyumluluk kontrolü ve güncel karşılaştırma tabloları burada tutulur.
Kitap metninde model/araç adları kalıcı tavsiye gibi yazılmaz; güncel tablolar bu klasörde
yaşayan ek olarak güncellenir (bkz. kök dizindeki `../../companion_repo_plani.md` §8).

## Güncelleme Sıklığı

| Sıklık | Güncelleme |
|---|---|
| Aylık | Model/araç uyumluluk kontrolü (OpenAI, Claude, Gemini, Grok, DeepSeek, Qwen, Mistral, Kimi, MiniMax, Gemma) |
| Aylık | Prompt ve structured output örnekleri (bozulan API, değişen model davranışı) |
| Çeyreklik | Saha gerçekleri raporu (DORA, AI coding telemetry, güvenlik raporları, benchmark değişimleri) |

## Güncel Model Tablosu

> Bu tablo web araştırmasıyla derlenmiştir; belirsizliği işaretli satırlar (**doğrulanmamış**,
> **belirsiz**, **bilgi eksik**) resmî model kartı/duyuru ile teyit edilmeden kitap veya lab
> içeriğinde kesin bilgi gibi kullanılmamalıdır.

### Anthropic (Claude)

| Model | Yayın dönemi | Bağlam | Reasoning/Thinking | Ajan/Tool-use | Multimodal | Kodlama | Fiyat/Erişim |
|---|---|---|---|---|---|---|---|
| **Claude Opus 4.8** (varsayılan flagship) | 2026 | 1M / 128K çıktı | Adaptive thinking, `effort`: low→max | Claude Code / Agent SDK'nın çalıştırdığı model; Managed Agents | Görsel (yüksek çözünürlük) | Uzun ufuklu agentic kodlamada state-of-the-art | $5/$25 per MTok |
| Claude Sonnet 5 | 2026 | 1M / 128K | Adaptive (varsayılan açık) | Güçlü, Opus'a yakın agentic performans | Görsel (yüksek çöz.) | Neredeyse Opus seviyesi, düşük maliyet | $3/$15 (giriş fiyatı $2/$10, 2026-08-31'e kadar) |
| Claude Haiku 4.5 | önceki nesil | 200K / 64K | Sınırlı | Hızlı/basit görevler | Görsel | Temel | $1/$5 |
| Claude Fable 5 (+ Mythos 5) | 2026, üst segment | 1M / 128K | Her zaman açık | En iddialı uzun-ufuk agentic işler | Görsel, yüksek çöz. | En yetenekli (premium) | $10/$50 — en pahalı katman |

### OpenAI

| Model | Yayın dönemi | Bağlam | Reasoning | Ajan/Tool-use | Kodlama | Fiyat/Erişim |
|---|---|---|---|---|---|---|
| GPT-5.6 (Sol/Terra/Luna katmanları) | Temmuz 2026, en yeni | 1.4–1.5M+ (**belirsiz**) | 5+ seviyeli effort slider + "ultra" subagent modu | — | Güçlü | Katman bazlı, kamuya tam açık değil |
| **GPT-5.5** (Codex CLI'nin şu anki varsayılanı) | Nisan 2026 | 1M+ | Effort kontrolü | Codex CLI'nin ana modeli | GPT-5.4'ten az tokenle aynı görevi tamamlıyor | — |
| GPT-5.3-Codex-Spark | 2026 | — | — | Cerebras donanımında ilk OpenAI modeli | Codex'e özel | Pro kullanıcılara sınırlı |

Codex CLI'yi hangi model çalıştırıyor: varsayılan **GPT-5.5**; GPT-5.6 dağıtımı kısmi/belirsiz olabilir.

### Google (Gemini)

| Model | Yayın | Bağlam | Reasoning | Ajan/Tool-use | Multimodal | Fiyat/Erişim |
|---|---|---|---|---|---|---|
| **Gemini 3.1 Pro** (flagship) | 2026 | 1M | Deep Think modu | MCP Atlas %83.6, OSWorld computer-use %78.4 | Native, güçlü (MMMU-Pro %83.6) | $2/$12 per MTok (200K'ya kadar; üstünde $4/$18) |
| Gemini 3.5 Pro (duyuruldu) | Haziran sonu 2026, preview/**belirsiz** | 2M (iddia) | Deep Think | — | Frontier multimodal | Net değil |

### Meta (Llama)

Meta açık-ağırlık liderliğinden uzaklaşıyor: **Muse Spark** (Nisan 2026) artık **kapalı** —
yalnızca meta.ai ve özel API önizlemesi. Açık-ağırlıklı en güncel Meta modeli hâlâ
**Llama 4 Maverick**. Llama 5'in açık ağırlıkla geleceği **doğrulanmamış**.

### xAI (Grok)

| Model | Bağlam | Fiyat | Not |
|---|---|---|---|
| **Grok 4.3** (flagship) | 1M | $1.25/$2.50 per MTok | Grok 4.1 emekli, çağrılar 4.3'e yönleniyor |
| Grok 4.1 Fast (bütçe) | 2M | $0.20/$0.50 | — |
| Grok Build (kodlama) | 256K | $1.00/$2.00 | Yazılım mühendisliğine özel |
| Grok 5 | 1.5M (iddia) | — | 6T parametre MoE iddiası; **resmî spec yok, yüksek belirsizlik** |

### Mistral AI

**Mistral Large 3** (Aralık 2025) — açık ağırlık (Apache 2.0), MoE 675B toplam/41B aktif,
262K bağlam, güçlü çok dillilik ve görsel anlama. Temmuz 2026'da yeni bir açık-ağırlık
"frontier gap" modeli erken erişime giriyor (isim/spec **belirsiz**).

### DeepSeek

**DeepSeek V4** ailesi (Nisan 2026, açık ağırlık): V4-Pro (1.6T toplam/49B aktif) ve
V4-Flash (284B/13B aktif), ikisi de 1M bağlam. **R2 resmî olarak yayınlanmadı** —
sızıntı/söylenti düzeyinde, **doğrulanmamış**.

### Alibaba (Qwen)

Qwen 3.5 (Şubat 2026, açık kaynak, 397B-A17B MoE) → Qwen 3.6 dalgası (Nisan 2026:
35B-A3B MoE + tek-GPU çalışan yoğun Qwen 3.6-27B, agentic kodlamada 3.5 flagship'i geçiyor)
→ **Qwen 3.7 Max** duyuruldu (Mayıs 2026). Bazı yeni varyantlar (3.5-Omni, 3.6-Plus)
artık kapalı kaynak.

### Diğer oyuncular

| Vendor/Model | Yayın | Öne çıkan |
|---|---|---|
| Moonshot AI — Kimi K2.7 Code | Haz 2026 | Açık kaynak kodlama modeli |
| Moonshot AI — Kimi K3 | Q3 2026 bekleniyor | 2.5T parametre, ~1M bağlam — **henüz yayınlanmadı** |
| MiniMax M3 | 1 Haz 2026 | Açık ağırlık, 1M bağlam, multimodal, SWE-Bench Pro %59 |
| Z.ai GLM-5.2 | Haz 2026 | Açık ağırlık |
| Google Gemma | — | Açık ağırlık hattı devam ediyor — güncel spec **bilgi eksik** |

Son doğrulama: 2026-07

## Durum

İlk tablo dolduruldu (2026-07). Sonraki güncelleme aylık kontrol takvimine göre yapılacak;
her bölüm lab'ı bu tabloyu referans alır, kendi başına farklı bir model iddiası üretmez.

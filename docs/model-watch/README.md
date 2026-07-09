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

> Bu tablo iki ayrı web araştırması + bir doğrulama turuyla derlenmiştir (son tur: 2026-07-09,
> haftanın gelişmelerine özel odaklandı). Belirsizliği işaretli satırlar (**doğrulanmamış**,
> **belirsiz**, **tek kaynak turu**) resmî model kartı/duyuru ile teyit edilmeden kitap veya lab
> içeriğinde kesin bilgi gibi kullanılmamalıdır.

### Anthropic (Claude)

| Model | Yayın | Bağlam | Reasoning/Thinking | Ajan/Tool-use | Kodlama | Fiyat/Erişim |
|---|---|---|---|---|---|---|
| **Claude Opus 4.8** (flagship) | GA 2026-05-28 | 1M / 128K çıktı | Adaptive thinking, `effort`: low→max | Claude Code / Agent SDK'nın çalıştırdığı model | Uzun ufuklu agentic kodlamada state-of-the-art | Standart $5/$25 per MTok; "fast mode" (~2.5x hız) $10/$50 |
| **Claude Sonnet 5** (Claude Code varsayılanı) | 2026-06-30 | 1M / 128K | Adaptive (varsayılan açık) | Güçlü, Opus'a yakın agentic performans | Neredeyse Opus seviyesi | **Tanıtım fiyatı $2/$10 (2026-08-31'e kadar), sonra standart $3/$15**. Yeni tokenizer nedeniyle aynı metin ~%30 daha fazla token üretiyor — token bütçesi hesaplarında dikkat |
| Claude Haiku 4.5 | önceki nesil | 200K / 64K | Sınırlı | Hızlı/basit görevler | Temel | $1/$5 |
| Claude Fable 5 (+ Mythos 5) | 2026, üst segment | 1M / 128K | Her zaman açık | En iddialı uzun-ufuk agentic işler | En yetenekli (premium) | $10/$50. **Not:** 2026-06-12'deki bir ABD ihracat-kontrolü kararıyla global erişimden 18 gün kaldırıldı, 2026-07-01'de geri geldi — birden fazla kaynakta bildirildi ama bu depoda bağımsız doğrulanmadı |

### OpenAI

| Model | Yayın | Bağlam | Reasoning | Ajan/Tool-use | Kodlama | Fiyat/Erişim |
|---|---|---|---|---|---|---|
| **GPT-5.6** (Sol/Terra/Luna) | Sınırlı erişim 2026-06-26, geniş kamuya açılış **2026-07-09** | Söylenti ~1.5M, **resmen doğrulanmadı** | 5+ seviyeli effort slider + "ultra" subagent modu | — | Güçlü | Sol (flagship) $5/$30, Terra $2.50/$15, Luna $1/$6 |
| **GPT-5.5** (Codex CLI'nin şu anki varsayılanı) | Nisan 2026 | 1M+ | Effort kontrolü | Codex CLI'nin ana modeli | GPT-5.4'ten az tokenle aynı görevi tamamlıyor | — |
| GPT-5.3-Codex-Spark | 2026 | — | — | Cerebras donanımında ilk OpenAI modeli | Codex'e özel | Pro kullanıcılara sınırlı |

Codex CLI'yi hangi model çalıştırıyor: bu depodaki testlerde gözlemlenen varsayılan **GPT-5.5**;
GPT-5.6'ya geçiş henüz teyit edilmedi.

### Google (Gemini / Gemma)

| Model | Yayın | Bağlam | Reasoning | Ajan/Tool-use | Fiyat/Erişim |
|---|---|---|---|---|---|
| **Gemini 3.1 Pro** (flagship) | 2026 | 1M | Deep Think modu | MCP Atlas %83.6, OSWorld computer-use %78.4 | $2/$12 per MTok (200K'ya kadar; üstünde $4/$18) |
| Gemini 3.5 Pro | **Henüz GA değil** — Mayıs I/O'da duyuruldu, Haziran hedefinden kaydı, söylenti 2026-07-17 (resmî değil) | 2M (iddia, **doğrulanmamış**) | Deep Think | — | Net değil |
| Gemma 4 (açık ağırlık, Apache 2.0) | 2026-04-02 (temel), 12B varyant 2026-06-03 | 256K'ya kadar | — | — | E2B/E4B/26B-A4B MoE/31B dense boyutları, çoklu-modal |

### Meta (Llama)

Meta açık-ağırlık liderliğinden uzaklaşıyor: **Muse Spark** (2026-04-08, kapalı ağırlık) —
Artificial Analysis Index'te 52 puan, Llama 4 Maverick'in (18 puan) ~3 katı. Açık-ağırlıklı en
güncel Meta modeli hâlâ **Llama 4 Maverick**; ardılı yok, strateji kapalı modele kaymış durumda.

### xAI

| Model | Bağlam | Fiyat | Not |
|---|---|---|---|
| **Grok 4.5** (yeni flagship) | **500K — Grok 4.3'ün 1M'ine göre gerileme** | $2/$6 (cache girişi $0.50) | Geliştiricilere 2026-07-08, halka 2026-07-09'da açıldı; "V9" temel model üzerine, Cursor ile birlikte eğitilmiş; Artificial Analysis'te 168 modelde 54 puan/4. sıra; AB'de henüz yok |
| Grok 4.3 (önceki flagship) | 1M | $1.25/$2.50 per MTok | Artık ikincil konumda |
| Grok 4.1 Fast (bütçe) | 2M | $0.20/$0.50 | Bu turda yeniden doğrulanmadı |
| Grok Build (kodlama) | 256K | $1.00/$2.00 | Bu turda yeniden doğrulanmadı |

**Not (tek tur, çoklu kaynak — Axios/TechCrunch/Forbes):** xAI/SpaceX birleşmesi sonrası şirket
bazı kaynaklarda "SpaceXAI" olarak anılmaya başladı; bu depoda bağımsız doğrulanmadı, izlenmeli.
"Grok 5" söylentisi muhtemelen anlamsızlaştı — 4.5 doğrudan çıktı, isimlendirme atlanmış olabilir.

### Mistral AI

**Mistral Large 3** (2025-12-02) hâlâ flagship — açık ağırlık (Apache 2.0), MoE 675B toplam/
41B aktif, 262K bağlam. Temmuz başında uzman modeller yayımlandı (genel sohbet modeli değil):
Robostral Navigate (robotik navigasyon), Mistral OCR 4, Leanstral 1.5 (Lean 4 teorem-kanıtlama).
Ayrıca isimsiz yeni "seyrek ama büyük" MoE açık-ağırlık model Temmuz'da erken erişime giriyor —
spek yok, **belirsiz**.

### DeepSeek

**DeepSeek V4** önizlemesi 2026-04-24 (V4-Pro 1.6T toplam/49B aktif, V4-Flash 284B/13B aktif,
1M bağlam); **resmî/tam sürüm orta Temmuz 2026'ya planlı, henüz tam GA değil**. **R2 hâlâ
yayımlanmadı**, resmî tarih yok (kaynaklara göre performanstan memnuniyetsizlik nedeniyle
gecikiyor) — **doğrulanmamış/söylenti düzeyinde**.

### Alibaba (Qwen)

Qwen 3.5 (Şubat 2026) → Qwen 3.6 (Nisan 2026) → **Qwen 3.7 Max fiilen piyasaya çıktı**
(2026-05-19/21, Hangzhou Cloud Summit): 1M bağlam, Artificial Analysis Index 56.6 (5. sıra,
#1 Çin modeli), Terminal-Bench Hard %50.8, en düşük halüsinasyon oranı (%22.9). Çoklu-modal
kardeşi Qwen3.7-Plus de mevcut.

### Diğer oyuncular

| Vendor/Model | Yayın | Öne çıkan |
|---|---|---|
| Moonshot AI — Kimi K2.7 Code / K2.6 | Haz 2026 | Şu an mevcut açık kaynak kodlama modelleri |
| Moonshot AI — Kimi K3 | **Henüz yayımlanmadı**; Temmuz 2026 içinde bekleniyor (personel kaynaklı) | 3-4T parametre, ~1M bağlam iddiası — **doğrulanmamış** |
| MiniMax M3 | 2026-06-01 | Açık ağırlık, 229.9B toplam/9.8B aktif MoE, "MiniMax Sparse Attention", 1M bağlam, SWE-Bench Pro %59 |
| Z.ai GLM-5.2 | 2026-06-13 | Açık ağırlık (MIT), 744B toplam/40B aktif MoE, 1M bağlam (5.1'in 200K'sinden büyük sıçrama), FrontierSWE'de Opus 4.8'e yalnızca %1 geride |
| Google Gemma | yukarıya taşındı (bkz. Google tablosu) | — |

**Hâlâ belirsiz/izlenmeli:** Gemini 3.5 Pro kesin tarih/spek; DeepSeek R2; Kimi K3; Mistral'ın
isimsiz yeni açık-ağırlık modeli; GPT-5.6 resmî bağlam penceresi rakamı; "SpaceXAI" adlandırması;
Grok 4.1 Fast/Build güncel spek.

Son doğrulama: 2026-07-09

## Durum

İlk tablo dolduruldu ve aynı gün içinde bir doğrulama turuyla güncellendi (2026-07-09) —
hızlı hareket eden bir hafta yakalandı (Grok 4.5, GPT-5.6 geniş kamuya açılışı, Qwen 3.7 Max,
Gemma 4, MiniMax M3, GLM-5.2 hepsi Haziran-Temmuz 2026 içinde). Sonraki güncelleme aylık kontrol
takvimine göre yapılacak; her bölüm lab'ı bu tabloyu referans alır, kendi başına farklı bir model
iddiası üretmez.

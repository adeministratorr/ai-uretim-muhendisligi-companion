# Kitap Destek Deposu — Yapay Zekâ ile Üretim Mühendisliği Serisi

Bu depo, dört ciltlik Türkçe kitap serisinin (Prompt Mühendisliği · Vibe Coding ve Loop
Engineering · Agent Engineering · AI-Native Production) **companion (destek) deposudur**.
Yalnızca örnek kod deposu değildir; kitabın uygulama laboratuvarı, güncel araç/model izleme
alanı ve web yayınının teknik tamamlayıcısıdır.

Kitap: *Yapay Zekâ Okuryazarlığı ve Prompt Mühendisliği* ve devamı ciltler.

---

## Bu Depo Ne İşe Yarar?

- Kitapta anlatılan kavramların çalışan örneklerini sunar.
- Prompt, skill, loop, eval, schema, MCP ve agent örneklerini tek yerde toplar.
- Okurun AI ile ürettiği kodu test, review, checkpoint ve rollback disipliniyle yönetmesini öğretir.
- Web yayınındaki bölüm sayfalarına kod, şablon ve güncel tablo bağlantısı sağlar.
- Model ve araç ekosistemi değiştikçe güncellenen bir alan olarak çalışır.
- Etkileşimli HTML laboratuvarlarını <https://lab.ademyuce.tr> adresinde kurulumsuz sunar
  (örnek: [temperature/top-p/top-k laboratuvarı](https://lab.ademyuce.tr/cilt-1-prompting/parameter-matrix/sampling_lab.html)).
- `prompt-kutuphanesi/` klasöründe, yazılımdan görsel/video üretimine ve günlük hayata
  uzanan alan alan bir prompt koleksiyonu sunar.

**Temel ilke:** Bu repo hem insan okur hem de coding agent tarafından okunabilir olmalıdır.

---

## Repo Haritası

```text
├── AGENTS.md              ← Coding agent davranış sözleşmesi (izinler, yasaklar, commit kuralı)
├── CLAUDE.md               ← Claude Code / CLI agent proje kuralları
├── SPEC_TEMPLATE.md         ← Yeni örnek/lab eklemeden önce doldurulacak mini spec şablonu
├── CONTRIBUTING.md          ← Okur katkı rehberi ve kabul kriterleri
├── SECURITY.md              ← Güvenlik/kalite kapıları
├── CHANGELOG.md             ← Kitap/web/repo güncelleme notları
├── docs/
│   └── model-watch/         ← Aylık model/araç uyumluluk takibi
├── prompt-kutuphanesi/      ← Alan alan prompt koleksiyonu (yazılım, iş, görsel, video, JSON, trend...)
├── cilt-1-prompting/        ← Prompt mühendisliği ve structured output örnekleri
├── cilt-2-loops/            ← Vibe coding, checkpoint, debug loop, mutation test örnekleri
├── cilt-3-agents/           ← Tool schema, MCP, ACI/poka-yoke, multi-agent örnekleri
└── cilt-4-production/       ← Model gateway, guardrails, eval, observability, AI review
```

Her klasörün kendi README'i, o klasörün amacını ve (doldurulduğunda) hızlı başlangıç
adımlarını taşır.

`cilt-1-prompting/` içindeki dolu lab klasörleri (her biri README + saf-Python lab +
kurulumsuz HTML + pytest testi içerir): `parameter-matrix/`, `prompt-patterns/`,
`structured-outputs/`, `model-selection/`, `instruction-hierarchy/`, `prompt-log/`,
`task-templates/`, `reliability-check/`, `model-gateway-framework/`,
`exercises/impact-effort-matrix/`, `exercises/data-sensitivity-classifier/`,
`exercises/tool-permission-audit/`, `exercises/guardrail-chain-check/`,
`exercises/competency-matrix/`.

---

## Hızlı Başlangıç (Cilt Bazlı)

| Cilt | Konu | Klasör |
|---|---|---|
| 1 | Prompt Mühendisliği ve Structured Output | `cilt-1-prompting/` |
| 2 | Vibe Coding ve Loop Engineering | `cilt-2-loops/` |
| 3 | Agent Engineering | `cilt-3-agents/` |
| 4 | AI-Native Production | `cilt-4-production/` |

Şu an yalnızca ilk uygulama paketindeki klasörler açık; her klasördeki README, o örneğin
ne zaman doldurulacağını belirtir. Kitabın ilgili bölümü yayınlandıkça klasör içeriği
doldurulur.

---

## Katkı

Okur katkıları kabul edilir; bkz. `CONTRIBUTING.md`.

## Güvenlik

Repo örnekleri yayınlanmadan önce kalite kapılarından geçer; bkz. `SECURITY.md`.

## Lisans

Bu depodaki örnek kod, `LICENSE` dosyasındaki MIT lisansı ile paylaşılır. Kitap metninin
kendisi bu lisansın kapsamında değildir.

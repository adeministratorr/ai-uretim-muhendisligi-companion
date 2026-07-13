# Changelog

Bu dosya, kitap/web/repo güncellemelerini sürüm bazlı kaydeder.

## [Yayınlanmadı]

### Prompt Kütüphanesi eklendi (2026-07-13)

- `prompt-kutuphanesi/`: seriyi destekleyen, alan alan düzenlenmiş prompt
  koleksiyonu (README + 13 kategori dosyası): yazılım geliştirme, yazma ve
  içerik, iş ve verimlilik, eğitim ve öğrenme, veri analizi, görsel üretim
  (Midjourney/gpt-image-2/Nano Banana/Flux + üretim modları), video üretim
  (Veo 3.1/Kling/Runway/Pika/Luma + dudak senkronu), JSON/yapılandırılmış
  promptlar, sosyal medya trend promptları, kurumsal şablonlar, sosyal
  medya yönetimi, günlük hayat, strateji ve pazarlama.
- Kaynak ve lisans notları dosya sonlarında; prompts.chat içerikleri CC0,
  resmî model rehberleri atıflı. Hızla eskiyen bilgiler `Son doğrulama:
  2026-07` notu taşır.

### Eklendi

- Repo iskeleti oluşturuldu: `AGENTS.md`, `CLAUDE.md`, `SPEC_TEMPLATE.md`, `CONTRIBUTING.md`,
  `SECURITY.md`.
- İlk uygulama paketi klasör yapısı açıldı: `cilt-1-prompting/structured-outputs/`,
  `cilt-2-loops/{checkpoints,debug-loops,mutation-tests}/`,
  `cilt-3-agents/{tool-schemas,aci-poka-yoke}/`, `cilt-4-production/ai-review/`,
  `docs/model-watch/`.
- Kaynak plan: `companion_repo_plani.md` (kitap projesi deposunda).

### Cilt 1, Bölüm 1 için eklendi (2026-07-05)

- `cilt-1-prompting/parameter-matrix/`: temperature/top-p/top-k laboratuvarı.
  - `sampling_lab.html` — kurulumsuz, tarayıcıda çalışan interaktif versiyon (kaydırıcılar).
  - `sampling_lab.py` + `test_sampling_lab.py` — aynı mantığın Python sürümü, 5 test.
  - Kitap bağlantısı: Cilt 1, Bölüm 1, 1.6-1.8 (Şekil 1.6).

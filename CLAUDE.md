# CLAUDE.md

Bu repo, dört ciltlik Türkçe AI kitap serisinin companion deposudur. Claude Code veya benzeri CLI agent'lar bu dosyadaki kurallara göre çalışır.

---

## Proje Amacı

Kitapta anlatılan kavramları çalışan kod, prompt, schema, eval, MCP, loop ve production örnekleriyle desteklemek.

Ana cilt klasörleri:

- `cilt-1-prompting/`
- `cilt-2-loops/`
- `cilt-3-agents/`
- `cilt-4-production/`

---

## Çalışma Standardı

- Önce ilgili bölümü ve README dosyasını oku.
- Kapsam dışı refactor yapma.
- Türkçe açıklama yaz; teknik terimleri ilk kullanımda İngilizce karşılığıyla ver. Terim çevirilerinde seri sözlüğüne bağlı kal; aynı kavrama iki farklı Türkçe karşılık kullanma.
- Kod örneği öğretici ama oyuncak problem düzeyinde kalmayacak kadar gerçekçi olmalı.
- Test veya doğrulama adımı olmayan örnek final sayılmaz.
- Yeni bağımlılık eklemeden önce paketin registry'de gerçekten var olduğunu doğrula ve sürümü sabitle (dependency hallucination koruması).
- Model adı, fiyat, benchmark ve lisans gibi hızla eskiyen bilgiler `Son doğrulama: YYYY-AA` notu taşır.
- Agent güvenlik kuralları, commit biçimi ve terminal state'ler için `AGENTS.md` dosyasına uy.

---

## Komutlar

Bu alan companion repo oluşturulunca gerçek komutlarla doldurulacaktır.
Komutlar örnektir; ilgili paket veya script repoda yoksa çalıştırılmış gibi raporlanmaz.

```bash
# Python örnekleri
python -m pytest
python -m ruff check .

# TypeScript örnekleri
npm test
npm run lint

# Web çıktı kontrolü
npm run build
```

---

## Kod Tarzı

- Python örneklerinde tip ipucu tercih edilir.
- TypeScript örneklerinde açık type/interface kullanılır.
- Shell scriptleri `set -euo pipefail` ile yazılır.
- Örnekler küçük tutulur ama gerçek iş akışı gösterir.
- Gerçek secret veya gerçek kişisel veri kullanılmaz. Örnek değer gerekiyorsa açıkça placeholder olarak yazılır: `EXAMPLE_API_KEY`, `example@example.com` gibi.
- Kurgusal kişi, kurum veya veri gerçek vaka gibi sunulmaz.

---

## Güvenlik

Şunları yapma:

- Testleri silme.
- Assertion'ları zayıflatma.
- `.env` dosyası okuma veya yazma.
- API key, token veya cookie loglama.
- Kullanıcı onayı olmadan destructive komut çalıştırma.
- Kullanıcı onayı olmadan gerçek dış servise okuma/yazma işlemi yapma.

---

## Bölüm Bağlantısı

Her örnek dosyada mümkünse şu metadata bulunur:

```yaml
volume: 2
chapter: 12
book_section: "Hata Ayıklama ve Versiyon Kontrolü"
concepts:
  - Git checkpoint
  - failing test
  - rollback
objectives:
  - "2.12.3"   # kitaptaki öğrenme hedefi numarası
last_verified: "2026-07"
```

---

## Tamamlanma Kriteri

Bir görev ancak şu koşullarda tamamlanmış sayılır:

- Kod veya doküman değişikliği hedefle uyumlu.
- Doğrulama komutu çalıştırılmış veya neden çalıştırılamadığı yazılmış.
- Risk varsa açıkça belirtilmiş.
- Değişiklik küçük ve review edilebilir.

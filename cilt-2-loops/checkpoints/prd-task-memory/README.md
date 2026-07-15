# PRD ve Proje Hafızası Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 8 — PRD, TASKS ve Proje Hafızası,
8.2-8.6, 8.10-8.13 ve 8.15 (Lab 8 — PRD + TASKS.md + DECISIONS.md).

```yaml
volume: 2
chapter: 08
book_section: "8.2-8.6 PRD, 8.10 Kabul Kriterleri, 8.11-8.13 TASKS.md ve 8.15 Decision Log"
concepts:
  - PRD
  - EARS benzeri kabul kriteri
  - görev parçalama
  - decision log
objectives:
  - "LO-8.2"
  - "LO-8.4"
  - "LO-8.5"
  - "LO-8.6"
last_verified: "2026-07"
```

## Ne Yapar?

Bir özellik için hazırlanan `PRD.md`, `TASKS.md` ve `DECISIONS.md` metinlerini aynı
kabul kapısından geçirir. Doğrulayıcı şu koşulları denetler:

- PRD, Amaç'tan Başarı Kriterleri'ne kadar altı zorunlu bölümü taşır.
- Kapsam bölümünde rolü ve sonucu yazılmış en az iki user story bulunur.
- Out-of-Scope bölümü en az bir madde içerir; başarı kriterlerinden en az biri EARS
  benzeri koşul-davranış kalıbıyla yazılmıştır.
- TASKS.md en az beş görevi `[ ]`, `[~]` veya `[x]` durumuyla kaydeder. Tamamlanan
  her görev, hangi testin ya da denetimin çalıştığını belirten bir doğrulama notu taşır.
- DECISIONS.md en az iki kararı `Tarih | Karar | Gerekçe` tablosunda tutar.

Bu üç dosya aynı işi yapmaz. PRD niyeti ve sınırı, TASKS.md güncel ilerlemeyi,
DECISIONS.md ise kararın gerekçesini kaydeder.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/prd-task-memory/prd_task_memory_lab.html>
İsterseniz `prd_task_memory_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Üç metin alanındaki Vardiya örneğini kendi fikrinizle değiştirip **Belgeleri Doğrula**
düğmesine basın.

**Kod biliyorsanız:** Saf Python sürümü gömülü örnekle veya kendi dosyalarınızla
çalışır.

```bash
python3 prd_task_memory_lab.py
python3 prd_task_memory_lab.py PRD.md TASKS.md DECISIONS.md
python3 -m pytest test_prd_task_memory_lab.py
```

İlk komut kurgusal Vardiya belgelerini doğrular. İkinci komut verdiğiniz üç dosyayı
okur; dosyalara yazmaz. Üçüncü komut eksik PRD bölümünün, belirsiz görev durumunun,
doğrulama notu olmayan tamamlanmış işin ve gerekçesiz kararın reddedildiğini sınar.

## Beklenen Çıktı

```text
PRD ve Proje Hafızası — doğrulama
PRD bölümü: 6/6
User story: 2
TASKS.md görevi: 5 (tamamlandı: 2)
DECISIONS.md kararı: 2
Kabul kriteri karşılandı: Belge üçlüsü yapısal denetimden geçti.
```

Bir ölçüt karşılanmazsa sonuç başarılı sayılmaz. Doğrulayıcı eksik başlığı, görev
durumunu veya karar kaydını ayrı satırda gösterir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 prd_task_memory_lab.py`).
- [x] Test komutu var (`pytest`).
- [x] Beklenen çıktı gösteriliyor.
- [x] PRD'nin altı bölümü, iki user story ve EARS benzeri kabul kriteri denetleniyor.
- [x] TASKS.md en az beş durumlu görev ve tamamlanan işler için doğrulama notu taşıyor.
- [x] DECISIONS.md en az iki tarihli, gerekçeli karar taşıyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü Vardiya belgeleri kurgusaldır. Bir üretim sisteminin gereksinimi veya gerçek
  bir işletmenin kaydı değildir.
- Doğrulayıcı belge yapısını denetler. Bir user story'nin gerçekten değer taşıdığını,
  görevin yeterince küçük olduğunu veya kararın teknik açıdan doğru olduğunu ölçemez.
- `[~]` işareti bu laboratuvarda “devam ediyor” durumunu gösterir. Standart Markdown
  onay kutusu değildir; başka araçlar bu işareti farklı yorumlayabilir.
- Bir görevin yanında test adı yazması, testin gerçekten çalıştığını kanıtlamaz. Test
  çıktısını ve diff'i ayrıca inceleyin.
- Gerçek kişi verisini, gizli anahtarı veya kurum içi hassas bilgiyi tarayıcı formuna
  ya da örnek belgelere koymayın.

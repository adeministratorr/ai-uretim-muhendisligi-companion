# Rule Dosyası Denetimi Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 9 — Rule Dosyaları, 9.12-9.15
(Lab 9 — Bir Proje İçin Rule Dosyası Hazırlama).

```yaml
volume: 2
chapter: 09
book_section: "9.12-9.15 İzin Kuralları, Compiled Enforcement ve Takım Kuralları"
concepts:
  - rule dosyası
  - permission rule
  - compiled enforcement
  - PR devre kesici
objectives:
  - "LO-9.4"
  - "LO-9.5"
  - "LO-9.6"
last_verified: "2026-07"
```

## Ne Yapar?

Bir `AGENTS.md`, `CLAUDE.md` veya rules dosyası taslağını Bölüm 9'daki Lab 9
ölçütleriyle denetler. Doğrulayıcı şu koşulları arar:

- Proje Özeti bölümünde teknoloji yığını ve temel mimari kararı anlatan 2-3 madde.
- Yasak İşlemler bölümünde en az üç somut kural ve bunlardan en az biri için
  `[deny]` etiketi.
- Zorunlu Doğrulama Adımları bölümünde en az üç kontrol ve bunlardan en az biri
  için `[compiled]` etiketi.
- PR Devre Kesici bölümünde durma koşulunu ve PR'ın duracağını açıkça yazan en az
  bir `[pr-stop]` maddesi.
- Yinelenmeyen kurallar; açık e-posta adresi veya gizli bilgi ataması içermeyen
  temsilî içerik.

Etiketler denetim katmanını görünür kılar. `[directive]` yazılı yönergedir;
`[deny]` bir izin kuralına (permission rule), `[compiled]` ise test, linter veya CI denetimine
bağlanması gereken maddeyi gösterir. `[pr-stop]`, birleştirme akışını durduran
somut koşulu işaretler.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/rule-enforcement/rule_enforcement_lab.html>
İsterseniz `rule_enforcement_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Vardiya için hazırlanmış temsilî metni kendi proje kurallarınızla değiştirip
**Rule Dosyasını Doğrula** düğmesine basın.

**Kod biliyorsanız:** Saf Python sürümünü gömülü örnekle veya kendi Markdown
dosyanızla çalıştırın.

```bash
python3 rule_enforcement_lab.py
python3 rule_enforcement_lab.py AGENTS.md
python3 -m pytest test_rule_enforcement_lab.py
```

İlk komut temsilî Vardiya kuralını denetler. İkinci komut verdiğiniz dosyayı okur;
dosyaya yazmaz. Üçüncü komut eksik bölümün, yetersiz kural sayısının, yanlış katman
etiketinin, belirsiz devre kesicinin ve hassas veri örüntüsünün reddedildiğini sınar.

## Beklenen Çıktı

```text
Rule Dosyası Denetimi
Proje özeti: 2 madde
Yasak işlem: 3 ([deny]: 1)
Doğrulama adımı: 3 ([compiled]: 2)
PR devre kesici: 1
Kabul kriteri karşılandı: Rule dosyası yapısal denetimden geçti.
```

Bir ölçüt karşılanmazsa sonuç başarılı sayılmaz. Doğrulayıcı eksik başlığı,
yanlış etiketi veya belirsiz durma koşulunu ayrı satırda gösterir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 rule_enforcement_lab.py`).
- [x] Test komutu var (`pytest`).
- [x] Beklenen çıktı gösteriliyor.
- [x] Proje özeti 2-3 madde, en az üç yasak işlem ve üç doğrulama adımı taşıyor.
- [x] En az bir `[deny]`, bir `[compiled]` ve bir koşullu `[pr-stop]` maddesi denetleniyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü Vardiya kural dosyası temsilîdir. Gerçek bir ürün ayarı, kurum politikası
  veya üretim sistemi yapılandırması değildir.
- `[deny]` etiketi tek başına bir işlemi engellemez. Kural, kullanılan aracın gerçek
  izin kuralı ayarında `deny` olarak tanımlanmalıdır.
- `[compiled]` etiketi testin veya CI kontrolünün kurulduğunu kanıtlamaz. İlgili komutun
  depoda bulunduğunu ve birleştirme öncesi zorunlu çalıştığını ayrıca doğrulayın.
- Doğrulayıcı açık e-posta adreslerini ve yaygın gizli bilgi atamalarını yakalar.
  Serbest metindeki bütün kişisel verileri belirleyemez; insan incelemesi gerekir.
- Bir kuralın doğru başlık altında ve somut yazılması, aracın onu her durumda doğru
  yorumlayacağını garanti etmez. Kritik işlemler işletim sistemi ve CI düzeyindeki
  denetimlerle desteklenmelidir.

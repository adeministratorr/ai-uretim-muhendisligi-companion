---
volume: 1
chapter: 14
book_section: "Guardrails ve İnsan Gözetimi"
concepts:
  - guardrail
  - denetim zinciri
  - araç risk sınıflandırması
  - insan onayı
objectives:
  - "LO-14.3"
  - "LO-14.6"
last_verified: "2026-07"
---

# Guardrail Zinciri Denetimi Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 14 — Guardrails ve İnsan Gözetimi, özellikle
14.1 (girdi guardrail → ajan → çıktı guardrail zinciri) ve 14.6 (araç risk
sınıflandırma tablosu).

## Ne Yapar?

Bölüm 14, bir ajanın etrafındaki denetimi tek bir kontrole değil, birbirini
tamamlayan katmanlara (girdi guardrail, çıktı guardrail, insan onayı)
dayandırır. 14.6'daki tablo bu katmanları araç bazında somutlaştırır: her araç
bir risk düzeyi (düşük / orta / yüksek / kritik) taşır ve risk yükseldikçe
beklenen guardrail katmanı sayısı artar; kritik risk taşıyan bir araç
(örneğin yetki yükseltme) insan onayı olmadan hiçbir zaman otomatik
yürütülmemelidir.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, bir ajan akışındaki her aracın
beyan edilen risk seviyesini fiilen tanımlı guardrail katmanlarıyla karşılaştırır:

- `guardrail_chain_check.py`: `REQUIRED_LAYERS` politikasını (14.6'daki tablodan
  türetilmiştir) her araca uygular, eksik katmanları listeler ve kritik risk
  seviyesinde insan onayı eksikse bunu ayrı, yüksek öncelikli bir uyarı olarak
  işaretler.
- `chain_template.json`: kendi araç zincirinizi doldurmak için boş şablon.
- `example_incident.json`: bölümün açılış olayı — BT Destek Ajanı'nın yetki
  yükseltme aracı kritik risk taşır ama insan onayı katmanı tanımlı değildir.
- `example_fixed.json`: Barış'ın ekibinin 14.6'da anlatılan yeniden tasarımından
  sonraki, tamamen uyumlu hâli.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/exercises/guardrail-chain-check/guardrail_chain_check.html>
İsterseniz `guardrail_chain_check.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. "Bölüm
başındaki olayı yükle" ve "14.6'daki düzeltilmiş hâli yükle" düğmeleriyle iki
durumu karşılaştırabilir; risk seviyesi ve katman kutucuklarını değiştirdikçe
denetim sonucu canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `guardrail_chain_check.py`
dosyasındadır.

```bash
python3 guardrail_chain_check.py example_incident.json   # bölüm başındaki olay
python3 guardrail_chain_check.py example_fixed.json       # 14.6'daki düzeltilmiş hâl
python3 -m pytest                                          # testler (6 test, bağımlılık: pytest)
```

Kendi araç zincirinizi denetlemek için:

```bash
cp chain_template.json benim_zincirim.json
python3 guardrail_chain_check.py benim_zincirim.json
```

## Beklenen Çıktı (özet)

```text
Denetlenen araç: 4 | Uyumlu: 3/4
- [UYUMLU] Bilgi bankasında arama (risk: düşük) — gerekli: girdi denetimi | tanımlı: girdi denetimi
- [UYUMLU] Destek kaydı oluşturma/güncelleme (risk: orta) — ...
- [UYUMLU] Standart kullanıcı şifre sıfırlama (risk: yüksek) — ...
- [EKSİK] Yetki yükseltme / yönetici erişimi verme (risk: kritik) — gerekli: girdi denetimi, çıktı doğrulama, insan onayı | tanımlı: girdi denetimi, çıktı doğrulama
    [YÜKSEK ÖNCELİKLİ] 'insan onayı' katmanı tanımlı değil.
Kritik boşluk: Yetki yükseltme / yönetici erişimi verme — bölüm başındaki sahte yetki yükseltme olayıyla aynı desen (kritik risk seviyesinde otomatik yürütme, insan onayı yok).
```

`example_fixed.json` ile çalıştırıldığında dördü de UYUMLU görünür ve
"Kritik boşluk" satırı hiç yazılmaz.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3, gerçek API çağrısı yok).
- [x] Örnek çalışıyor (`python3 guardrail_chain_check.py`).
- [x] Test/doğrulama komutu var (`pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu araç bir guardrail katmanının gerçekten çalıştığını doğrulamaz; yalnızca
  beyan edilen risk seviyesi ile beyan edilen katmanlar arasındaki
  tutarsızlığı görünür kılar. Bir katman "tanımlı" işaretlenip fiilen bozuk
  veya devre dışı olabilir — bu laboratuvarın kapsamı dışındadır.
- `REQUIRED_LAYERS` politikası kitabın 14.6'daki dört seviyeli tablosundan
  türetilmiştir; farklı bir ajan/organizasyon farklı bir eşleme (örneğin orta
  riskte de insan onayı isteyen bir politika) tercih edebilir. Bu durumda
  politika sabiti kendi ihtiyacınıza göre güncellenmelidir.
- Girdi denetimi ve çıktı doğrulama burada tek bir boole (var/yok) olarak
  modellenir; 14.2-14.5'teki dört ayrı içerik guardraili (alaka düzeyi,
  güvenlik, PII, moderasyon) veya 14.7'deki çıktı doğrulama ayrıntıları bu
  laboratuvarda ayrıştırılmaz — bkz. bölüm metni.

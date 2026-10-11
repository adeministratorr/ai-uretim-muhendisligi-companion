# Model seçimi ve ölçüm | En iyi model hangisi değil, hangi işte daha iyi?

**[Türkçe](../tr/model-secimi-ve-olcum.md) · [English](../en/model-secimi-ve-olcum.md)** · [Model Watch](../README.md)

**Yöntem sürümü:** 2026-10 · **Bu repo için durum:** Değerlendirme şablonu; aşağıdaki puanlar örnektir, gerçek benchmark sonucu değildir.

Bir modeli seçerken yalnızca en yüksek puanlı modeli ararsak iki sorun yaşarız: ölçmediğimiz bir başarıya para öderiz, ayrıca sonuç kötüleştiğinde neyi geri alacağımızı bilemeyiz. Bu bölüm, kitap serisinin **istem → çıktı → doğrulama → geri bildirim → iyileştirme** yaklaşımını somut bir model seçme yöntemine bağlar.

## 1. Önce görevi tanımla

| Görev | Başarılı sayılma koşulu | Örnek kontrol |
|---|---|---|
| Türkçe eğitim metni düzenleme | Anlamı koruyan, doğal, tutarlı ve ölçülü dil | Kör insan değerlendirmesi + anlam karşılaştırması |
| JSON / structured output | Şemaya tam uyum, doğru alanlar | JSON Schema doğrulama + içerik kontrolü |
| Kod onarımı | Hata giderildi; eski testler bozulmadı | Failing test → fix → test + regression |
| Agent / MCP | İzinli aracı doğru seçti, tekrar ve maliyet sınırlı | Tool trace + izin denetimi + terminal state |
| Uzun doküman | Bölümler arası doğru atıf ve tutarlılık | Kaynak destekli soru seti + rastgele konumlama |
| Çok biçimli okuma | Görsel/tablo içeriğini uydurmadan çözümleme | İşaretlenmiş örnekler ve kritik hata kontrolü |
| Yüksek hacimli sınıflandırma | Düşük maliyetle istikrarlı doğruluk | Precision/recall + throughput + $/doğru sonuç |

## 2. Aynı koşullarda dene

- Aynı veri bölümü: 20–50 başlangıç örneği; üretime geçmeden önce temsil gücü artırılır.
- Aynı istem sürümü, aynı araç ve ağ izni, aynı şema ve aynı kabul kriteri.
- Rastgelelik destekleniyorsa sabitlenir; desteklenmiyorsa tekrarlı çağrılarla varyans ölçülür.
- Aynı kod tabanı snapshot'ı, aynı testler, aynı gizlilik düzeyi ve aynı görev bütçesi.
- Model ID'si, tarih, API endpoint, bölge, reasoning seviyesi ve kullanılan servis katmanı kaydedilir.
- Üretici veya üçüncü taraf benchmark sonuçları **bu testlerin yerine geçmez**.

## 3. Puan kartı

Şablon ağırlıkları her proje için önceden belirlenir. Aşağıdaki **örnek ağırlıklar** performans sonucu veya evrensel doğruluk iddiası değildir.

| Boyut | Örnek ağırlık | Ölçüm |
|---|---:|---|
| Görevi doğru tamamlama | %35 | Geçen kabul kriteri / toplam kriter |
| Test ve şemaya uyum | %20 | Başarılı testler ve invalid output oranı |
| Güvenlik / izin disiplini | %15 | Yetkisiz tool çağrıları; yüksek riskli ihlal ayrı başarısızlık |
| Maliyet | %15 | **Tamamlanan doğru görev başına** toplam tutar |
| Gecikme ve kararlılık | %10 | p50/p95 süre, 429/5xx, timeout ve yeniden deneme |
| Türkçe doğallığı / kaynak sadakati | %5 | Rubrikle değerlendirilen gerçek örnekler |

**Güvenlik kapısı:** Yetkisiz dosya erişimi, gizli veri ifşası, sahte kaynak üretimi veya izin dışı dış servis çağrısı varsa toplam ortalama puan iyi olsa bile model **geçmedi** sayılır. Güvenlik ihlalini ağırlıklı ortalamayla telafi etmeyin.

### Toplanacak veri alanları

```yaml
case_id: TR-CODING-001
volume: 2
chapter: null # Kitaptaki bölüm kesinleşince doldur
checked_at: "2026-10-11"
provider: "<provider>"
model_id: "<exact-model-id>"
model_snapshot: "<snapshot-or-unknown>"
api_endpoint: "<endpoint>"
region: "<region-or-unknown>"
reasoning_effort: "<value-or-not-supported>"
prompt_version: "v1"
fixture_revision: "<git-sha>"
input_tokens: null
cached_input_tokens: null
output_tokens: null
tool_calls: null
latency_ms: null
retry_count: null
provider_cost_usd: null
schema_valid: null
tests_passed: null
human_review: "not-reviewed"
terminal_state: "needs-review"
evidence: []
```

### Raporlama kalıbı

| Model / snapshot | n | Başarı oranı | Şema geçişi | İzin ihlali | p95 | Doğru görev başı maliyet |
|---|---:|---:|---:|---:|---:|---:|
| Denenen model A | — | **ölçülmedi** | — | — | — | — |
| Denenen model B | — | **ölçülmedi** | — | — | — | — |

Başarısız deneyler silinmez; veri kaynağı ve test komutu ile saklanır. “Daha güçlü” kararını ancak aynı iş yükündeki sonuç destekliyorsa yazarız.

## 4. Türkçe yazı testi: Doğal, açık ve tutarlı

**Yazılı metinde** Türkçenin yabancı dilden çevrilmiş gibi akmaması önemli. Bunu ölçerken yalnızca imla denetimine güvenemeyiz.

Önerilen rubrik (her ölçüt 0–4):

1. **Anlam ve kaynak sadakati:** İçerik değiştirilmedi mi, yeni iddia eklendi mi?
2. **Doğal cümle akışı:** Türkçenin söz dizimi ve ritmi yerinde mi?
3. **Gereksiz kalıp kullanımı:** “Günümüzün hızla değişen dünyasında”, tekrar eden özetler ve gösterişli ama boş sıfatlar var mı?
4. **Terim tutarlılığı:** “Ajan (agent)”, “bağlam (context)”, “istem (prompt)” aynı anlamda ve seri sözlüğüne uygun mu?
5. **Okura fayda:** Somut, öğretici ve gerektiği kadar ayrıntılı mı?
6. **Eleştirel yaklaşım:** Belirsiz bilgi kesinleştirilmiyor, kaynak ve tarih ayrımı korunuyor mu?

Değerlendirmeyi mümkünse **model adlarını gizleyerek** yapın. Bir modelin güzel cümle kurması, veri doğruluğunun yerini tutmaz. Kitap dili ve GitHub dokümantasyonu tek dilde olmalı; yapay şekilde sık tekrarlanan sloganlara dönüşmemeli.

## 5. Kod ve ajan görevleri

**Kodlama ölçümü** tek seferde üretilen satır sayısı değildir. Gerçek ölçüt: sorunu anlayıp değişikliği ne kadar küçük ve güvenli tamamladığıdır.

- Başlangıçta aynı repo commit'i ve aynı test seti sağlanır.
- Failing test doğrulanır. Model yalnızca kapsamla ilgili dosyaları değiştirir.
- Testleri silme, assertion gevşetme, tool izinlerini aşma ve secret okuma **başarısızlık** nedenidir.
- Toplam token tüketimi, araç çağrısı, modelden gelen tekrar isteği ve insan düzeltmesi sayılır.
- Son durum `done`, `blocked`, `needs-review`, `unsafe`, `budget-exceeded` ile kaydedilir (bkz. kök [AGENTS.md](../../../AGENTS.md)).
- Kullanımda ideal ölçüm **tamamlanan güvenli görev başına maliyet** ve **insan inceleme yüküdür**.

## 6. Benchmark nasıl okunmalı?

**SWE-bench Verified**, **SWE-bench Pro**, **Terminal-Bench**, **LiveCodeBench**, **Humanity's Last Exam**, **GPQA**, **MMMU**, **OSWorld**, **Toolathlon** ve **Artificial Analysis Intelligence Index** farklı şeyler ölçer. Birindeki sonuç diğerinin yerine geçmez.

Benchmark notuna şu alanları ekleyin:

| Alan | Neden gerekli? |
|---|---|
| Benchmark + sürüm / tarih | Görev seti değişmiş olabilir |
| Ölçülen model ID / snapshot | Reklam adı yeterli değildir |
| Agent harness + araç izinleri | Aynı model farklı ortamda farklı sonuç verir |
| Reasoning effort / token veya süre bütçesi | Yüksek bütçeli modelin avantajını gizlememek gerekir |
| Tek deneme mi, best-of-N mi? | Çoklu örneklem başarıyı şişirebilir |
| Dış kaynak, browsing, test geri bildirimi var mı? | Karşılaştırma koşullarını değiştirir |
| Sonuç bağımsız mı, sağlayıcının kendi deneyi mi? | Çıkar çatışması değerlendirilir |
| Veri sızıntısı / kontaminasyon notu | Eğitim ve test verisinin ayrılması gerekir |

**Kaynaklar:** [SWE-bench](https://www.swebench.com/), [SWE-bench Pro](https://scale.com/leaderboard/swe_bench_pro), [Terminal-Bench](https://www.tbench.ai/), [Artificial Analysis](https://artificialanalysis.ai/), [DORA araştırmaları](https://dora.dev/research/). Bunlar **takip kaynaklarıdır**; bu belgede bunlardan güncel puan türetilmedi.

## 7. Üretim geçiş kapıları

1. **Pilot:** Gerçek kişisel veri içermeyen temsilî görevler.
2. **Kıyas:** Eski sürüm + aday sürüm yan yana; testler ve maliyet.
3. **Gölge trafik (shadow):** Üretimi etkilemeden, veri politikası izin veriyorsa ölçüm.
4. **Kademeli açılış (canary):** Küçük pay; hata oranı, maliyet ve güvenlik alarmı.
5. **Geri alma (rollback):** Sabit model/snapshot'a dönebilen yapı.
6. **Kayıt:** Neden seçildi, hangi sürüm, kim onayladı, ne zaman yeniden test edilecek?

**Kural:** Bir modelin yeni sürümü, yapılan işin daha iyi sonuç verdiği kanıtlanana kadar yalnızca yeni bir adaydır.

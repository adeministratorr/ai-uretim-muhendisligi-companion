# Yeni yaklaşımların yerleşim kararları

Bu kayıt, iki araştırma metnindeki önerileri Pusula uygulamalarına bağlar. On iki önerinin üretim görevi, dosyası ve kabul koşulu müfredata işlendi. Bunlar öğretim tasarımıdır; koşu sonucu değildir. Çalışma adı ve isteğe bağlı laboratuvar tercihleri için yazar incelemesi beklenir.

| Öneri | Yer ve karar | Çıktı | Kabul sınırı |
|---|---|---|---|
| Ajan deneyimi (AX) | U07, U08, U18, U33; çekirdek | `evals/ax-cases.json`, `docs/ax-review.md` | Yanlış belgeyi bulan veya yazma aracı seçen aday görev başarılı olsa bile ilgili ölçütte geçmez. |
| İşlem izi ve simülasyon | U24, U30; çekirdek | `evals/trajectory-cases.json` | Tek bir doğru araç sırası dayatılmaz; aynı sonuca yetkisiz yoldan ulaşan iz reddedilir. |
| Kimlik, keşif ve yetki devri | U17, U28, U32; çekirdek | `policies/delegation.yaml` | Kayıtta bulunan ama yetkisi olmayan ajan ve süresi dolmuş devir reddedilir; taslak protokol RFC diye sunulmaz. |
| Özerklik bütçesi | U19, U20, U25; çekirdek | `policies/autonomy-budget.yaml` | Sınırlardan biri dolunca yeni dış etki başlamaz; bilinmeyen maliyet sıfır kabul edilmez. |
| Kesinti ve belirsiz dış etki | U21, U31; çekirdek | `recovery-tests.json` | Aynı işlem kimliğiyle tekrar denemede alıcıda ikinci etki oluşmaz; yerel checkpoint küresel exactly-once garantisi sayılmaz. |
| Çalışma izinden eğitim verisi | U24, U30, U35; ileri deney | `datasets/provenance.json` | Aynı kaynak/görev ailesinin türevleri eğitim ve değerlendirme tarafına sızmaz; kullanım izni bilinmeyen iz dışlanır. |
| Adım bazında model yönlendirme | U29; ileri deney | `evals/routing-comparison.json` | Yeniden deneme ve inceleme dahil toplam süre/maliyet ile kalite raporlanır; yedek rota veri sınırını genişletemez. |
| Bağlam sıkıştırma | U13, U14; çekirdek | `evals/context-results.json`, `memory-tests.json` | Özet sonrası eski revizyonun geçerli sayılması ve iptal edilmiş işin yeniden başlaması reddedilir. |
| Deneyle harness iyileştirme | U34, U35; ileri deney | `experiments/approach-comparison.json`, `experiments/ablation.json` | Saklı değerlendirme seti ayara katılmaz; yetki denetimi optimizasyon adına kaldırılmaz. |
| Gereksinimden teste izlenebilirlik | U02, U03, U04, U05, U06, U07, U11; çekirdek | `docs/traceability.md` | Var olmayan test planned kalır; kaynak revizyonu değişikliğinde etkilenen bağlar birlikte güncellenir. |
| Graf türleri | U16, U20, U23; ileri deney | `graph-design.md`, `harness-design.md`, `parallel-work.md` | Bilgi grafı kenarı yürütme yetkisi sayılmaz; eski kod grafının güncellik sınırı ve bakım maliyeti gösterilir. |
| Skill taşınabilirliği | U08, U33; çekirdek | `docs/skill-compatibility.md`, `compatibility.md` | Aynı SKILL.md dosyasının bulunması farklı ürünlerde aynı çalışma garantisi değildir; desteklenmeyen alan açık kalır. |

## Kaynakların sınırları

AX bir uygulayıcı yaklaşımıdır. Agent Registry ve AIP sürümlü Internet-Draft belgeleridir; RFC diye sunulmaz. Özerklik bütçesi yazısı IEEE standardı değildir; doğrudan sayfa erişimi 403 döndüğü için birincil URL’nin arama metniyle sınırlı incelenmiştir ve yazıdaki tarih sırası belirsizliği korunur. AgentRouter, AHE ve Graph Engineering ön baskılarının yöntemleri ve sonuçları Pusula’da yeniden üretilmedi.

Tüm kaynakların erişim sınırları [kaynak envanterindedir](../sources.json). Skill biçimi ile ürünün keşif/izin davranışı ayrı değerlendirilir. Bağlam sıkıştırma ve kalıcı yürütme belgeleri, aynı adla anılan bütün ürünlerin aynı davrandığını göstermez.

## Araştırma eklerinin tamamı

İki ekteki 121 terim ve ad [terim envanterinde](approach-inventory.json) bulunur. Terimin geçtiği ek ve satır numarası korunur. Bu sayı 121 bağımsız yöntem veya standart anlamına gelmez. Mevcut konu, yeni öneri, ürün, protokol adı ve araştırma etiketi ayrımı her kayıtta görülebilir.

Sesli ajanlar için ses akışı ve gecikme ölçümü; ajanlı ticaret için sentetik sipariş, alıcı ve ödeme simülatörü; robotik için fiziksel etkiyi sınırlayan ayrı simülasyon gerekir. Bu üç alan isteğe bağlı laboratuvar önerisidir. UCP, ACP ve AP2 adları aynı protokol kabul edilmez; özellikle ACP kısaltmasının hangi projeyi anlattığı doğrulanmadan kurulum verilmez.

Recursive self-improvement, autonomous research, model–harness co-design ve test-time search araştırma başlıkları olarak U34–U35 izleme listesine bağlandı. Sabit görev ve kabul ölçütü olmadan kendini değiştiren bir sistem, bu kitabın tekrarlanabilir Pusula deneyinin yerine konmaz.

## İlk sekiz uygulama ve mevcut kitaplar

P01’de bulunan 27 öğretim açığının 25’i ilgili promptlara açık görev ve kabul koşulu eklenerek karşılandı. Süreli GUI prototipi U11’e, harici tasarım skill’i seçimi U33’e taşındı; her ikisinin somut kabul vakası korundu. Her hedefin eski gerekçesi ve yeni prompt bağlantısı [öğrenme hedefleri kaydındaki](learning-objectives.json) `editorial_resolution` alanında bulunur. Bunların hiçbirinin gerçek deneyi yapılmış sayılmaz.

Mevcut kitaplar için 12 konu eki ve üç kaynak düzeltme adayı [kitap güncelleme önerilerindedir](book-updates.json). Konu eklerinin alt başlığı henüz seçilmediğinde `pending_inspection` yazılır. P01’de doğrulanan üç tutarsızlığın başlığı ayrıca kayıtlıdır. Kaynak kitap dosyaları değiştirilmedi.

## Uygulama sırası

U02 izlenebilirlik çizelgesini başlatır; U03–U06 kararlarla, U11 gerçek kod ve testlerle günceller. U07 AX vakalarını ve ayrı gözlem alanlarını kurar. U08 iki dar skill’i başvuru dosyası, taşınabilirlik ve skill kapalı/açık karşılaştırmasıyla genişletir. İleri yöntemler kendi uygulama grubuna gelmeden gerekli kaynak okuması ve ayrıntılı deney tasarımı tamamlanır.

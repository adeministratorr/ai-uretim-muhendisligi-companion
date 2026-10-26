# Pusula: sonraki işlerin üretim planı

> Uygulayıcı için: Planı `executing-plans` yöntemiyle, görev bazında yürüt. Aşağıdaki kutular gelecek işleri gösterir; plan dosyasının hazırlanması bu işlerin tamamlandığı anlamına gelmez.

**Hedef:** Kaynak kitapların öğrenme hedeflerini kapsayan, gerçek koşularla sınanmış ve GitHub companion dosyalarıyla birlikte okunabilen bir uygulama kitabı üretmek.

**Mimari:** Kaynak eşlemesi, öğretim şablonu, gerçek çalışma sonucu ve kitap anlatımı ayrı kaydedilir. Her uygulama grubu kabul edilmiş proje dosyalarını sonraki gruba devreder. Kitap metni, o grubun gerçek koşularından sonra yazılır; bütün ürünün bitmesi beklenmez.

**Teknoloji:** Paket denetimi mevcut Python standart kitaplığıyla sürer. Ürünün teknoloji seçimi U04'te doğrulanır; mevcut Python/FastAPI/SQLite önerisi kesinleşmiş karar değildir.

**Şartname ve dayanak:** [Başlangıç şartnamesi](../../../SPEC.md), [kitap planı](../../../KITAP_PLANI.md), [uygulama sırası](../../../UYGULAMALAR.md), [ajan uyumluluğu](../../../AJAN_UYUMLULUGU.md). Bu plan, başlangıç şartnamesinde ayrı bırakılan sonraki üretimi tanımlar; başlangıç teslimini geriye dönük olarak genişletmez.

Tarih: 26 Ekim 2026. Başlangıç revizyonu: `629718f48f20a964f45bd4ad7392c90057e1240a`. Güncel durum: P01 kaynak denetimi tamamlandı; P02 editoryal düzenlemeleri bağımsız incelemeden geçti. P03–P12 bekliyor.

## Ortak kurallar ve mevcut durum

- 36 uygulama, 108 prompt, iki skill ve altı skill vakası mevcut taslaktır. 100 kaynak bölüm eşlenmiştir; bütün öğrenme hedeflerinin karşılandığı henüz gösterilmemiştir.
- 22 araç/bileşen ve 37 birincil kaynak incelenmiştir. 11 yönerge vakası ile ürün ve model koşuları henüz çalıştırılmamıştır.
- Uygulama numaraları U01–U36 korunur. Yeni yaklaşım önce ilgili uygulamaya bağlanır; gerekçesiz yeni bölüm ve dosya eklenmez.
- Her proje çıktısı ilgili üretim promptuyla hazırlanır, kontrol promptuyla değerlendirilir ve gerekiyorsa düzeltme promptuyla yenilenir. Elle yapılan müdahale ayrıca kaydedilir; prompt tek başına üretmiş gibi anlatılmaz.
- Ortak yönerge `AGENTS.md`, ürünün rol kataloğu `agent-roles.md` olur. `design.md`, `roadmap.md` ve `tech-stack.md` görevlerine göre okunur; evrensel otomatik yükleme iddiası kurulmaz.
- Geliştiren ajan ile Pusula içindeki araştırma ajanının kimliği, bağlamı, yetkisi ve kayıtları ayrı tutulur.
- Planlanan sonuç `done` veya gözlenmiş başarı olarak yazılmaz. Koşu ve referans çıktı birbirinden ayrılır; başarısız ilk deneme düzeltmeden sonra da korunur.
- Her kitap bölümü anlam bütünlüğü, teknik doğruluk ve yönerge–örnek uyumu bakımından okunur. Mekanik üslup denetimi bu okumanın yerine geçmez.
- Companion teslimleri incelenebilir PR'lerle yapılır. Canlı kitap, site ve medya yayını mevcut yayın onayı kuralına tabidir; bu plan yayın onayı değildir.

Bu plandaki `paket` yolları `uygulama-kitabi/pusula/` dizinine göredir. `Ürün` yolları, companion kökünden ayrı açılacak Pusula çalışma dizinine göredir. `Ana kitap deposu` Yapay Zekâ serisinin mevcut kaynaklarını tutan depodur. Yeni dosya yolları aşağıda yapılacak iş olarak tanımlanır; bugün mevcut oldukları ileri sürülmez.

## Teslim sırası

| Sıra | İş | Teslim | Önkoşul |
|---|---|---|---|
| P01 | Kaynak ve öğrenme hedefi denetimi | Öğrenme hedefleri ve açık kapsam listesi | Mevcut eşleme |
| P02 | Yeni yaklaşımları yerleştirmek | 12 yaklaşımın uygulama, dosya ve kabul eşlemesi | P01'in pilot kapsamı |
| P03 | Koşu ve doğrulama düzeni | İzlenebilir kayıt biçimi ve sonuç denetimi | P02'nin pilot çıktıları |
| P04 | U01–U06 belge üretim pilotu | Gereksinimden görev listesine tutarlı proje | P03 |
| P05 | U07–U08 ajan ve skill pilotu | Yükleme, devir ve skill davranış kayıtları | P04 |
| P06 | İlk örnek kitap bölümleri | Gerçek çıktılara dayalı U01, U07 ve U08 metni | İlgili P04/P05 koşusu |
| P07 | U09–U12 prompt deneyi ve ilk ürün | Ölçülmüş promptlar ve çalışan yerel akış | P05 |
| P08 | U13–U16 bağlam, bellek ve RAG | Kaynaklı yanıt ve karşılaştırma raporu | P07 |
| P09 | U17–U21 araç, loop ve harness | İzin, bütçe ve kurtarma davranışları | P08 |
| P10 | U22–U28 ajanlar ve değerlendirme | İş bölümü, simülasyon ve birlikte çalışma | P09 |
| P11 | U29–U35 işletim ve ileri deneyler | Maliyet, sürüm, dağıtım ve yöntem karşılaştırmaları | P10 |
| P12 | U36, kitap bütünlüğü ve teslim | Tekrarlanabilir companion ve kitap taslağı | Önceki teslimler |

P01 tüm üretim boyunca güncellenir. P06'da kurulan bölüm yazım düzeni P07–P11'de tekrarlanır. Böylece kaynak denetimi ve yazım sona birikmez. P01–P03 ilk hazırlık teslimidir; P04–P06 ilk çalıştırılmış öğretim teslimidir.

## P01: Kaynakları öğrenme hedeflerine indirmek

**Dosyalar:** Pakette `editorial/source-map.json`, `editorial/learning-objectives.json`, `editorial/coverage-gaps.md` oluştur; `coverage.json` ve `KAPSAM.md` kayıtlarını denetle.

**Girdi ve çıktı ilişkisi:** Mevcut 100 bölüm kaydı ve iki araştırma metni okunur. Çıktı, her öğrenme hedefinin hangi uygulama, dosya ve kabul deneyiyle öğretileceğini gösterir.

- [x] Kanonik kitap dosyalarını belirle; mevcut eşlemedeki dosya özetiyle güncel kaynağı karşılaştır. Eski yayın veya panel kopyasını kendiliğinden kanonik sayma.
- [x] Önce U01–U08'e bağlanan bölümleri tam oku. Hedef başına `id`, `source_id`, `heading`, `objective`, `lesson_ids`, `output_paths`, `acceptance_case`, `status`, `gap_reason` alanlarını kaydet. Durumlar `mapped`, `gap` veya gerekçeli `out_of_scope` olsun.
- [x] Kalan 69 bölüm sonraki uygulama gruplarına atandı. Bu madde tam okuma tamamlandı anlamına gelmez; her grup başlamadan aynı denetim yapılacak.

**Kabul:** Pilotun öğrenme hedeflerinde belirsiz uygulama veya kabul eşlemesi kalmaz. Kalan bölümlerin durumu açıkça görünür. Gerekçeli kapsam dışı kararlar yazar incelemesine sunulur; kapsam daralması sessizce kabul edilmiş sayılmaz. `full_text_audit_complete` ancak 100 bölümün tamamı incelenince değişir.

## P02: Yeni yaklaşım önerilerini müfredata işlemek

**Dosyalar:** Pakette `editorial/approach-decisions.md` ve `editorial/book-updates.json` oluştur; `curriculum.json`, ilgili `prompts/NN.md`, `UYGULAMALAR.md`, `DOSYA_MIMARISI.md`, `YAKLASIMLAR.md` ve `sources.json` birlikte güncelle. Ana kitap deposundaki `docs/uygulama-kitabi/yeni-yaklasimlar-degerlendirmesi-2026-10-26.md` bu işin girdisidir.

- [x] Aşağıdaki yerleşimi kaynak ve P01 hedefleriyle karşılaştır; her öneriye çekirdek uygulama, ileri deney veya kapsam dışı ek kararı ve gerekçesi yaz.
- [x] Önce U01–U08'i etkileyen izlenebilirlik, ajan deneyimi ve skill taşınabilirliğini işle. Diğer önerilerin ayrıntılı deney tasarımı ilgili uygulama grubu başlamadan tamamlanacak; gerçek deneyler henüz yapılmadı.
- [x] Yeni çıktıların girdilerini ve üretim sırasını denetle; müfredat kaydı ile üç promptun aynı işi tarif ettiğini oku. Mevcut kitaplara eklenecek yerleri cilt/bölüm ve öğrenme hedefiyle kaydet; doğrulanmamış alt başlığı pending_inspection bırak.

| Yaklaşım | Uygulamalar | Somut deney veya çıktı |
|---|---|---|
| Ajan deneyimi (AX) | U07, U08, U18, U33 | `evals/ax-cases.json`: doğru belgeyi bulma, doğru araç seçme ve görevi tamamlama ayrı ölçülür |
| İşlem izi ve simülasyon | U24, U30 | Kullanıcı eksikliği, servis gecikmesi ve izin verilen alternatif araç yolları |
| Kimlik, keşif ve yetki devri | U17, U28, U32 | `policies/delegation.yaml`; keşfedilen ajan ile yetkili ajan ayrımı |
| Özerklik bütçesi | U19, U20, U25 | `policies/autonomy-budget.yaml`; çağrı, süre, maliyet ve işlem kapsamı sınırları |
| Kesinti ve belirsiz dış etki | U21, U31 | Yanıtı kaybolan işlemi tekrar etmeden sonucu uzlaştırma |
| Çalışma izinden eğitim verisi | U24, U30, U35 | `datasets/provenance.json`; kaynak ve görev ailesine göre ayrılmış veri |
| Adım bazında model yönlendirme | U29 | `evals/routing-comparison.json`; tekrarlar dahil maliyet ve kalite |
| Bağlam sıkıştırma | U13, U14 | Kaynak revizyonu, açık sorular ve yarım işlerin korunması |
| Deneyle harness iyileştirme | U34, U35 | Sabit kabul setiyle bileşen çıkarma ve geri alma karşılaştırması |
| Gereksinimden teste izlenebilirlik | U01–U07, U11 | `docs/traceability.md`; gereksinim değişikliğinin belge ve test etkisi |
| Graf türleri | U16, U20, U23 | Bilgi, yürütme ve kod bağımlılık graflarının farklı görevleri |
| Skill taşınabilirliği | U08, U33 | `docs/skill-compatibility.md`; keşif, etkinleşme ve davranış ayrı sonuçlar |

Sesli ajanlar, ajanlı ticaret, robotik ve sistemin kendi iyileştirme yöntemini değiştirmesi gibi daha geniş araştırma başlıkları da aynı karar dosyasında yer alır. Ana Pusula akışına alınmayan konu için öğretilecek hedef ve ayrı laboratuvar gereksinimi yazılır. Kaynağı doğrulanmamış tarih veya ürün iddiası kitap metnine taşınmaz.

**Kabul:** 12 önerinin her birinin yeri ve kabul koşulu bellidir. Diğer araştırma başlıkları da gerekçeli statü taşır. Dosya bağımlılıkları geçerlidir; hiçbir yeni deney sonucu gerçekleşmiş gibi yazılmaz.

## P03: Gerçek koşuların kayıt ve doğrulama düzeni

**Dosyalar:** Pakette `schemas/run.schema.json`, `runs/README.md`, `runs/index.json`, `tools/validate_runs.py`, `tests/test_validate_runs.py` oluştur; `DOGRULAMA.md` ve gerekirse `tools/validate_package.py` güncelle.

- [ ] Her koşuda kimlik, uygulama, araç/arayüz/sürüm, model, tarih, prompt revizyonu, girdi revizyonları, çıktı dosyaları, çalıştırılan kontroller, çıkış kodları, süre, gözlenebilen maliyet ve inceleme durumunu kaydet. Ölçülemeyen değeri sıfır yapma; `null` ve nedenini kullan.
- [ ] Şablonların boş gözlemlerini koru; gerçek sonuçları koşu dizinine yaz. Mevcut doğrulayıcının bütün uygulamaları `not_run` kabul eden kuralını, şablon ile gerçek koşu ayrımına göre düzenle. Bir başarı kaydı, ilişkilendirilmiş sonuç ve kabul denetimi olmadan geçerli olmasın.
- [ ] Eksik sonuç dosyası, değişmiş girdi özeti ve kabul kaydı olmadan `verified` yazılmış koşu ayrı denemelerde reddedilsin. Geçerli kayıt kabul edilsin. Yeni doğrulayıcının bu dört davranışını test et; mevcut paket kontrollerini koru.

**Kabul:** Aynı örnek yanıtın kopyaları ayrı model koşusu sayılmaz. Gerçek koşu kaynak ve prompt revizyonuna kadar izlenebilir. Sentetik ham kayıtlar paylaşılabilir; oturum kimlik bilgileri ve gerçek kişisel veri companion'a girmez. Model çağrısı ve ürün çağrısı ayrı sayılır.

## P04: U01–U06 ile belge üretim pilotu

**Dosyalar:** Üründe U01–U06'nın [çıktıları](../../../UYGULAMALAR.md); pakette `runs/` kayıtları ve `reports/pilot-u01-u06.md`. İlgili promptlar ve referans belgeler bulgulara göre güncellenir.

- [ ] Boş ürün dizinine yalnız brif ve sentetik kaynakları koy; ortamı kaydet. Kullanılabilir bir kodlama ajanıyla U01–U06'yı üretim, kontrol ve gerektiğinde düzeltme sırasıyla çalıştır.
- [ ] U04'te iki teknoloji adayını gereksinimlere göre değerlendir. Seçilen paketlerin varlığını, lisansını ve sürümünü doğrula; kurulum gereksinimini kaydet. Kararı gerçek kurulum sonucu olmadan uyumluluk kanıtı diye sunma.
- [ ] Bir gereksinimi kontrollü değiştir; tasarım, veri sözleşmesi, teknoloji kararı ve görev listesindeki etkisini izle. İlk çıktı, bulgu ve düzeltme revizyonunu sakla.

**Kabul:** Her gereksinim ilgili tasarım ve kabul kontrolüne bağlanır. İleri aşamada üretilecek belge bugünkü girdi sayılmaz. Yapılmamış görev `done` görünmez. Referans belgeyle modelin gerçek çıktısı ayırt edilebilir.

## P05: U07–U08 ile ajanlar arası devir ve skill pilotu

**Dosyalar:** Üründe U07–U08 çıktıları; pakette `reports/agent-pilot.md`, `reports/skill-pilot.md` ve araçlara göre ayrılmış koşu kayıtları.

- [ ] Ortamda kullanılabilen ana ajanla ortak `AGENTS.md`, belge haritası ve iki skill'i üret. Başka bir temiz oturumun yalnız bu dosyalardan küçük bir görevi devralmasını dene.
- [ ] Öncelikli karşılaştırma sırasını Codex, Claude Code, Qoder IDE/CLI ve ZCode olarak tut; yalnız erişilebilen araçta gerçek koşu yap. Qoder IDE ve CLI ayrı satır olsun. Diğer araçlar için belge desteği ile yerel deney durumunu ayrı göster; 22 aracın tamamını ilk teslimin koşulu yapma.
- [ ] Yedi genel yönerge vakasını seçilen aracın belgelenen davranışına göre uyarla. ZCode'da dört özel vakayı, Qoder'da kural önceliği ve alt dizin yükleme farkını uygula. İki skill'in toplam altı olumlu, ilgisiz ve eksik/yanıltıcı girdili vakasını çalıştır.

**Kabul:** En az bir araçta U07–U08 uçtan uca gözlenir. İkinci erişilebilir araçla devir deneyi kaydedilir; erişim yoksa karşılaştırma açık iş olarak kalır. Yükleme kaydı, skill'in seçilmesi ve görevin başarısı ayrı değerlendirilir. Ortak kuralın elle sürdürülen çelişkili kopyaları oluşmaz.

## P06: İlk örnek kitap bölümleri

**Dosyalar:** Pakette `manuscript/01.md`, `manuscript/07.md`, `manuscript/08.md`, `editorial/chapter-template.md` ve `editorial/review-log.md` oluştur.

- [ ] U01'in ürün tanımı, U07'nin çok araçlı yönergeleri ve U08'in skill üretimi üzerinden üç bölüm yaz. Her bölüm gerçek başlangıç dosyası, prompt, çıktı, bulgu, düzeltme ve kabul kaydını kullanır.
- [ ] Okurun her adımda neyi yapacağını ve hangi dosyayı inceleyeceğini açıkla. Başarısızlık doğal koşuda görülmediyse öğretim için eklenen hata senaryosunu kontrollü deney olarak etiketle.
- [ ] Türkçe anlam ve teknik sadakat okumasını yap; mekanik üslup bulgularını ayrı kaydet. Yazar incelemesine üç bölüm ve bağlı dosyalarla tek paket sun.

**Kabul:** Üç bölümde yönerge ile örnek aynı işi gösterir. Sonuç cümleleri mevcut kayda dayanır. Yazarın inceleme durumu açık kalır; bekleyen üslup kararı bağımsız teknik denemeleri durdurmaz, geniş metin üretiminden önce ele alınır.

## P07: U09–U12 ile prompt deneyi ve çalışan ürün

**Dosyalar:** Üründe U09–U12 çıktıları; pakette `reports/prompt-pilot.md`, `reports/product-pilot.md`, ilgili koşular ve bölüm metinleri.

- [ ] U09–U10 için kaynak ve soru setini sabitle; üç prompt varyantını geliştirme ve ayrılmış değerlendirme girdileriyle karşılaştır. Çalıştırma bütçesi ve model erişimi netleşmiş koşuları yap; yapı, kaynak desteği, çekilme, süre ve maliyeti ayrı kaydet.
- [ ] U11'de belge ekleme → soru → kaynaklı taslak → insan incelemesi akışını önce sabit öğretim yanıtıyla çalıştır. Normal, boş, bozuk, çelişkili ve eski kaynak girdilerini kabul koşullarıyla sınayıp tarayıcı gözlemini sakla.
- [ ] U12'de görülen bir hatanın yeniden üretimi, düzeltmesi ve Git geri dönüşünü belgele. Model değerlendirmesi ve sabit yanıtlı ürün çalışmasını ayrı raporla.

**Kabul:** Temiz dizinden kurulum ve ilk akış tekrarlanabilir. Öğretim yanıtı ekranda örnek olarak görünür. U10 modeli çalıştırılmadıysa prompt karşılaştırması tamamlandı sayılmaz; model çağrısız ürün işi kendi kabul koşuluyla ilerleyebilir.

## P08: U13–U16 ile bağlam, bellek ve kaynaklı yanıt

**Dosyalar:** Üründe U13–U16 çıktıları ve P02'de tanımlanan sıkıştırma/graf vakaları; pakette `reports/context-retrieval.md` ve ilgili bölümler.

- [ ] Ürüne gerçek model bağlantısını kayıtlı erişim ve bütçeyle ekle; sabit öğretim yanıtından ayrıldığını göster. Bu geçişin üretim adımını ve kabulünü ilgili prompta açıkça işle.
- [ ] Bağlam seçimi, sıkıştırma ve bellekte güncel kaynak revizyonunun, açık sorunun ve yarım işin korunmasını karşılaştır. Eski bellekle yanlış sonuca gidilen olumsuz vakayı kullan.
- [ ] Kaynak getirme ve graf ekleme deneyini aynı görev setinde daha basit başlangıç çözümüyle karşılaştır; getirilmeyen kaynakla atıf üretme ve cevabı olmayan soruda çekilme davranışını sınayarak kaydet.

**Kabul:** Ürün yanıtındaki iddia kaynak revizyonuna bağlanır. Graf veya bellek yalnız ölçülen katkısıyla gerekçelendirilir; gereksiz bileşen kaldırılabilir.

## P09: U17–U21 ile araç, loop ve harness

**Dosyalar:** Üründe U17–U21 çıktıları, `policies/delegation.yaml`, `policies/autonomy-budget.yaml` ve arıza vakaları; pakette `reports/harness-recovery.md`.

- [ ] Araç sözleşmesi, MCP erişimi, ajan kimliği ve yetki kapsamını aynı görevde birleştir. İzin reddini yalnız metin yönergesinde bırakma; yürütme noktasında denetle.
- [ ] Loop'un başarı, bilgi eksikliği, iptal, bütçe dolması ve tekrar sınırı sonuçlarını sınayıp durma nedenlerini kaydet. Zaman ve işlem bütçesinin gerçek sayaçla uygulandığını göster.
- [ ] Görevi ayrı süreçte kesip kaydedilmiş durumdan sürdür. Sentetik dış işlemde kayıp yanıt, tekrarlı istek ve beklerken iptal edilmiş yetkiyi dene; belirsiz işlem sonucunu körlemesine tekrar etme.

**Kabul:** Yan etki, yetki ve bütçe denetimleri çalışma kaydında görünür. Kurtarma güncel kaynak ve yetkiyi yeniden kontrol eder. Yerel tekrar güvenliği ağda tam bir kez teslim garantisi olarak anlatılmaz.

## P10: U22–U28 ile iş bölümü ve değerlendirme

**Dosyalar:** Üründe U22–U28 çıktıları, simüle kullanıcılar ve araç arızaları; pakette `reports/agent-evaluation.md`.

- [ ] Tek ajan ile rol ayrılmış ajanları aynı kabul seti ve toplam bütçeyle karşılaştır. P09 bütçesini çalışanlar arasında ortaklaştır; devirde girdi, çıktı, yetki ve başarısızlık sorumluluğunu sınayarak kaydet.
- [ ] U24 değerlendirmesini nihai yanıtla birlikte işlem izini kapsayacak şekilde kur. Eksik bilgi, gecikme, çelişkili kaynak ve birden fazla geçerli araç sırası için senaryolar çalıştır. U25 güvenlik vakalarını bu sonuçlarla ilişkilendir.
- [ ] Çok kipli girdi, tarayıcı, olay/zaman otomasyonu ve A2A örneklerini kontrollü ortamda ekle. İçerikten gelen talimat ile kullanıcı yetkisini ayır; otomasyonun iptal ve yinelenen olay davranışını sınayarak kaydet.

**Kabul:** Çoklu ajan katkısı varsa ölçümle görünür; yoksa sonuç açıkça yazılır. Doğru yanıtla birlikte yapılan yetkisiz işlem başarısız sayılır. Değerlendirme ilk kez burada başlamaz; önceki uygulamaların kabul kayıtlarını genişletir.

## P11: U29–U35 ile işletim ve ileri deneyler

**Dosyalar:** Üründe U29–U35 çıktıları, yönlendirme karşılaştırması, veri kökeni ve harness deneyleri; pakette `reports/operations-experiments.md`.

- [ ] Model yönlendirmeyi tek modelle karşılaştır; tekrar, gecikme ve toplam maliyeti dahil et. İzleme, kapasite, sürüm değişikliği, dağıtım ve geri alma provasını kontrollü ortamda tamamla.
- [ ] Takım sahipliği, lisanslar, veri yaşam döngüsü ve skill dağıtımını belgeleyip temiz kurulumda kontrol et. U07–U08 pilotundaki açık araç karşılaştırmalarını erişim durumuna göre genişlet.
- [ ] İncelenmiş işlem izlerinden veri seti hazırla; görev ailesine göre eğitim/değerlendirme ayrımını koru. Veri hazırlamayı model eğitimi başarısı sayma. U34–U35'te bileşen ekleme/çıkarma deneylerini sabit kabul setiyle yap; başarısız adayı geri al.

**Kabul:** Maliyet ve kalite aynı görevler üzerinden değerlendirilir. Veri kökeni açıktır. Deney yapan ajan kabul ölçütünü veya izin sınırını değiştirerek başarı üretemez. Araştırma iddiaları ile Pusula'da gözlenen sonuçlar ayrı yazılır.

## P12: Kitap bütünlüğü, mevcut kitap ekleri ve GitHub teslimi

**Dosyalar:** Üründe U36 çıktıları; pakette `manuscript/`, `editorial/review-log.md`, `editorial/book-updates.json`, `release-manifest.json` ve güncel kapsam çizelgesi. Companion kökünde `.github/workflows/pusula-checks.yml` oluşturulur. Ana kitap deposunda yalnız eşleme kaydında belirlenmiş bölüm kaynakları değiştirilir.

- [ ] Her uygulama grubu kabul edildikçe ilgili bölümü yaz ve mevcut kitap ekini hazırla. Cilt 1'de kısa kavram açıklaması; Cilt 2'de belge/prompt/skill; Cilt 3'te ajan/harness/evals; Cilt 4'te işletim/yönetişim; Claude rehberinde kendi araca özgü karşılıkları düzenle. Mevcut anlatımı gereksiz tekrarlarla büyütme.
- [ ] 100 bölümün hedeflerini son kez karşılaştır; açık veya kapsam dışı hedefleri yazarın görebileceği listede tut. Her U01–U36 için başlangıç, çözüm, çalıştırma kaydı ve kullanılan kaynak revizyonunu gerçek commit kimlikleriyle sürüm manifestine bağla.
- [ ] Temiz çalışma dizininde kurulum ve seçilmiş uçtan uca akışları yeniden çalıştır. Bölüm metinlerini baştan sona oku; dosya adlarını, promptları, ekranları ve çıktıları karşılaştır. Kitap taslağı ve companion sürümünü birlikte incelemeye sun.
- [ ] GitHub kontrolünü paket/koşu doğrulaması ve model çağrısız ürün testleriyle çalıştır. Gerçek model deneylerini ayrı, bütçesi belirlenmiş çalıştırmalar olarak tut; dış katkıdan gelen PR'nin kendiliğinden ücretli çağrı başlatmasını önle.

**Kabul:** Okur belirtilen başlangıç revizyonundan ilgili uygulamayı tekrar edebilir. Çözümlenmemiş öğrenme hedefi varken “bütün içerik uygulandı” denmez. Yayın onayı verilince sürüm etiketleri, kitap bağlantıları ve gerekiyorsa yayın çıktıları aynı revizyona bağlanır.

## İlk çalışma oturumunun kesin sırası

1. P01 için kaynak haritasını ve U01–U08 hedeflerini çıkar.
2. P02 için 12 yaklaşımın yerini kaydet; pilot promptlarına izlenebilirlik, AX ve skill taşınabilirliğini işle.
3. P03 için koşu sözleşmesini, gerçek sonuç denetimini ve olumsuz kayıt denemelerini tamamla.
4. Bu hazırlık teslimini ayrı commit ile incelemeye aç; ardından P04'te U01'i çalıştır.

İlk gerçek koşuların süre, düzeltme sayısı ve giderleri oluşmadan bütün kitaba takvim veya maliyet sözü verilmez. Pilot raporu sonraki grupların iş tahminini günceller.

## Deneme araçları ve gider kararı

Kitap örnekleri API veya mevcut abonelik seçeneklerini gösterebilir. Bu projenin gerçek denemelerinde yalnız mevcut abonelikler kullanılacak; ayrıca ücretlenen API çağrısı yapılmayacak. Abonelikte gözlenmeyen gider `null` ve gerekçeyle kaydedilecek; teorik API eşdeğeri gerçek fatura sayılmayacak.

Antigravity öncelikli araçtır. OpenCode, kullanıcının bildirdiği IP sınırı nedeniyle beklemededir; yeniden deneme yapılmaz. Antigravity ile bağımsız kaynak incelemesi tamamlandı, fakat etkileşimsiz düzenleme denemesi komut onayı sınırında dosya değiştirmeden durdu. Bu iki editoryal çalışma U01–U36 pilot koşularına dahil edilmez. 26 Ekim 2026 tarihli son Antigravity çağrısı da kota sınırı (429) nedeniyle başlamadı; araç yaklaşık 4,5 saatlik yenilenme süresi bildirdi. Bu nedenle geliştirme ve gerçek model deneyleri sonraya alındı. Kitap ve prompt hazırlığı tamamlanan editoryal kapsamıyla korunur; başarısız çağrı çalışma sonucu sayılmaz. Codex/Claude yedek seçeneklerdir; ücretli API'ye sessiz geçiş yapılmaz.

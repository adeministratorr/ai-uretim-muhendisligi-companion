# Kaynak ve öğrenme hedefi denetimi

Bu dizin P01'in kanonik editoryal kayıtlarını tutar. `mapped`, bir hedefin uygulama, hedef dosya ve önerilen kabul vakasıyla eşlendiğini söyler; üretim veya öğrenme başarısını göstermez. Bütün runtime sonuçları `not_run`, gözlemler `null`dır. Sentetik vakalar gerçek ürün koşusu değildir.

- [source-map.json](source-map.json): 100 kanonik kaynağın depo kimliği, yolu, başlangıç/güncel SHA-256 değeri, kanonik gerekçesi, okuma durumu ve denetim grubu.
- [pilot-reading-log.json](pilot-reading-log.json): Tam okunan 31 pilot kaynağın satır kapsamı ve başlıklarının pilot/ileri/bağlam kararları. Başlık kararları yalnız bu kayıtta tutulur.
- [learning-objectives.json](learning-objectives.json): Hedef cümlesi, kaynak başlığı, uygulama, göreli ürün çıktısı, kabul kimliği ve açık gerekçe.
- [pilot-acceptance-cases.json](pilot-acceptance-cases.json): Hedef kimliğine bağlı sentetik olumlu/olumsuz adaylar ve beklenen karar. Uygulama ve çıktı ilişkisi hedef kaydından okunur; burada tekrarlanmaz. Adındaki pilot, kaynak seçkisini belirtir; ileri uygulamalara ayrılan vakalar da açıkça işaretlenir.
- [coverage-gaps.md](coverage-gaps.md): Pilot/ileri öğretim açıkları ve tam okuma bekleyen 69 kaynağın sırası.
- [source-issues.json](source-issues.json): Yazar incelemesine ayrılan kaynak tutarsızlıkları. Kaynak kitap dosyaları değiştirilmedi.

`gap`, kaynağın hedefinin henüz yeterli öğretim veya kabul tasarımına sahip olmadığını belirtir. Önerilen uygulama/dosya açığın nereye taşınacağını gösterir; açığı kapatmaz. `needs_design` olan ileri vakalar o grup başlamadan somutlaştırılmalıdır. Kapsam dışı karar alınmadı; gerekirse yazar incelemesine sunulmalıdır.

## Doğrulama

Companion içindeki `uygulama-kitabi/pusula/` dizininden çalıştırın. Yer tutucuları kanonik kaynak depolarının kökleriyle değiştirin; yerel kökler kayıtlara yazılmaz.

```sh
python3 editorial/validate_source_audit.py \
  --books-root '<engineering-book checkout>' \
  --guide-root '<claude-guide checkout>'
python3 tools/validate_package.py
```

İlk komut 100 gerçek kaynak dosyasını yeniden okuyup güncel hash, bayt ve satır sayılarını denetler. Pilot 31 bölümün gerçek Markdown başlıklarını kod blokları ve HTML yorumları dışından çıkarır; okuma kaydının ana başlık kapsamını ve bütün hedeflerin başlık ilişkisini kontrol eder. Kimlikler, başlangıç hashlerinin korunması, hedef/vaka/uygulama/çıktı ilişkileri ve runtime sınırları da denetlenir. Kaynak revizyonu değiştiyse durur; otomatik güncelleme yapmaz. Git HEAD, envanterin alındığı checkout kimliğidir; çalışma ağacının temiz olduğu iddiası değildir.

İkinci komut mevcut paket yapısını denetler. Bu kontroller okuma beyanını veya anlamsal kararı otomatik kanıtlamaz; metnin okur gözüyle okunmasının ve bağımsız incelemenin yerine geçmez.

## Köken ve editör müdahalesi

İlk P01 commitinde bulunan ara okuyucu raporları, override girdileri ve birleştirme betiği Git geçmişinde korunur; yerel kopyaları sürüm dışı `.superpowers` scratch arşivine taşındı. Bunlar public paketin ikinci doğruluk kaynağı değildir. Eski birleştirme betiği paketten kaldırıldığı için ilerideki P02 kararları onunla yeniden üretilip ezilemez.

Hedefe özgü kabul adaylarının somutlaştırılması ve uygulama/çıktı ilişkilerinin düzeltilmesi gibi elle verilen kararlar, kanonik hedeflerin `editorial_intervention` alanlarında görünürdür. Kanonik hedef/vaka ayrımı korunur; ara raporların aynı içeriği yeniden yayımlanmaz. Hiçbiri üretim promptunun tek başına gözlenmiş başarısı olarak sunulmaz.

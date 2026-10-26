# Kaynak ve öğrenme hedefi denetimi

Bu dizin P01'in editoryal kaydını tutar. `mapped`, hedefin bir uygulama, hedef dosya ve önerilen kabul vakasıyla eşlendiğini söyler. Dosyanın üretildiğini, modelin çalıştığını veya okurun hedefi öğrendiğini göstermez. Bütün çalışma sonuçları `not_run`, gözlemler `null` kalır. Sentetik vakalar gerçek ürün koşusu değildir.

- [source-map.json](source-map.json): 100 kanonik kaynak, önceki/güncel SHA-256, depo kimliği, bütün Markdown başlıkları ve denetim grubu.
- [pilot-reading-log.json](pilot-reading-log.json): Gerçek tam okuma beyanları, satır aralıkları ve başlıkların pilot/ileri/bağlam ayrımı. Başlık çıkarmak tam okuma sayılmaz.
- [learning-objectives.json](learning-objectives.json): Kısa hedef cümlesi, uygulama ve göreli ürün çıktısı, kabul kimliği, durum ve açık gerekçe.
- [pilot-acceptance-cases.json](pilot-acceptance-cases.json): Olumlu ve olumsuz sentetik adaylar ile beklenen karar. Adındaki `pilot`, kaynak seçkisini belirtir; bu bölümlerden ileriki uygulamalara ayrılan vakalar da açıkça işaretlenir.
- [coverage-gaps.md](coverage-gaps.md): Öğretim ve kabul tasarımı açıkları; henüz okunmayan 69 kaynak için sıradaki gruplar.
- [source-issues.json](source-issues.json): Yazar incelemesine gönderilecek kaynak tutarsızlıkları. Kaynak kitap dosyaları değiştirilmedi.
- `local-reader.json` ve `readings/`: Okuma araştırmacılarının önerileri. Bunlar birleşik kaydın yerine geçmez.
- [acceptance-overrides.json](acceptance-overrides.json): Birleştiren editörün somutlaştırdığı vakalar ve düzelttiği uygulama/çıktı ilişkileri. Elle eklenen bu kararlar otomatik prompt çıktısı gibi sunulmaz.

`gap`, kaynakta bulunan hedefin henüz yeterli öğretim veya kabul tasarımına sahip olmadığını belirtir. Önerilen uygulama/dosya, açığın nereye taşınacağını gösterir; açığı kapatmaz. `needs_design` işaretli ileri kabul taslakları o uygulama grubu başlamadan somut girdiye ve karara dönüştürülmelidir. Bu denetimde kapsam dışı karar alınmadı. Böyle bir karar gerekirse yazar incelemesine sunulmalıdır.

## Yeniden üretme ve denetleme

Companion içindeki `uygulama-kitabi/pusula/` dizininden çalıştırın. Yer tutucuları kanonik kaynak depolarının kökleriyle değiştirin; bu yerel kökler çıktı JSON'una yazılmaz.

```sh
python3 editorial/build_source_audit.py \
  --engineering '<engineering-book checkout>' \
  --claude '<claude-guide checkout>' \
  --reader editorial/local-reader.json \
  --reader editorial/readings/c2-early.json \
  --reader editorial/readings/c2-c4.json \
  --reader editorial/readings/claude-early.json \
  --reader editorial/readings/claude-skills.json \
  --overrides editorial/acceptance-overrides.json
python3 editorial/validate_source_audit.py
python3 tools/validate_package.py
```

Üretici kaynak SHA'sı ile okuma raporunun SHA'sı uyuşmazsa durur. Eski `coverage.json.sha256` değerini değiştirmez; güncel revizyonu ayrıca kaydeder. Başlık envanteri kod bloklarındaki örnek başlıkları ve HTML yorumlarını gerçek bölüm başlığı saymaz. Kanonik depolardaki güncel dosya baytları esas alınır; Git HEAD bilgisi çalışma ağacının temiz olduğu iddiası değildir.

İkinci komut kimlik, yol, hedef/vaka bağı, okunan satır kapsamı, başlık ayrımı ve sonuç durumunu denetler. Okuma beyanının doğruluğunu veya anlam değerlendirmesini otomatik kanıtlayamaz. Son komut mevcut paket yapısını denetler. Bu iki mekanik kontrol, bölümün okur gözüyle okunmasının ve bağımsız incelemenin yerine geçmez.

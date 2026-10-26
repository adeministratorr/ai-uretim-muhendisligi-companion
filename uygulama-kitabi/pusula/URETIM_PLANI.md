# Pusula kitap ve uygulama üretim planı

**Hedef:** Birbirine bağlı uygulamalarla kitap kaynaklarını çalışan ve doğrulanmış Pusula projesine dönüştürmek.
**Mimari:** Kitap anlatımı, kopyalanabilir prompt, referans çıktı ve çalıştırma kanıtı ayrı tutulur. Her uygulama önceki uygulamanın kabul edilmiş çıktısını kullanır.
**Teknoloji:** İlk paketin denetimi Python 3 standart kitaplığıyla yapılır. Uygulama teknoloji kararı U04'te resmî kaynak ve sürüm kaydıyla verilir.
**Şartname:** [SPEC.md](SPEC.md).

## Aşama 1: Kitap iskeleti ve başlangıç paketi

- [x] Farklı örnek proje, uygulama sırası ve dosya bağımlılıkları yazıldı.
- [x] 36 uygulama için üretim, kontrol ve düzeltme promptları hazırlandı.
- [x] 100 kaynak bölüm için bölüm düzeyinde eşleme çıkarıldı.
- [x] Örnek belge, skill ve sentetik veri paketi hazırlandı.
- [ ] Yazarın kapsam ve proje adı incelemesi tamamlandı.

## Aşama 2: İlk uygulamaların gerçek koşuları

- [ ] U01–U08 boş bir uygulama dizininde sırayla çalıştırılır.
- [ ] Her koşunun promptu, girdi özeti, model/araç bilgisi, ham çıktısı ve doğrulama kaydı saklanır.
- [ ] Referans belgeler gerçek çıktılarla karşılaştırılır; başarısız örnekler düzeltme dersine dönüştürülür.
- [ ] Skill seçimi ve davranışı olumlu, ilgisiz ve eksik girdili vakalarda gözlenir.

## Aşama 3: İlk çalışan Pusula

- [ ] U09–U12 ile model çağrısız uygulama ve kabul testleri hazırlanır.
- [ ] Gerçek model bağlantısı için ayrı yetki, bütçe ve kayıt düzeni kurulur.
- [ ] Aynı görevin sabit öğretim yanıtı ve gerçek model koşusu ayrı raporlanır.
- [ ] Boş, hatalı, çelişkili ve eski kaynak senaryoları tarayıcıda doğrulanır.

## Aşama 4: Ajan ve işletim uygulamaları

- [ ] U13–U33, bağımlılık sırasına göre ayrı teslimlerle yürütülür.
- [ ] Her uygulamaya başlangıç ve çözüm sürümü eklenir; yalnız doğrulanmış commit kimlikleri kullanılır.
- [ ] Normal sonuç kadar iptal, kesinti, ret ve belirsiz dış etki de sınanır.
- [ ] Dış hizmet veya yeni paket kurulumu gerektiğinde kapsam ve gerçek maliyet kaydı korunur.

## Aşama 5: Yeni yaklaşımlar ve kitap yazımı

- [ ] U34–U36 için sürümlü kaynak incelemesi ve karşılaştırmalar tamamlanır.
- [ ] Kaynakların tam metni okunur; alt başlık, hedef ve örnek düzeyindeki kapsam boşlukları kapatılır.
- [ ] Her uygulama, gerçek koşu kayıtlarından yürüyen kitap bölümüne dönüştürülür.
- [ ] Türkçe anlam, teknik doğruluk, öğretim sırası ve dosya uyumu birlikte denetlenir.
- [ ] Son kitap ve uygulama paketi yazar incelemesine sunulur; yayın ayrıca kararlaştırılır.

Her aşama bağımsız incelenebilir bir teslimle kapanır. Sonraki aşamanın planlanmış olması öncekinin başarısını göstermez. Bu dosyada işaretlenen tamamlanma yalnız başlangıç paketindeki dosya üretimidir.

# Doğrulama kapsamı

Bu başlangıç paketinin doğrulayıcısı dosya ve kayıt ilişkilerini inceler. Uygulama sayısını, kaynak bölüm kimliklerini, ders bağımlılıklarını, prompt yollarını, JSON biçimini, skill girişlerini ve paket içi Markdown bağlantılarını denetler. Model, ağ veya ürün çağrısı yapmaz.

```sh
python3 uygulama-kitabi/pusula/tools/validate_package.py
```

Beklenen çıktı 36 uygulama, 100 kaynak bölüm, iki skill, altı skill vakası ve 14 birincil kaynak kaydıdır. Bunlar içerik envanterinin sayılarıdır; model başarısı veya çalışan özellik sayısı değildir. Araç Python 3.9 ve üzerindeki standart kitaplıkla yazılmıştır; kullanılan ortam ve gözlenen sonuç `validation-result.json` dosyasına kaydedilir.

Doğrulayıcının bir kusuru reddetmesi de kontrol edilir. Paketin geçici kopyasında bir bölüm eşlemesi kaldırılır, başka bir kopyada ilk uygulamaya henüz üretilmemiş girdi eklenir, üçüncü kopyada yerel bağlantı bozulur. Her kopyanın reddedilmesi beklenir. Asıl paket bu denemeler için değiştirilmez.

Promptların tamamı `not_run`, skill vakalarının gözlemleri `null` durumundadır. Referans belgeler öğretim için hazırlanmış çıktılardır. Model karşılaştırması, temiz makinede kurulum, tarayıcı kabulü, gerçek insan incelemesi ve ürünün üretime hazır olması bu denetimin dışındadır.

Kitabın anlam bütünlüğü dosya doğrulayıcısıyla ölçülmez. Okur, neyi yapacağını, hangi dosyayı üreteceğini ve hangi sonucu kabul edeceğini metinden çıkarabilmelidir. Tam kitap bölümleri yazılırken bu okuma her bölüm için yeniden yapılır.

# Skill örnekleri

Paket içindeki iki skill, kitapta üretilecek yöntemin başlangıç örneğidir. Etkin skill dizinine kurulmadı; model seçimi ve davranış testi yapılmadı.

- [pusula-belge-uret](skills/pusula-belge-uret/SKILL.md): Bir proje belgesini mevcut kararları koruyarak üretir veya günceller.
- [pusula-kaynak-denetle](skills/pusula-kaynak-denetle/SKILL.md): İddia, alıntı ve kaynak revizyonu ilişkisini inceler.

U08'de bu paketleri okuyup kendi uygulamanız için yeniden üretin. Kurulum yolunu kullandığınız aracın güncel belgesinden doğrulayın. Claude Code için ürün belgesi [kaynak listesinde](YAKLASIMLAR.md) bulunur. Başka araca kopyalamak davranış uyumluluğunu kanıtlamaz.

Deneme istekleri [skill-tests.json](skill-tests.json) dosyasındadır. Her isteği temiz görev bağlamında yürütün; seçilen skill'i, gözlenen eylemi ve çıktıyı kaydedin. Olumlu çağrı kadar ilgisiz istek ve eksik girdi de incelenir. Gözlem yapılana kadar observed alanı null kalır.

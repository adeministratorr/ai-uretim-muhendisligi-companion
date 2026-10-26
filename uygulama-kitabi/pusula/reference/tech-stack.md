# Teknoloji kararı örneği

Durum: aday tasarım; paket kurulumu ve sürüm uyumluluğu henüz sınanmadı.

İlk öğretim adayı Python tabanlı bir sunucu, FastAPI, sunucuda üretilen HTML ve SQLite'tır. Bu aday küçük yerel akışta ayrı ön yüz uygulaması kurma yükünü azaltma amacıyla seçilmiştir. Bu gerekçe bir performans ölçümü değildir. TypeScript tabanlı tek dil yaklaşımı U04'te aynı ihtiyaçlara göre karşılaştırılacaktır.

Paket adı, lisans ve sürüm U04 sırasında resmî belge ve registry üzerinden doğrulanır. Doğrulanmadan bağımlılık manifesti ve kurulum komutu üretilmez. Kullanılan Python sürümü, işletim sistemi, kilit dosyası ve test sonucu ortam kaydına yazılır.

İlk akış model çağrısız çalışır. Gerçek model daha sonra ayrı bir bağlantı bileşeniyle eklenir. Girdi/çıktı sözleşmesi korunarak sağlayıcı değişimi sınanır. PostgreSQL, kuyruk ve dağıtık hizmetler yalnız ilgili ileri uygulamanın ihtiyacı ve kabul deneyiyle eklenir.

# Güvenlik ve Kalite Kapıları

Bu depodaki her örnek, final hâline gelmeden önce aşağıdaki kontrollerden geçer.

## Kalite Kapıları

- Komutlar yıkıcı işlem yapıyor mu?
- `.env`, API key veya kişisel veri sızıntısı var mı?
- Testler çalışıyor mu?
- Kod örneği kitabın bölüm hedefiyle eşleşiyor mu?
- Agent talimatları dosya silme, test zayıflatma veya secret okuma gibi riskleri engelliyor mu?
- JSON/schema örnekleri doğrulanıyor mu?
- Web bağlantısı, bölüm slug'ı ve companion link doğru mu?
- Yeni bağımlılık registry'de doğrulandı ve sürümü sabitlendi mi? (dependency hallucination / slopsquatting koruması)

## Gizli Veri ve Secret Politikası

- Gerçek API key, token, cookie veya kişisel veri bu depoya **asla** eklenmez.
- Örnek değerler açıkça placeholder olarak yazılır: `EXAMPLE_API_KEY`, `example@example.com`.
- `.env` dosyaları `.gitignore` ile takip dışı bırakılır.

## Güvenlik Açığı Bildirimi

Bu depoda bir güvenlik açığı (secret sızıntısı, zararlı bağımlılık, prompt injection
riski taşıyan örnek vb.) fark ederseniz, GitHub Issues yerine depo sahibine doğrudan
bildirin (bkz. kitap/web sitesindeki iletişim bilgisi).

## Agent Güvenlik Sınırları

Bu repoda çalışan coding agent'lar için tam kural listesi `AGENTS.md` dosyasındadır.
Özet: agent secret okuyamaz/yazamaz, kullanıcı onayı olmadan yıkıcı işlem yapamaz, test
veya assertion zayıflatamaz, production/canlı servise dokunamaz.

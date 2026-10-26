# Kitap planı

Çalışma başlığı: **Yapay Zekâ ile Üretim Atölyesi**.
Alt başlık: **Promptlardan Proje Dosyalarına, Skill’lerden Çalışan Ajan Sistemlerine**.
Tarih: 26 Ekim 2026. Durum: editoryal taslak.

## Kitabın amacı

Okur bir ihtiyacı tanımlayarak başlayacak; proje belgelerini, uygulama kodunu, testleri, skill paketlerini ve işletim dosyalarını promptlarla üretecek. Her yeni çıktı bir sonraki uygulamanın girdisi olacak. Dosyanın hangi soruyu çözdüğü, ne zaman güncelleneceği ve hangi sonuçla kabul edileceği açıklanacak.

Pusula adlı kaynaklı araştırma ve karar uygulaması kitap boyunca büyüyecek. İlk bölümdeki atölye programı seçimi, ileride çelişkili kaynak, eski bellek, yetkisiz araç çağrısı ve kesintiden devam deneylerine dönüşecek. Günlük yazışma, öğrenme, sunum ve veri analizi alıştırmaları da aynı araştırma dosyasının farklı çıktıları üzerinden işlenecek.

## Kısımlar

| Kısım | Uygulamalar | Okurun tamamlayacağı iş |
|---|---|---|
| I. Fikirden proje sözleşmesine | 01–07 | Vizyon, gereksinim, tasarım, teknoloji kararı, veri sözleşmesi, yol haritası ve ajan yönergeleri |
| II. Prompt ve skill atölyesi | 08–10 | Tekrarlanan yöntemlerin paketlenmesi, prompt karşılaştırması ve çıktı değerlendirmesi |
| III. Çalışan ürün ve bağlam | 11–16 | İlk uygulama, hata ayıklama, bağlam seçimi, bellek, RAG ve graf karşılaştırması |
| IV. Araç, loop ve harness | 17–21 | Yetkili araçlar, MCP, durma kuralları, çalışma çatısı ve kalıcı görev durumu |
| V. İş bölümü ve değerlendirme | 22–26 | Alt ajanlar, çoklu ajan karşılaştırması, evals, güvenlik ve çok kipli kullanım |
| VI. Otomasyon ve üretim | 27–33 | Olaylar, A2A, ajanlara açık web, model geçidi, izleme, dağıtım ve ekip paketi |
| VII. Yeni yaklaşımlar ve devir | 34–36 | Yöntem karşılaştırması, sürüm değişikliği, gereksiz katmanları çıkarma ve proje teslimi |

## Ajan araçları arasında taşınabilir proje

U07 ortak proje kurallarını AGENTS.md içinde üretir. Okur kullandığı ajan aracının, arayüzünün ve sürümünün bu dosyayı nasıl yüklediğini inceler. Gereken yerde CLAUDE.md, GEMINI.md, Copilot yönergesi veya Cursor kuralı gibi bir uyarlama ekler. Ortak kararlar tek yerde tutulur; yükleme, dosya kapsamı ve çelişki davranışı küçük görevlerle sınanır. Model seçimiyle ajan aracının dosya keşfi ayrı öğretilir.

[Ajan uyumluluğu rehberi](AJAN_UYUMLULUGU.md) ZCode ve Qoder dahil 22 araç veya araç bileşeni için belgeye dayalı eşlemeyi içerir. Bu eşleme yerel araç denemelerinin yerini tutmaz. Kitap bütün araçları kurmayı veya her araca ayrı bir ortak kural kopyası yazmayı gerektirmez.

## Her uygulamanın anlatımı

Bölüm önce Pusula kullanıcısının karşılaştığı somut sorunu anlatır. Okur başlangıç dosyalarını açar, neyi değiştireceğini öğrenir ve üretim promptunu uygular. Ardından çıkan dosyaları kabul ölçütüyle karşılaştırır. Bir hata örneği üzerinde düzeltme promptu kullanır ve sonucun neden kabul edildiğini kaydeder.

Dosya biçimini doğrulamak, içeriğin doğru olduğunu göstermeye yetmez. Örneğin kaynaklı cevap JSON'u şemaya uyduğu hâlde alıntının söylemediği bir sonucu ileri sürebilir. Bu yüzden çalışma; yapı kontrolünü, anlam kontrolünü ve yetki kontrolünü ayrı sonuçlarla tamamlar.

## İki çalışma çatısı

Kitap, uygulamayı geliştiren kodlama ajanının çalışma düzenini ve Pusula ürününün içinde çalışan araştırma ajanının çalışma çatısını ayrı gösterir. İlki PRD, Git, test, inceleme ve görev devriyle ilgilidir. İkincisi kullanıcı sorusu, kaynak getirme, araç çağrısı, kalıcı durum ve taslak teslimiyle ilgilidir. Ortak kavramları vardır; izinleri, durum depoları ve kabul koşulları aynı değildir.

Prompt engineering görev talimatını; context engineering o görev sırasında modele verilecek bilgiyi; loop engineering çevrim, geri bildirim ve durma kurallarını; harness engineering modelin çevresindeki yürütme, araç, durum ve doğrulama düzenini ele alır. Bu ayrım kitabın öğretim düzenidir. Loop engineering için tek bir evrensel ürün standardı iddiası kurulmaz.

## Kaynak kitaplarla ilişki

Serinin 60 bölümü ve Claude Code rehberinin 40 bölümü [kapsam çizelgesinde](KAPSAM.md) uygulamalara bağlanmıştır. Eşleme bölüm düzeyinde hazırlanmıştır. Alt başlık ve öğrenme hedeflerinin tamamının karşılandığını henüz kanıtlamaz. Kitap yazılırken her bölümün tam metni yeniden okunacak, bilgi ve alıştırma hedefleri tek tek eşlenecektir.

## Okuma yolları

Başlangıç okuru önce 01–10'u tamamlar. Yazılım geliştiren okur 11–21 ile çalışan ürün ve ajan düzenini kurar. İleri uygulamalar 22–36'da aynı projenin değerlendirme ve işletim koşullarını genişletir. İleri uygulamaya atlayan okur, bağımlı olduğu çıktıların kendi projesinde mevcut ve doğrulanmış olduğunu kontrol eder.

Yeni yöntemler tarihli kaynak kaydıyla eklenir. Yöntemin adı, çözmek istediği sorun, deney sorusu, maliyeti ve çıkarılma koşulu birlikte yazılır. Böylece sonraki baskıda değişen bir ürünü güncellerken uygulamanın öğrenme hedefi korunabilir.

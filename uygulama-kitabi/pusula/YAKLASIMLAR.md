# Güncel yaklaşımlar ve deney soruları

İnceleme tarihi: 26 Ekim 2026. Aşağıdaki kayıtlar birincil belgelerden kapsam belirlemek için hazırlanmıştır. Ürünlerin yerel çalıştırma veya uyumluluk testi yapılmadı. Her kaydın erişim tarihi ve uygulanacağı ders [sources.json](sources.json) içinde bulunur.

| Yaklaşım | Pusula'da sorulacak soru | Ders |
|---|---|---|
| Prompt engineering | Aynı kaynak ve görevde hangi talimat değişikliği sonucu iyileştiriyor? | U09–10 |
| Context engineering | Gerekli bilgi kaybolmadan bağlam nasıl seçiliyor? | U13–14 |
| Spec-driven development | Gereksinim değişince plan, görev ve test nasıl birlikte güncelleniyor? | U02–07, U34 |
| Loop engineering | Yeni çevrim ne zaman gerekli, ne zaman durmalı? | U19 |
| Harness engineering | Model, araç, durum ve doğrulayıcı nasıl birlikte çalışıyor? | U20–21 |
| Agent Skills | Tekrarlanan yöntem ne zaman yükleniyor ve doğru uygulanıyor mu? | U08, U33 |
| Değerlendirmeyle yönlendirilen geliştirme | Değişiklik kabul edilen sonuçları hangi görevlerde bozuyor? | U10, U24 |
| Agentic RAG ve bilgi grafı | Arama veya ilişki katmanı hangi sorularda yarar sağlıyor? | U15–16 |
| Çoklu ajan ve uzun görev | İş bölümü kaliteyi, süreyi ve insan emeğini nasıl etkiliyor? | U21–23 |
| MCP, A2A, NLWeb, WebMCP | Gereken şey araç bağlantısı mı, görev devri mi, bilgi sorgusu mu, tarayıcı etkileşimi mi? | U18, U28 |
| Yönetilen çalışma çatısı | Yerel sorumluluklardan hangileri hizmete taşınıyor, hangileri ekipte kalıyor? | U34 |
| Programatik optimizasyon ve katman çıkarma | Aynı kabul setinde hangi talimat veya bileşen gereksizleşiyor? | U10, U35 |

Bu başlıklar tek bir standart ailesi değildir. Protokol, dosya biçimi, ürün özelliği, araştırma yaklaşımı ve kitabın öğretim yöntemi kendi türleriyle adlandırılır. “Yeni” nitelemesi bütün başlıkların aynı tarihte ortaya çıktığını anlatmaz.

## Birincil kaynaklar

- [Context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents): Bağlam seçimi, sıkıştırma ve görev sürekliliği için yöntem kaynağı.
- [Harness engineering](https://openai.com/index/harness-engineering/): Depo bilgisini, araçları ve doğrulamayı ajan çalışmasına bağlayan mühendislik örneği.
- [Uzun süren uygulama geliştirme](https://www.anthropic.com/research/harness-design-long-running-apps): Planlayıcı, üretici ve değerlendirici rollerini uzun görevde inceleyen deney.
- [Agent Skills biçimi](https://agentskills.io/specification): SKILL.md giriş dosyası, gerekli name/description alanları ve isteğe bağlı destek kaynakları.
- [Spec-driven development](https://github.com/github/spec-kit): Gereksinim, plan ve görev belgelerine dayanan geliştirme aracı; bütün yöntemlerin standardı olarak sunulmaz.
- [Ajan değerlendirmesi](https://www.anthropic.com/research/demystifying-evals-for-ai-agents): Görev, deneme, iz, değerlendirici ve sonuç ayrımı.
- [MCP mimarisi](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture): Araç ve veri bağlantısının protokol düzeyi; sürümlü belge.
- [A2A](https://a2a-protocol.org/latest/): Ajanlar arasında görev ve yetenek etkileşimini inceleme kaynağı.
- [AGENTS.md](https://agents.md/): Kodlama ajanına proje bağlamı ve çalışma yönergesi veren açık dosya biçimi.
- [Claude Code Skills](https://code.claude.com/docs/en/skills): Claude Code ürünündeki skill kullanımı; taşınabilir biçimden ayrılan ürün ayrıntıları burada doğrulanır.
- [Yönetilen ajan çalışma düzeni](https://www.anthropic.com/research/managed-agents): Model, oturum ve yürütme ortamı arayüzlerini ayırma yaklaşımı.
- [DSPy](https://dspy.ai/current/): İmza, modül, ölçüt ve optimizasyonla model programları kurma yaklaşımı.
- [NLWeb](https://github.com/nlweb-ai/NLWeb): Bilgi içeriğini doğal dil sorgularına açan proje; MCP veya A2A ile aynı kapsamda sunulmaz.
- [WebMCP önizleme duyurusu](https://developer.chrome.com/blog/webmcp-epp): Duyuru, tarayıcıda yapılandırılmış araç etkileşimi önerisini anlatır. Bugünkü genel erişim veya normatif standart statüsünü tek başına kanıtlamaz.

## Yeni yaklaşım ekleme kuralı

Önce mevcut uygulamada çözülemeyen sorunu yazın. Ardından birincil kaynak, yayın veya sürüm tarihi, kullanılan özellik ve karşılaştırma görevini belirleyin. Aynı veri ve kabul koşuluyla bir deney yapın. Sonuç yeterli değilse yöntemi kitaba zorunlu adım olarak eklemeyin; sınırı gösteren karşılaştırma olarak saklayın.

Superpowers, Ralph Loop, Context Mode, Maestro ve hazır/görsel ajan araçları U34'te aday araştırma konularıdır. Bu pakette her birinin proje kimliği, sürümü ve ürün davranışı ayrı doğrulanmadığından kurulum talimatı verilmez. İlk uygulamaları hazırlarken resmî depo ve belgelerle doğrulanacaklardır. Bu kayıt, adayları denenmiş yöntem gibi göstermemek içindir.

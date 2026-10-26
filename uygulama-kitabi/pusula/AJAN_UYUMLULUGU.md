# Ortak proje yönergeleri ve ajan uyarlamaları

Belge kontrolü: 26 Ekim 2026. Yerel araç denemeleri: `not_run`.

Proje dosyasını keşfeden ve modele aktaran bileşen, kullanılan ajan aracıdır. Aynı model farklı araçlarda çalışabilir. Bu nedenle modelin adından hareketle yönerge dosyası seçmeyiz; araç, arayüz, sürüm ve etkin ayarları kaydederiz. Normal bir sohbet veya doğrudan model API çağrısı, diskteki AGENTS.md dosyasını sırf bulunduğu için okumaz. Böyle bir kullanımda belgeyi ekleme veya yükleme adımı ayrıca kurulmalıdır.

## Ortak bilgi ile araca özgü davranışı ayırmak

Pusula'da proje amacı `vision.md`, gereksinimler `prd.md`, tasarım `design.md`, teknoloji kararları `tech-stack.md`, iş sırası `roadmap.md` ve `tasks.md` içinde tutulur. `AGENTS.md`, ortak çalışma kurallarını ve bu belgelerin hangi görevde okunacağını belirtir. Bütün belgeler her oturuma tam metin olarak eklenmez.

Araca özgü giriş gerekiyorsa ortak kurala bağlanan küçük bir dosya oluşturulur. Dosya içe aktarma, yapılandırmayla dosya ekleme ve ajandan bir belgeyi okumasını isteme farklı yöntemlerdir. Sıradan bir Markdown bağlantısı her araçta otomatik içe aktarma anlamına gelmez. İçeriğin gerçekten yüklendiği ve göreve uygulandığı ayrı denetlenir.

Bir araç AGENTS.md dosyasını gereken kapsamda zaten okuyorsa ona başka adla aynı içeriği üretmek gerekmez. Örneğin Codex için sırf simetri kurmak amacıyla `CODEX.md` oluşturulmaz. Ürün içindeki araştırmacı ve inceleyici rollerinin kataloğu ise `agent-roles.md` adını taşır; bu dosya bir yükleyici standardı değildir. `AGENTS.md` ile `agents.md` adlarını birlikte kullanmak harf büyüklüğünü ayırmayan dosya sistemlerinde çakışır.

## Hangi araç hangi dosyayı kullanır?

Bu tablo resmî belgelerdeki davranışın kapsamını gösterir. Kurulu sürümün aynı davrandığını kanıtlayan yerel koşu değildir. Her araca ait model, sürüm, arayüz ve etkin ayar, okurun `agent-compatibility.md` kaydında ayrıca bulunmalıdır.

| Ajan aracı | Ortak yönerge ve gerekirse ek dosya | Yükleme deneyinde kontrol edilecek nokta |
|---|---|---|
| Codex | `AGENTS.md`; gerektiğinde dizin kapsamlı yönergeler | Üst dizinden çalışma dizinine keşif sırası ve aynı dizinde `AGENTS.override.md` önceliği. [OpenAI Docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code | `CLAUDE.md`, `.claude/rules/*.md`; güncel belgede proje yönergesi ayarına bağlı `AGENTS.md` desteği | Varsayılan seçimde CLAUDE dosyalarının bulunması AGENTS yüklenmesini etkiler. Birlikte yükleme ve içe aktarma seçenekleri ayrı denenir. [Resmî belge](https://code.claude.com/docs/en/memory) |
| Gemini CLI | Varsayılan `GEMINI.md`; `context.fileName` ile başka ad veya liste seçilebilir | `@dosya` içe aktarması veya doğrudan AGENTS seçimi kullanılır. `/memory show` ile yüklenen bağlam kontrol edilir. [Resmî belge](https://geminicli.com/docs/cli/gemini-md/) |
| Cursor | `AGENTS.md`; koşullu kurallar için `.cursor/rules/*.mdc` | Kuralın sürekli, dosya kapsamlı veya başka bir etkinleşme biçimiyle çalışması denetlenir. Dosya atfı içeriği kendiliğinden bağlama birleştirmez. [Resmî belge](https://cursor.com/docs/rules) |
| GitHub Copilot | `.github/copilot-instructions.md`; yol kapsamlı `.github/instructions/*.instructions.md` | IDE, CLI, kod inceleme ve bulut ajanının desteklediği özellikler ayrı kaydedilir. AGENTS desteği bütün arayüzler için varsayılmaz. [Resmî belge](https://docs.github.com/en/copilot/reference/customization-cheat-sheet) |
| OpenCode | `AGENTS.md`; ek belgeler için `opencode.json` içindeki `instructions` | AGENTS varken CLAUDE geri dönüşünün seçilmemesi ve ek dosyaların yüklenmesi kontrol edilir. [Resmî belge](https://opencode.ai/docs/rules/) |
| Cline | `AGENTS.md`; `.clinerules/` veya `.cline/rules/` | Kural panelinde etkin dosyalar görülür. Aynı kurallar iki dizine kopyalanmaz. [Resmî belge](https://docs.cline.bot/customization/cline-rules) |
| Cascade | `AGENTS.md`; incelenen güncel belgede `.devin/rules/*.md`, eski `.windsurf/rules/*.md` için geri dönüş desteği | Windsurf belge adresi Devin Desktop belgelerine yönleniyor. Kurulu ürün ve sürüm kaydedilmeden eski/yeni dizin seçilmez. [Resmî belge](https://docs.devin.ai/desktop/cascade/memories) |

AGENTS.md ile özel alt ajan tanımı da ayrı şeylerdir. Örneğin Copilot'un `.github/agents/` dosyaları uzman ajan tanımları; `.github/prompts/` dosyaları tekrar kullanılabilen promptlardır. Bunlar proje yönergesiyle eşanlamlı değildir. Skill paketi de göreve bağlı yöntem içerir; izin ve sandbox ayarlarının yerine geçmez.

## Şablonları kullanmak

Bu paket araçları yapılandırmaz. Aşağıdaki dosyalar öğretim örneğidir; seçilen örnek yalnız okurun ayrı Pusula projesinde belirtilen konuma yerleştirilir. `.example` uzantısı şablonun çalışır yapılandırma gibi algılanmasını önler. Mevcut dosyanın üstüne otomatik yazılmaz.

| Örnek | Okurun projesindeki hedef | Açıklama |
|---|---|---|
| [Ortak AGENTS örneği](reference/AGENTS.md) | `AGENTS.md` | Ortak proje kuralları |
| [Claude Code girişi](reference/CLAUDE.md) | `CLAUDE.md` | Gerekiyorsa aynı dizindeki AGENTS.md içeriğini içe alır |
| [Gemini CLI girişi](reference/adapters/GEMINI.md.example) | `GEMINI.md` | Varsayılan dosya adıyla aynı ortak kaynağı içe alır |
| [Copilot yönergesi](reference/adapters/copilot-instructions.md.example) | `.github/copilot-instructions.md` | Ortak dosyayı açıkça okuma yönergesi verir; otomatik içe aktarma iddiası taşımaz |
| [Cursor tasarım kuralı](reference/adapters/design.mdc.example) | `.cursor/rules/design.mdc` | Örnek `app/ui/**` kapsamını kullanır; gerçek dizine uyarlanmalıdır |

Claude Code ve Gemini CLI için seçilen yükleme yolunun çift içerik veya eksik bağlam üretmediğini kontrol edin. Bir araç ortak dosyayı gerektiği gibi yükleyemiyorsa bunu uyumluluk kaydında belirtin. Kopya türetmek zorunluysa kaynak ve güncellik denetimi olan bir üretim adımı tanımlayın; bağımsız elle düzenlenen ikinci kopya bırakmayın.

## U07'nin üretim ve kabul akışı

[U07 promptu](prompts/07.md), ortak belgelerle birlikte `agent-compatibility.md`, `instruction-tests.json` ve seçilen araca ait `agent-adapters/` şablonlarını üretir. Uyum kaydı araç, sürüm, arayüz, model, çalışma dizini, kaynak tarihi, hedef dosya, etkin ayar ve gözlenen sonucu ayrı alanlarda tutar. Model bilgisi karşılaştırma içindir; yönerge dosyasının adını belirlemez.

[Deneme taslağında](reference/instruction-tests.example.json) ortak kuralın yüklenmesi, araca özgü ek, alt dizin kapsamı, çelişen kural ve eksik başvuru vakaları bulunur. Tüm gözlemler boştur. Önce seçilen araç için beklenen davranış resmî belge ve ayarla tanımlanır; sonra yeni bir oturumda sentetik görev çalıştırılır. Eksik belgeyle sonuç uydurulmaması ve yapılamayan kontrolün açıkça bildirilmesi ayrıca aranır.

Yükleme kaydı ile davranış sonucu ayrı değerlendirilir. Aracın bağlam görünümü bir dosyanın yüklendiğini gösterebilir; dosyanın kurallarına uyulduğunu tek başına göstermez. Ajanın “okudum” demesi de yükleyici kanıtı değildir. Gerçek görev çıktısı, yapılan işlemler ve varsa bağlam kaydı birlikte saklanır. Araç böyle bir kayıt sunmuyorsa gözlem sınırı belirtilir.

Bu başlangıç paketinin yapısal doğrulaması JSON ve dosya bağlantılarını denetler. Sekiz araçta davranış uyumu veya güvenlik sınırı doğrulandığı anlamına gelmez. Teknik erişim kısıtları, aracın izin ve korumalı alan ayarlarıyla ayrıca uygulanır.

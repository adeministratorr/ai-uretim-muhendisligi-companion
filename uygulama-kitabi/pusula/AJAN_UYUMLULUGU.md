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

## Diğer IDE ve CLI araçları

İlk tabloyla birlikte 22 araç veya araç bileşeni kapsanır. Her satır yalnız belirtilen arayüz ve belge için geçerlidir. VS Code veya JetBrains bir barındırıcı olabilir; içinde seçilen Copilot, Junie, Continue ya da harici CLI ayrıca belirtilir. Kullanıcının söylediği Zcode burada Z.ai'nin **ZCode Agent** ürünü olarak incelendi; Zed ve Qoder ayrı ürünlerdir.

| Araç / arayüz | Dosya veya bağlantı yöntemi | Denenecek fark |
|---|---|---|
| [ZCode Agent](https://zcode.z.ai/en/docs/agents) | `AGENTS.md`; kullanıcı genelinde `~/.zcode/AGENTS.md` | Çalışma alanı kökü esas alınır. Alt dizin birleştirme ve otomatik import desteği varsayılmaz. |
| Qoder — [IDE](https://docs.qoder.com/user-guide/rules) / [CLI](https://docs.qoder.com/cli/memory) | `AGENTS.md`, `.qoder/rules/**/*.md`; CLI'da ayrıca kullanıcı ve yerel proje yönergeleri | IDE'de çelişen rules içeriği AGENTS içeriğinden önceliklidir. CLI'da kapsam, tetikleme ve yüklenen kaynaklar ayrıca denetlenir. |
| [Zed Agent](https://zed.dev/docs/ai/instructions) | `AGENTS.md`; uyumlu eski dosyalar da tanınır | İlk eşleşen dosya kullanılır: örneğin `.rules`, AGENTS dosyasından önce gelir. Harici ajan kendi kurallarına göre değerlendirilir. |
| [Google Antigravity](https://www.antigravity.google/docs/rules/) | `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md` | `.agents/rules/` içindeki modüler dosyalarda geçerli `trigger` gerekir; AGENTS/GEMINI düz Markdown kullanır. App/CLI/IDE ayarları ayrı kaydedilir. |
| [Kiro](https://kiro.dev/docs/steering/) | `AGENTS.md`, `.kiro/steering/*.md` | IDE ve CLI sürümlerinin inclusion desteği ayrılır. Özel ajanın steering yüklemesi için `resources` ayarı denetlenir. |
| [Junie CLI](https://junie.jetbrains.com/docs/guidelines-and-memory.html) | Önce `.junie/AGENTS.md`; sonra kök `AGENTS.md` ve ilgili Junie ekleri | Eski `.junie/guidelines.md` bir geri dönüş seçeneğidir. CLI belgesi bütün IDE eklentilerinin davranışı diye genellenmez. |
| [JetBrains AI Assistant](https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html) | `.aiassistant/rules/*.md` | Always, manual, model decision ve dosya kalıbı seçenekleri kaydedilir; yanıt eklerinde uygulanan kural kontrol edilir. |
| [Continue IDE eklentisi](https://docs.continue.dev/customize/deep-dives/rules) | `.continue/rules/*.md` | Kural sırası ve etkinleşme koşulu denetlenir. Belgedeki Agent/Chat/Edit desteği autocomplete veya CLI için otomatik kanıt sayılmaz. |
| [Roo Code](https://roocodeinc.github.io/Roo-Code/features/custom-instructions/) | `AGENTS.md`, `.roo/rules/`, `.roo/rules-{modeSlug}/` | `roo-cline.useAgentRules` ayarı ve etkin mod kaydedilir. Dizin kuralları ile eski `.roorules` geri dönüşü ayrı incelenir. |
| [Kilo Code — VS Code](https://kilo.ai/docs/customize/custom-instructions) | `AGENTS.md`; uyumlu `CLAUDE.md`, `CONTEXT.md`; ekler için `kilo.jsonc` | İncelenen eklenti yönergeleri CLI davranışıyla özdeş sayılmaz. Eski `.kilocoderules` örnekleri güncel varsayılan diye kopyalanmaz. |
| [Aider](https://aider.chat/docs/usage/conventions.html) | `--read AGENTS.md` veya `.aider.conf.yml` içinde `read` | Ortak dosyanın bağlama salt okunur alınması açıkça yapılandırılır. AGENTS adının varlığı tek başına otomatik keşif kanıtı değildir. |
| [Qwen Code](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/) | Varsayılan `QWEN.md`; `context.fileName` ile ortak dosya seçilebilir | Dizin hiyerarşisi ve etkin bağlam `/memory` görünümünden kontrol edilir. Model adı ile CLI adı ayrılır. |
| [Amp](https://ampcode.com/docs/customize/agents-md) | `AGENTS.md`; üst dizin ve alt ağaç yönergeleri | Üst kapsam ile dosya okunduğunda yüklenen alt kapsam ayrılır. Ignore ayarının ilgili dosyayı dışlamadığı kontrol edilir. |
| [Factory Droid](https://docs.factory.com/harness/agents-md) | `AGENTS.md`; tasarım için `DESIGN.md`, `Design.md` veya `design.md` | Tasarım yönergeleri ayrıca yüklenir. Bu araçtaki davranış bütün ajanlara genellenmez; aynı dosyanın farklı harfli kopyaları oluşturulmaz. |

### ZCode için uygulama

ZCode'da yeni bir `ZCODE.md` dosyası gerekmiyor. Çalışma alanındaki ortak AGENTS dosyası kullanılır. Genel yönerge önce, çalışma alanı yönergesi sonra eklenir. `CLAUDE.md` yalnız ilk geçişte kaynak olabilir; sürekli yüklenen dosya olarak anlatılmamalı. Bu davranış [ZCode belgesinde](https://zcode.z.ai/en/docs/agents) açıklanır.

Pusula'nın ZCode denemesinde [dört vakalı taslak](reference/zcode-instruction-tests.example.json) kullanılır. Geçici çalışma alanları hazırlanır; gerçek kullanıcı profilindeki yönergeler değiştirilmez. Otomatik yükleme ile ajanın görev sırasında açıkça dosya okuması ayrı kaydedilir. Belgelenen kapsamı aşan bir davranış beklenmez.

### Qoder için uygulama

Qoder IDE, proje dizinindeki `AGENTS.md` dosyasını ek ayar olmadan tanır. `.qoder/rules` içindeki kurallar elle çağrılabilir, model kararına bağlanabilir, sürekli uygulanabilir veya dosya kalıbıyla sınırlandırılabilir. AGENTS içeriğiyle çeliştiklerinde bu kurallar önceliklidir. Bu öncelik [IDE belgesinde](https://docs.qoder.com/user-guide/rules) belirtilir; CLI için ayrıca kontrol edilir.

Qoder CLI'nın [bellek belgesi](https://docs.qoder.com/cli/memory), `~/.qoder/AGENTS.md`, proje `AGENTS.md`, `AGENTS.local.md` ve `.qoder/rules/**/*.md` konumlarını açıklar. Güvenilen çalışma alanında üst dizin araması varsayılan olarak `.git` sınırında durur. Alt dizin yönergeleri başlangıçta topluca yüklenmez; ilgili dosya okunduğunda eklenir. `@dosya` içe aktarması desteklenir; kod içinde yazılan atıflar içe aktarılmaz. `/memory`, yüklenen kaynakların incelenmesini sağlar. Yerel yönergeler ekip deposuna eklenmez.

U07'de Qoder seçildiğinde [genel deneme taslağının](reference/instruction-tests.example.json) I03 ve I06 vakaları kullanılan arayüze uyarlanır. IDE için geçici kopyada çelişen AGENTS ve rules içeriği; CLI için dosya okunmadan önceki ve sonraki alt dizin bağlamı karşılaştırılır. Beklenen sonuç kaynakla, gözlenen sonuç koşu kaydıyla yazılır. Bu pakette Qoder koşusu yapılmadı.

### Kitapta ortaklaştırılmayacak davranışlar

Yönergeleri birleştirmek, ilk eşleşen dosyayı seçmek ve yapılandırmada belirtilen dosyayı yüklemek farklı işlemlerdir. Bir araçta çalışan yönerge düzenini diğerine taşırken dosya adını değiştirmek yeterli olmayabilir. Ayrıca bir IDE içindeki yerleşik ajanla harici ajan aynı yükleyiciyi kullanmak zorunda değildir. Bu nedenle karşılaştırma kaydı barındırıcı IDE, eklenti, çalışan ajan, sürüm ve çalışma dizinini ayrı tutar.

Droid'in tasarım dosyalarını ayrıca yüklemesi gibi istisnalar, `design.md` için evrensel otomatik yükleme kuralı oluşturmaz. Kitap önce seçilen aracın davranışını doğrulatır, ardından ortak Pusula belgelerini o davranışa göre bağlar. Yeni bir araç için doğrulanmamış dosya adı türetilmez.

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

[Deneme taslağında](reference/instruction-tests.example.json) ortak kuralın yüklenmesi, araca özgü ek, alt dizin kapsamı, çelişen kural, eksik başvuru, dosya seçme sırası ve harici ajan ayrımı için yedi vaka bulunur. Tüm gözlemler boştur. Önce seçilen araç için beklenen davranış resmî belge ve ayarla tanımlanır; sonra yeni bir oturumda sentetik görev çalıştırılır. Eksik belgeyle sonuç uydurulmaması ve yapılamayan kontrolün açıkça bildirilmesi ayrıca aranır.

Yükleme kaydı ile davranış sonucu ayrı değerlendirilir. Aracın bağlam görünümü bir dosyanın yüklendiğini gösterebilir; dosyanın kurallarına uyulduğunu tek başına göstermez. Ajanın “okudum” demesi de yükleyici kanıtı değildir. Gerçek görev çıktısı, yapılan işlemler ve varsa bağlam kaydı birlikte saklanır. Araç böyle bir kayıt sunmuyorsa gözlem sınırı belirtilir.

Bu başlangıç paketinin yapısal doğrulaması JSON ve dosya bağlantılarını denetler. Listelenen araçlarda davranış uyumu veya güvenlik sınırı doğrulandığı anlamına gelmez. Teknik erişim kısıtları, aracın izin ve korumalı alan ayarlarıyla ayrıca uygulanır.

# Belge ilişkileri

| İstenen belge | Gerekli girdiler | Kontrol |
|---|---|---|
| vision.md | brief.md | Kullanıcı, sorun ve ilk kapsam açık mı? |
| prd.md | vision.md, scope.md | Davranışlar gözlenebilir kabul koşullarına bağlı mı? |
| design.md | prd.md, acceptance.md | Boş, hata, iptal ve eski kaynak durumları var mı? |
| tech-stack.md | prd.md, design.md, environment.md | Tercih gerekçesiyle doğrulanmış sürüm ayrılmış mı? |
| roadmap.md | prd.md, tech-stack.md, acceptance.md | Aşamalar ve tamamlanma koşulları tutarlı mı? |
| tasks.md | roadmap.md, acceptance.md | Her iş gereksinime, çıktıya ve doğrulamaya bağlı mı? |
| AGENTS.md | tech-stack.md, tasks.md, acceptance.md | Komutlar gerçekten mevcut mu, yetki sınırı açık mı? |

Tabloda bulunmayan belge için kullanıcının görev tanımından girdi ihtiyacını çıkar; olmayan dosyayı varmış gibi gösterme. Bu liste Pusula öğretim düzenidir, ürünlerin otomatik dosya keşif kuralı değildir.

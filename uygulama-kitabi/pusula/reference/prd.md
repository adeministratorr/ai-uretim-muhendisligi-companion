# Pusula ilk sürüm gereksinimleri

Durum: öğretim amaçlı tasarım örneği; çalışan ürün kanıtı yok.

| Kimlik | Davranış | Kabul koşulu |
|---|---|---|
| REQ-001 | Kaynağı kimlik ve revizyonuyla kaydet | Aynı kaynağın yeni revizyonu eski metni sessizce değiştirmesin; eski taslak kendi revizyonunu göstersin |
| REQ-002 | Soru ve taslağı çalışma alanına bağla | Başka çalışma alanının kaynağı sorguya ve taslağa girmesin |
| REQ-003 | İddiayı kaynakla ilişkilendir | Her esas iddiada etkin kaynak kimliği, revizyon ve ilgili alıntı bulunsun; alıntının anlam desteği ayrıca incelensin |
| REQ-004 | Eksik bilgi ve çelişkiyi göster | Kayıtta bulunmayan kayıt ücreti sorusuna sayı üretilmesin; çelişen süreler birlikte gösterilsin |
| REQ-005 | İnceleme kararını revizyona bağla | Kaynak değiştiğinde eski kabul yeniden kullanılmasın; yeni taslak inceleme beklesin |

Taslağın biçim kontrolünden geçmesi insan kabulü oluşturmaz. Başlangıçta gerçek model kullanılmadan sabit öğretim yanıtıyla akış sınanır. Model bağlantısı bu kabul koşulları korunduktan sonra eklenir.

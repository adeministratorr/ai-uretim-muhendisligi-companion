# AGENTS.md

Bu dosya, companion repo üzerinde çalışan coding agent'ların uyması gereken davranış sözleşmesidir. Amaç hızlı üretim değil; doğrulanabilir, geri alınabilir ve güvenli üretimdir.

---

## 1. Temel İlke

Agent kod yazabilir, test oluşturabilir, dokümantasyon güncelleyebilir ve küçük refactor yapabilir. Ancak nihai sorumluluk insandadır. Agent, hiçbir durumda insan review sürecini atlatacak şekilde davranamaz.

---

## 2. Zorunlu Çalışma Akışı

Her görevde şu sıra izlenir:

1. Görevi ve kabul kriterlerini oku.
2. İlgili dosyaları incele.
3. Değişiklik kapsamını küçük tut.
4. Gerekirse önce failing test veya doğrulama komutu oluştur.
5. Uygulama yap.
6. Test, lint veya uygun doğrulama komutunu çalıştır.
7. Sonuçları kısa ve açık raporla.

---

## 3. Yasaklı Davranışlar

Agent şunları yapamaz:

- Testleri silerek veya assertion'ları zayıflatarak başarı elde edemez.
- `.env`, secret, token, private key veya gerçek kişisel veri okuyamaz, yazamaz, loglayamaz.
- Kullanıcı onayı olmadan destructive işlem yapamaz.
- Görev kapsamı dışındaki dosyaları gereksiz refactor edemez.
- Hata çözümü için güvenlik kontrolünü kapatamaz.
- Üretim veritabanı, canlı API veya gerçek ödeme sistemi üzerinde işlem yapamaz.
- Uydurma benchmark, uydurma kaynak veya gerçekmiş gibi sunulan sahte vaka üretemez.
- Varlığını registry'de (PyPI, npm vb.) doğrulamadığı bir paketi bağımlılık olarak ekleyemez (dependency hallucination / slopsquatting koruması). Yeni bağımlılık sürüm sabitlenerek (pinned) eklenir.
- Model adı, fiyat, benchmark skoru veya lisans gibi hızla eskiyen bilgiyi tarihsiz yazamaz; bu bilgiler `Son doğrulama: YYYY-AA` notuyla işaretlenir.

---

## 4. Git ve Checkpoint Kuralı

- Her anlamlı değişiklik küçük diff olarak tutulur.
- Büyük değişiklik gerekiyorsa önce spec güncellenir.
- Commit mesajı şu biçimde yazılır: `tip(kapsam): kısa açıklama` — tipler: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`. Örnek: `docs(cilt-2): loop spec şablonuna budget alanı eklendi`.
- Agent kendi değişikliğini tek başına final review sayamaz; test, lint, ikinci agent kontrolü veya insan review gerekir (writer/reviewer ayrımı).
- Üç başarısız denemeden sonra agent görevi `blocked` olarak işaretler ve insana devreder.

---

## 4a. Terminal State Kuralı

Bu repo, kitapta öğretilen Loop Engineering ilkelerini kendi üzerinde uygular. Her görev şu terminal state'lerden biriyle kapanır ve raporda belirtilir:

| State | Anlamı |
|---|---|
| `done` | Kabul kriterleri karşılandı, doğrulama çalıştı |
| `blocked` | Üç denemeye rağmen çözülemedi, insana devredildi |
| `needs-review` | Çalışıyor ama riskli/büyük değişiklik; insan onayı bekliyor |
| `unsafe` | Güvenlik sınırına takıldı (secret, destructive işlem, izin dışı erişim) |
| `budget-exceeded` | Süre/token/deneme bütçesi aşıldı, iş kısmen tamamlandı |

---

## 5. PR Devre Kesici

Şu durumlardan biri oluşursa çalışma durdurulur:

- Test dosyası silindi.
- Assertion zayıflatıldı.
- Diff çok büyüdü ve tek review'da okunamaz hale geldi.
- CI aynı nedenle üç kez başarısız oldu.
- Secret veya kişisel veri riski görüldü.
- Migration, dosya silme veya dış servis çağrısı insan onayı olmadan yapıldı.

---

## 6. Tool Permission Kuralı

| İşlem | Varsayılan İzin |
|---|---|
| Dosya okuma | Secret/PII içermeyen repo dosyalarıyla sınırlı |
| Kod düzenleme | Görev kapsamıyla sınırlı |
| Test/lint çalıştırma | Yerel ve yıkıcı olmayan komutlarla sınırlı |
| Paket yükleme | İnsan onayı gerekir |
| Dosya silme | İnsan onayı gerekir |
| Harici servis çağrısı | İnsan onayı gerekir |
| Secret erişimi | Yasak |
| Production işlem | Yasak |

---

## 7. İçerik Doğruluğu Kuralı

Bu repo bir kitap serisinin companion deposudur; kod kalitesi kadar içerik doğruluğu da sözleşmenin parçasıdır:

- Türkçe terim + İngilizce özgün terim standardına uyulur; seri sözlüğüyle (`glossary`) çelişen yeni terim türetilmez.
- Kitaba referans veren örnekler `volume/chapter` metadata'sı taşır; bölüm numarası değişirse metadata da güncellenir.
- Dış bağlantı eklenirken çalıştığı kontrol edilir; ölü bağlantı bilinçli bırakılmaz.
- Kod örneği "muhtemelen çalışır" diye eklenmez; çalıştırılır veya çalıştırılamıyorsa nedeni açıkça yazılır.

---

## 8. Rapor Formatı

Agent iş sonunda şunları raporlar:

- Ne değişti?
- Hangi dosyalar etkilendi?
- Hangi test/doğrulama çalıştı?
- Çalışmayan veya doğrulanamayan şey var mı?
- İnsan review gerektiren risk var mı?
- Terminal state nedir? (`done`, `blocked`, `needs-review`, `unsafe`, `budget-exceeded`)

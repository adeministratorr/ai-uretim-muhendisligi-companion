# Üç Skill'i Karşılaştır Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 10 — Skill Kullanımı, 10.3-10.10 ve 10.12
(Uygulama 10 — Üç Skill'i Karşılaştır).

```yaml
volume: 2
chapter: 10
book_section: "10.3-10.10 Skill Anatomisi, Hazır Skill Kullanımı ve Doğrulama"
concepts:
  - Skill
  - trigger koşulu
  - örnek girdi/çıktı
  - yasaklar
objectives:
  - "LO-10.1"
  - "LO-10.2"
  - "LO-10.4"
last_verified: "2026-07"
```

## Ne Yapar?

Kod inceleme, test yazma ve commit mesajı yazma görevleri için kurduğunuz üç
skill'in deneme kaydını ortak bir kabul kapısından geçirir. Her kayıt şu kanıtları
taşır:

- Skill'in adı, kaynağı ve trigger koşulu.
- Front matter, talimat, örnek girdi/çıktı ve yasaklar bölümlerinin incelendiği
  bilgisi.
- Gerçek araçta kullanılan deneme isteği.
- Skill'in tetiklenip tetiklenmediği, talimatların uygulanıp uygulanmadığı ve
  yasaklara uyulup uyulmadığına ilişkin gözlem.
- Başarısız ya da belirsiz davranışı açıklayan kısa karşılaştırma notu.

Doğrulayıcı skill'i çalıştırmaz. Claude Code, Cursor veya benzeri bir araçta
yaptığınız denemenin kaydını denetler. Bir gözlemin `hayır` olması kaydı geçersiz
kılmaz; eksik bırakılması geçersiz kılar. Amaç üç skill'i başarılı ilan etmek değil,
aralarındaki farkı kanıtla görünür kılmaktır.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/skill-comparison/skill_comparison_lab.html>
İsterseniz `skill_comparison_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Üç skill'i kendi aracınızda birer kez deneyin, sonra gözlemlerinizi forma yazıp
**Karşılaştırmayı Doğrula** düğmesine basın.

**Kod biliyorsanız:** Saf Python sürümünü gömülü kayıtlarla veya kendi JSON
dosyanızla çalıştırın.

```bash
python3 skill_comparison_lab.py
python3 skill_comparison_lab.py karsilastirma.json
python3 -m pytest test_skill_comparison_lab.py
```

İlk komut üç temsilî kaydı doğrular. İkinci komut verdiğiniz JSON dosyasını okur;
dosyaya yazmaz. Üçüncü komut eksik görevin, tamamlanmamış anatomi kontrolünün,
yanıtsız gözlemin, yinelenen skill adının ve hassas veri örüntüsünün reddedildiğini
sınar.

## Beklenen Çıktı

```text
Skill Karşılaştırma Kaydı
Görev: 3/3
Anatomi kontrolü: 3/3
Trigger gözlemi: 2/3 olumlu
Talimat gözlemi: 2/3 olumlu
Yasaklar gözlemi: 3/3 olumlu
İncelenecek skill: 1
Kabul kriteri karşılandı: Üç skill denendi ve karşılaştırma kaydı tamamlandı.
```

Temsilî test yazma skill'i dar trigger koşulu nedeniyle ilk istekte tetiklenmez.
Kayıt yine kabul edilir; karşılaştırma notu bu davranışı ve yeniden deneme kararını
açıkça yazar.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 skill_comparison_lab.py`).
- [x] Test komutu var (`pytest`).
- [x] Beklenen çıktı gösteriliyor.
- [x] Kod inceleme, test yazma ve commit mesajı yazma görevlerinin üçü de bulunuyor.
- [x] Her skill için dört anatomi parçası, bir deneme isteği ve üç gözlem kaydediliyor.
- [x] Olumsuz gözlem başarı gibi gösterilmiyor; incelenecek skill sayısına yansıtılıyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü skill adları, kaynaklar ve deneme sonuçları temsilîdir. Gerçek bir ekip
  kütüphanesini veya ürün davranışını göstermez.
- Formdaki `evet` seçimi araç tarafından doğrulanmaz. Gözlemi, gerçek denemenin
  çıktısını okuyarak insan kaydeder.
- Anatomi parçalarının varlığı, talimatların güvenli veya güncel olduğunu kanıtlamaz.
  Skill klasöründeki ek dosya ve betikler ayrıca incelenmelidir.
- Yasaklar bölümü niyet beyanıdır; mekanik izin sınırı değildir. Kritik işlemler
  aracın permission rules ayarlarıyla ve insan onayıyla sınırlandırılmalıdır.
- Skill davranışı araç, sürüm ve oturum bağlamına göre değişebilir. Son doğrulama:
  2026-07.

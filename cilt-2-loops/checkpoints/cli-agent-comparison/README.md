# CLI Ajan Karşılaştırma Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 6 — CLI Ajanlar, 6.9
(Uygulama 6 — Aynı Bug Fix'i CLI Ajanlarla Karşılaştırma).

```yaml
volume: 2
chapter: 06
book_section: "6.9 CLI Ajan Seçim Matrisi"
concepts:
  - CLI ajan
  - ortak görev tarifi
  - onay modu
  - diff karşılaştırması
objectives:
  - "LO-6.1"
  - "LO-6.2"
  - "LO-6.6"
last_verified: "2026-07"
```

## Ne Yapar?

`get_user_city` fonksiyonundaki aynı hatayı bir veya daha fazla CLI ajana (CLI agent)
çözdürdükten sonra gözlemleri ortak bir kayda dönüştürür. Doğrulayıcı şu koşulları
denetler:

- Her araç için önerilen diff ve gerekçe yazılmıştır.
- Diff, `get_user_city` fonksiyonunu gösteren en az bir ekleme satırı içerir.
- Test sonucu ve önerilen test, varsa, ayrı alanlarda tutulur.
- Değişikliğin yalnızca hedef fonksiyonla sınırlı kalıp kalmadığı kaydedilmiştir.
- Aracın değişiklik öncesi onay isteyip istemediği açıkça belirtilmiştir.
- Gözlemin onay modu kavramıyla ilişkisi tamamlanmış bir notla açıklanmıştır.

Laboratuvar tek araçla tamamlanabilir; ikinci ve üçüncü kayıt karşılaştırmayı genişletir.
Genel bir puan veya "kazanan" üretmez. Karar diff, test ve onay davranışı birlikte
okunarak verilir.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/cli-agent-comparison/cli_agent_comparison_lab.html>
İsterseniz `cli_agent_comparison_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
CLI ajan denemenizdeki diff'i, gerekçeyi, test gözlemini ve onay davranışını forma
yazıp **Karşılaştırmayı Doğrula** düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini denetleyen saf Python sürümünü çalıştırın.

```bash
python3 cli_agent_comparison_lab.py
python3 -m pytest test_cli_agent_comparison_lab.py
```

İlk komut iki temsilî araç kaydını denetler. İkinci komut eksik diff'in, yinelenen araç
adının, geçersiz test/onay kaydının ve onay modu bağlantısı kurulmayan notun reddedildiğini
sınar.

## Beklenen Çıktı

```text
CLI Ajan Karşılaştırması — 2 araç
Araç A: test=geçti, kapsam=uygun, onay=değişiklik öncesi onay istedi, test önerisi=var
Araç B: test=geçti, kapsam=uygun, onay=yalnızca diff sundu, test önerisi=var
Test öneren araç: 2/2
Hedef fonksiyonla sınırlı kalan diff: 2/2
Onay modu notu: Araç A değişiklik öncesinde onay istedi; Araç B yalnızca diff sunduğu için dosya yazma onayı gerektirmedi.
Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.
```

Tarayıcı sürümünde aynı özet yeşil bir sonuç kutusunda gösterilir. Eksik veya geçersiz
bir alan varsa ilgili araç ve ölçüt açıkça belirtilir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Python örneği çalışıyor (`python3 cli_agent_comparison_lab.py`).
- [x] Test komutu var (`pytest`, 18 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Tek araç ve 2-3 araç kullanım düzeyleri destekleniyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü araç adları, diff'ler ve gözlemler temsilîdir. Gerçek bir ürün karşılaştırması
  veya benchmark değildir; kendi denemenizde bu kayıtları değiştirin.
- Laboratuvar bir CLI ajan çalıştırmaz ve yapıştırılan diff'i yürütmez. Kodu ayrı bir
  çalışma dalında uygulayın; testleri orada çalıştırın.
- Formun bir diff'i kabul etmesi, değişikliğin doğru veya güvenli olduğunu kanıtlamaz.
  Diff incelemesi, davranış testleri ve insan onayı ayrı adımlardır.
- "Onay istedi" kaydı, sandbox sınırlarının doğru kurulduğunu göstermez. Dosya, komut,
  ağ ve gizli bilgi izinleri ayrıca kontrol edilmelidir.
- Hassas kodu, gerçek kişisel veriyi veya gizli anahtarı forma ya da bir araca
  yapıştırmayın.

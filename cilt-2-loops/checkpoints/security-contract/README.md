# Güvenlik Sözleşmesi Laboratuvarı

**Kitap bağlantısı:** Cilt 2, Bölüm 14 — Güvenlik, Etik ve Sınırlar, 14.2-14.13
(Lab 14 — Bir Yapay Zekâ Destekli Depo İçin Güvenlik Sözleşmesi).

```yaml
volume: 2
chapter: 14
book_section: "14.2-14.13 Güvenlik Sözleşmesi"
concepts:
  - veri sınıflandırması
  - secret yönetimi
  - tool permission yönetimi
  - korumalı dosya
  - loop güvenliği
objectives:
  - "LO-14.1"
  - "LO-14.2"
  - "LO-14.3"
  - "LO-14.4"
  - "LO-14.5"
  - "LO-14.6"
  - "LO-14.7"
last_verified: "2026-07"
```

## Ne Yapar?

Bir proje için hazırlanan güvenlik sözleşmesini Bölüm 14'teki beş ölçütle denetler:

- Veri sınıflandırmasında `gönderilebilir`, `anonimleştirilerek` ve `asla`
  kararlarının üç somut örnekle gerekçelendirilmesi.
- Secret yönetiminde yok sayılan dosyaların, taramanın çalıştığı noktanın ve sızıntı
  sonrası ilk üç adımın yazılması.
- En az beş işlem için `allow`, `ask` veya `deny` kararının gerekçelendirilmesi.
- En az üç korumalı dosya veya yolun `ask` ya da `deny` katmanına bağlanması.
- Bir ajan döngüsünün yetki, maliyet ve veri sınırlarının ayrı ayrı tanımlanması.

Doğrulayıcı ayrıca kararların yinelenmemesini, maliyet sınırının sayısal bir tavan
içermesini ve sözleşmenin Bölüm 14'teki bir alt başlığa doğrudan başvurmasını denetler.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-2-loops/checkpoints/security-contract/security_contract_lab.html>
İsterseniz `security_contract_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz. Sayfa tek başına çalışır; kurulum ve internet bağlantısı gerekmez.
Temsilî Vardiya sözleşmesini kendi projenize göre değiştirip **Sözleşmeyi Doğrula**
düğmesine basın.

**Kod biliyorsanız:** Aynı kabul kriterlerini saf Python sürümüyle denetleyin.

```bash
python3 security_contract_lab.py
python3 security_contract_lab.py kendi_sozlesmem.json
python3 -m pytest test_security_contract_lab.py
```

İlk komut gömülü Vardiya örneğini denetler. İkinci komut verdiğiniz JSON dosyasını
okur; dosyaya yazmaz. Üçüncü komut eksik bölümün, gerekçesiz kararın, yanlış izin
katmanının, sırasız sızıntı adımlarının ve hassas veri örüntüsünün reddedildiğini sınar.

## Beklenen Çıktı

```text
Güvenlik Sözleşmesi Denetimi
Veri kuralı: 3 (kategori: 3/3)
Secret yönetimi: 2 yok sayılan yol, 3 olay adımı
İzin kuralı: 6 (allow: 2, ask: 2, deny: 2)
Korumalı alan: 3
Loop sınırı: 3/3
Kabul kriteri karşılandı: Beş bölüm ve karar gerekçeleri tamam.
```

Bir ölçüt karşılanmazsa sonuç başarılı sayılmaz. Doğrulayıcı eksik bölümü veya
yanlış kararı ayrı satırda gösterir.

## Kabul Kriteri

- [x] Kurulum adımları açık; uygulama saf Python 3 ve tek dosyalık HTML ile çalışıyor.
- [x] Veri sınıflandırmasının üç kararı ayrı örneklerle denetleniyor.
- [x] Secret taramasının yeri ve rotasyonla başlayan üç olay adımı doğrulanıyor.
- [x] En az beş işlemde `allow`, `ask` ve `deny` kararları gerekçeleriyle aranıyor.
- [x] En az üç korumalı alan yalnızca `ask` veya `deny` katmanında kabul ediliyor.
- [x] Loop için yetki, sayısal maliyet tavanı ve veri sınırı ayrı ayrı aranıyor.
- [x] Bölüm 14 alt başlık referansı ve hassas veri örüntüsü denetleniyor.
- [x] Python örneği çalışıyor (`python3 security_contract_lab.py`).
- [x] Test komutu ve beklenen çıktı gösteriliyor.
- [x] Riskler ve sınırlar aşağıda açıklanıyor.
- [x] Web bölüm sayfasından doğrudan bağlantı verilebilir.

## Riskler ve Sınırlar

- Gömülü Vardiya sözleşmesi temsilîdir. Her ekip veri hassasiyetini, yetki sınırını
  ve maliyet tavanını kendi sistemine göre belirlemelidir.
- Doğrulayıcı sözleşmenin yapısını ve açık gerekçeleri denetler. Yazılı bir `deny`
  kararı, kullanılan aracın gerçek izin ayarını tek başına değiştirmez.
- Hassas veri denetimi açık e-posta adreslerini ve yaygın gizli bilgi atamalarını
  yakalar. Serbest metindeki bütün kişisel verileri belirleyemez; insan incelemesi
  gerekir.
- Maliyet sınırında bir sayı bulunması, o tavanın doğru seçildiğini kanıtlamaz.
  Tavan, görevin süresine ve çağrı maliyetine göre ayrıca değerlendirilmelidir.
- Laboratuvar secret tarayıcı, CI hattı veya sandbox başlatmaz. Bu kontrollerin gerçek
  projede çalıştığı ayrıca doğrulanmalıdır.

---
volume: 1
chapter: 5
book_section: "5.9 Çakışan Talimatlar Nasıl Çözülür? / 5.10 Prompt Injection Fikrine Giriş: Talimat Hiyerarşisi Neden Önemlidir?"
concepts:
  - Talimat hiyerarşisi
  - Sistem/rol/bağlam/kullanıcı katmanları
  - Prompt injection
  - Doğrudan ihlal ile enjeksiyon ayrımı
objectives:
  - "LO-5.5"   # Çakışan talimatları sabit bir öncelik sırasına (sistem > rol > bağlam > kullanıcı) göre çözebilir.
  - "LO-5.6"   # Talimat hiyerarşisinin prompt injection riskine karşı neden ilk savunma katmanı olduğunu, ancak tek başına yeterli olmadığını değerlendirebilir.
last_verified: "2026-07"
---

# Talimat Hiyerarşisi Çözümleyici

**Kitap bağlantısı:** Cilt 1, Bölüm 5 — Sistem, Rol ve Bağlamsal Promptlar, 5.9-5.10.

## Ne Yapar?

Gerçek bir model çağırmaz. Bir konuşmadaki sistem, rol, bağlam ve kullanıcı talimatlarını
serbest metin olarak "anlamaya" çalışmaz; her talimatı önceden etiketlenmiş
(`katman`, `konu`, `yön`, `kaynak`, `kategori`) yapılandırılmış bir kayıt olarak alır ve
kitaptaki 5.9 hiyerarşi kuralını saf kurallarla uygular:

- **Aynı konu, farklı yön** taşıyan iki (veya daha fazla) talimatı bir **çatışma** olarak
  tespit eder (ör. `konu="tam_cozum"`, biri `yon="ver"` biri `yon="verme"` diyorsa).
- Çatışmayı 5.9'daki sıralamaya göre çözer: **sistem > rol > bağlam > kullanıcı**; aynı
  katmandaki iki talimat çatışırsa **en son tur** (zaman sırası) kazanır; "tercih"
  kategorisindeki konularda (ton, uzunluk, biçim) kullanıcıya en yakın katman öncelik
  kazanır — bu üst katmanı hiyerarşik olarak geçersiz kılmaz, yalnızca o etkileşim için
  uyarlar; "kritik" konularda (güvenlik, gizlilik, etik) üst katmanın vetosu mutlaktır.
- 5.10'daki ayrımı uygular: kaybeden talimat önceki talimatları geçersiz kılmaya çalışan
  bir dil taşıyorsa (ör. "talimatları unut", "boş ver"), kaynağı **kullanıcının kendi
  mesajı** ise bunu "doğrudan ihlal şüphesi", kaynağı **üçüncü taraf bir içerik** (belge,
  web sayfası, e-posta) ise daha ciddi bir "enjeksiyon şüphesi" olarak işaretler ve her iki
  durumda da insan onayı önerir — hiyerarşi doğru sonucu verse (yani saldırı engellense) bile.
- 5.10'daki DİKKAT kutusuna uygun olarak, metin ödeme/veri silme/gizli anahtar paylaşma gibi
  hassas bir eylemden bahsediyorsa, çatışma otomatik çözülmüş olsa dahi insan onayını zorunlu
  işaretler.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/instruction-hierarchy/instruction_hierarchy_lab.html>
İsterseniz `instruction_hierarchy_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Sayfa açıldığında
kitaptaki dört senaryo örnek olarak yüklüdür; satırları düzenleyip "Örnek senaryoları
yükle" veya "+ Talimat ekle" ile kendi senaryonuzu deneyebilirsiniz.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `instruction_hierarchy_lab.py`
dosyasındadır (HTML sürümündeki JavaScript, bu dosyadaki fonksiyonların birebir portudur).

```bash
python3 instruction_hierarchy_lab.py    # demo çıktısı (4 senaryo, terminalde metin olarak)
python3 -m pytest                       # testler (8 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
Senaryo 1 — sistem vs kullanıcı (5.9)
  konu=tam_cozum: kazanan=Sistem ('verme') — şiddet=dogrudan_ihlal_supheli [İNSAN ONAYI GEREKİR]
    gerekçe: Hiyerarşi sırası: Sistem katmanı Kullanıcı katmanını geçersiz kılar.

Senaryo 2 — rol vs bağlam (5.9)
  konu=ton: kazanan=Bağlam ('resmi') — şiddet=otomatik_cozuldu
    gerekçe: Tercihe dayalı konu (ör. ton/uzunluk/biçim); Bağlam katmanının güncel isteği
    öncelik kazanır. Bu, Rol katmanını hiyerarşik olarak geçersiz kılmaz; yalnızca bu
    etkileşim için uyarlar.

Senaryo 3 — aynı katman, iki kullanıcı turu (5.9)
  konu=uzunluk: kazanan=Kullanıcı ('uzun') — şiddet=otomatik_cozuldu
    gerekçe: Aynı katman (Kullanıcı); tur 2 numaralı talimat daha güncel, tur 1'u geçersiz
    kılar (zaman sırası).

Senaryo 4 — üçüncü taraf belgeye gizlenmiş enjeksiyon (5.10)
  konu=talimat_gecerliligi: kazanan=Sistem ('koru') — şiddet=enjeksiyon_supheli [İNSAN ONAYI GEREKİR]
    gerekçe: Kritik konu (güvenlik/gizlilik/etik); mutlak veto: Sistem katmanı Bağlam
    katmanını geçersiz kılar.
```

Dördüncü senaryoda dikkat edilmesi gereken nokta: hiyerarşi doğru çalışır (sistem kazanır,
gizli anahtar paylaşılmaz) ama denetleyici yine de en yüksek şiddet düzeyinde ("enjeksiyon
şüphesi") işaretler — çünkü 5.10'un "mini kontrol" sorusunun ima ettiği gibi, bir saldırının
engellenmiş olması onu görünmez kılmamalıdır; kayıt altına alınıp insana bildirilmelidir.

## Kabul Kriteri

- [x] Kurulum adımları açık (bağımlılık yok, saf Python 3 / saf JavaScript).
- [x] Örnek çalışıyor (`python3 instruction_hierarchy_lab.py`).
- [x] Test/doğrulama komutu var (`pytest`, 8 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).
- [x] Web bölüm sayfasından linklenebilir (bkz. bolum05.md DEPO kutusu).

## Riskler ve Sınırlar

- Bu bir **kural tabanlı denetleyicidir**, gerçek bir dil modeli veya NLP sınıflandırıcısı
  değildir; "çatışma" tespiti, çağıranın önceden verdiği `konu`/`yön` etiketlerine dayanır.
  Serbest metni kendi başına ayrıştırıp çelişkiyi keşfetmez — bu, kitaptaki "değerler
  temsilîdir" notuyla aynı ruhtadır (bkz. `parameter-matrix` lab'ı).
- `override_iddiasi_var_mi` ve `hassas_eylem_iceriyor_mu` fonksiyonları **yüzeysel anahtar
  kelime eşleşmesi** yapar; gerçek bir prompt injection tespit sistemi çok daha gelişmiş
  yöntemler (ayrı sınıflandırıcı modeller, çok katmanlı doğrulama) kullanır. Burada amaç
  5.9-5.10'daki mantığı somutlaştırmaktır, üretim kalitesinde bir güvenlik filtresi
  sağlamak değildir.
- 3 veya daha fazla talimatın aynı konu üzerinde farklı yönlerde çatıştığı gruplar, sırayla
  katlanarak (fold) tek bir kazanana indirgenir; şiddet sınıflandırması ise gruptaki
  **tüm** kaybedenler taranarak belirlenir. Bu, kitaptaki örneklerin tamamını (ikili
  çatışmalar) doğru çözer, ama çok sayıda çelişen talimatın olduğu uç durumlar için basit
  bir genelleme olduğu unutulmamalıdır.
- Kitapta da vurgulandığı gibi (5.10 "Nerede yanılabiliriz?"): hiçbir talimat hiyerarşisi
  uygulaması tam güvenlik sağlamaz. Bu lab bir "insan onayı gerekir" bayrağı üretir, ama
  gerçek bir üründe hassas eylemler için ek, bağımsız bir onay adımı hâlâ zorunludur.

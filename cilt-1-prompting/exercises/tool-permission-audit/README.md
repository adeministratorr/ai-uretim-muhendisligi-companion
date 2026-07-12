---
volume: 1
chapter: 13
book_section: "Yapay Zekâ Ajanları: Kavramlar"
concepts:
  - araç tanımı
  - tool calling
  - parametre sınırı
  - onay noktası
  - yarı otonom çalışma
objectives:
  - "LO-13.4"
  - "LO-13.5"
last_verified: "2026-07"
---

# Araç İzni Denetimi Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 13 — Yapay Zekâ Ajanları: Kavramlar,
13.4-13.5 (araç tanımı, ajanın beş bileşeni) ve 13.10 (araştır-özetle-raporla
örneği, kabul kriterindeki üçlü kontrol).

## Ne Yapar?

13.4'teki GELİŞTİRİCİ NOTU, bir aracın modele adı, kısa açıklaması ve
parametre şemasıyla tanıtıldığını, ama araç listesinin tek başına yeterli bir
sınır olmadığını vurgular: bir araç izinliyse bile hangi parametrelerle
çağrılabileceği ayrıca sınırlanmalıdır. 13.9, geri alınamaz eylemlerin
(gönderme, silme, ödeme gibi) bir onay noktasının arkasında durması
gerektiğini ekler. 13.10'un kabul kriteri bu iki ilkeyi tek bir denetimde
birleştirir: araç listesinde gönderme/silme/ödeme yetkili, parametresi
sınırlanmamış bir araç var mı?

Bu laboratuvar, gerçek bir API çağrısı yapmadan, bir ajana tanımlanan araç
listesini bu üçlü denetimden geçirir:

- `Arac`: bir aracın adı, izinli parametreleri, geri alınabilirlik durumu ve
  onay noktası bilgisini tutan veri sınıfı.
- `araci_denetle`: tek bir aracı denetler; yalnızca **parametre sınırı yok +
  eylem geri alınamaz + onay noktası yok** koşullarının üçü birden
  sağlandığında riskli işaretler.
- `arac_listesini_denetle`: bir ajana tanımlanan tüm listeyi sırayla
  denetler.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü
tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/exercises/tool-permission-audit/tool_permission_audit.html>
İsterseniz `tool_permission_audit.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Araç
satırlarını düzenleyin (ad, izinli parametreler, geri alınabilirlik, onay
noktası); denetim sonucu her değişiklikte anında güncellenir. "+ Araç ekle"
ile kendi örneğinizi ekleyebilir, "Selin'in listesine sıfırla" ile 13.10'daki
örneğe dönebilirsiniz.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `tool_permission_audit.py`
dosyasındadır.

```bash
python3 tool_permission_audit.py   # demo çıktısı (13.10'daki Selin örneği)
python3 -m pytest                  # testler (10 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
- web_oku: güvenli
    · parametre sınırlı: rakip1.com/fiyat, rakip2.com/fiyat, ...
    · eylem geri alınabilir
    · onay noktası tanımlanmamış
- gecmis_raporu_getir: güvenli
- rapor_taslagi_olustur: güvenli
- eposta_gonder: RİSKLİ
    · parametre sınırı yok (herhangi bir değerle çağrılabilir)
    · eylem geri alınamaz
    · onay noktası tanımlanmamış

Toplam 4 araçtan 1 tanesi riskli işaretlendi.
```

`eposta_gonder`, 13.10'un araç listesinde hiç bulunmaz; bu laboratuvara
kabul kriterinin üçüncü kontrolünün ne yakaladığını göstermek için eklenen
hayali bir karşı örnektir — talimatta tarif edilmeyen bir gönderme yetkisinin
araç listesine yanlışlıkla eklenmesi durumunu somutlaştırır.

## Kabul Kriteri

- [x] Kurulum adımları açık (bağımlılık yok, saf Python 3).
- [x] Örnek çalışıyor (`python3 tool_permission_audit.py`).
- [x] Test/doğrulama komutu var (`pytest`, 10 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu denetim yalnızca üç alanı (parametre sınırı, geri alınabilirlik, onay
  noktası) kontrol eder; gerçek bir ajan tasarımında araç izinlerinin doğru
  tanımlanması tek başına yeterli değildir — talimat hiyerarşisi, araç
  çıktısının güvenilmezliği (prompt injection riski) ve guardrail tasarımı
  gibi konular Bölüm 14'ün kapsamındadır.
- "Geri alınabilir" ve "geri alınamaz" ayrımı burada ikili (boolean) bir
  alandır; gerçek dünyada bazı eylemler kısmen geri alınabilir olabilir
  (ör. bir e-posta geri çağrılabilir ama okunmuşsa etkisi sürer) — bu
  nüans kitaptaki 13.9'un anlattığı ilkeye aykırı değildir, yalnızca bu
  laboratuvarın basitleştirmesidir.
- Bu araç, bir ajan çatısına (framework) veya gerçek bir modele bağlanmaz;
  girdiğiniz araç tanımları üzerinde saf mantık çalıştırır, riski otomatik
  olarak "gidermez", yalnızca görünür kılar.

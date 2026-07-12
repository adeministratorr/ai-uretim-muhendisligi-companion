---
volume: 1
chapter: 11
book_section: "AI Çıktısını Değerlendirmek"
concepts:
  - güvenilirlik piramidi
  - fact-checking
  - kaynak kontrolü
  - birincil ve ikincil kaynak
last_verified: "2026-07"
objectives:
  - "LO-11.2"
  - "LO-11.3"
---

# Güvenilirlik Piramidi Denetleyicisi

**Kitap bağlantısı:** Cilt 1, Bölüm 11 — AI Çıktısını Değerlendirmek, 11.5
(Güvenilirlik Piramidi), 11.6 (Fact-Checking Stratejileri), 11.7 (Kaynak
Kontrolü) ve 11.8 (Birincil Kaynak, İkincil Kaynak ve Kullanıcı Doğrulaması).

## Ne Yapar?

Gerçek bir API çağrısı yapmadan, bir AI çıktısından ayrılmış iddiaları
(claim) listeye alıp her biri için üç şeyi zorunlu kılan saf bir denetim
mantığı sunar:

- İddia **kritik mi** (piramidin tepesi — hukuki/tıbbi/finansal sonuç veya
  itibar riski doğurabilecek bir iddia mi, 11.5 ve 11.13)?
- İddia hangi **kanıt kademesinde**: kendi bilgin (modelin kaynaksız ezberi),
  genel bilgi, doğrulanabilir kaynak (11.8'deki ikincil kaynak) veya birincil
  kaynak?
- Kaynak varsa **adı belirtilmiş mi** (11.7) ve kullanıcı bizzat **doğrulamış
  mı** (11.8'deki "bir kaynak var" ile "bu kaynak bu cümleyi destekliyor"
  ayrımı)?

Bu üç girdiden hareketle her iddiayı `hazır` / `uyarı` / `hata` olarak
işaretler. Kaynaksız kritik iddialar (piramidin tepesinde ama kendi
bilgi/genel bilgi kademesinde bırakılmış iddialar) **uyarı** üretir; kaynak
adı verilmeden "doğrulanabilir kaynak" veya "birincil kaynak" seçilmesi
**hata** üretir, çünkü kaynağın adı olmadan bu kademenin bir anlamı yoktur.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü
tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/reliability-check/reliability_check_lab.html>
İsterseniz `reliability_check_lab.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. "+ İddia
Ekle" ile kendi iddialarınızı girin veya "Kitaptaki örneği yükle" ile 11.11'deki
dört iddialık örneği görün; her alan değiştiğinde sonuç anında güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `reliability_check_lab.py`
dosyasındadır.

```bash
python3 reliability_check_lab.py     # demo çıktısı (kitaptaki 11.11 örneği, terminalde metin olarak)
python3 -m pytest                    # testler (9 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
[HAZIR] İlçede son iki yılda küçük işletme sayısı arttı
  Kademe: Doğrulanabilir kaynak (ikincil kaynak)
[UYARI] Bir yetkili bu artışın teşvik programından kaynaklandığını söyledi
  Kademe: Kendi bilgin (modelin ezberi, kaynaksız)
[UYARI] Artış oranı yaklaşık yüzde 18
  Kademe: Genel bilgi (yaygın, tartışmasız)
[HAZIR] İlçenin nüfusu resmî kayıtlara göre yaklaşık 42 bin
  Kademe: Birincil kaynak (olayı doğrudan üreten kaynak)

İddia: 4 | Hata: 0 | Uyarı: 2 | Durum: ek doğrulama gerekli
```

İki iddia (yetkili alıntısı ve yüzde 18 oranı) kritik işaretlenmiş ama
kaynaksız kaldığı için uyarı alır — kitaptaki 11.11 tablosunda bu iki
iddianın da doğrulanamadığı veya yalanlandığı için metinden çıkarıldığı
ya da ertelendiği anlatılır.

## Kabul Kriteri

- [x] Kurulum adımları açık (bağımlılık yok, saf Python 3).
- [x] Örnek çalışıyor (`python3 reliability_check_lab.py`).
- [x] Test/doğrulama komutu var (`pytest`, 9 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu araç bir iddianın **gerçekten doğru olup olmadığını** denetlemez;
  yalnızca kullanıcının doğrulama disiplinini (11.6'daki dört fact-checking
  adımı) uygulayıp uygulamadığını biçimsel olarak görünür kılar. "Hazır"
  durumu, iddianın doğru olduğunun kanıtı değildir.
- Kritik/kanıt kademesi işaretlemesi tamamen **kullanıcı beyanına** dayanır;
  araç bir iddianın gerçekten kritik olup olmadığını veya girilen kaynak
  adının gerçekten var olup olmadığını kendi başına doğrulayamaz.
- "Kullanıcı doğrulaması" onay kutusu, kaynağın gerçekten kontrol edildiğinin
  değil, kullanıcının bunu beyan ettiğinin işaretidir; sahte biçimde
  işaretlenebilir. Hukuk, sağlık, finans ve akademik alanlarda (11.13) bu
  aracın çıktısı uzman onayının yerine geçmez.

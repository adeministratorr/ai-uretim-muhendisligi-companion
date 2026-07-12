---
volume: 1
chapter: 10
book_section: "Yapay Zekâ ile Günlük Hayat ve İş Akışları"
concepts:
  - etki/efor matrisi
  - risk/değer matrisi
  - insan onayı noktası
  - yüksek riskli karar alanı
objectives:
  - "LO-10.6"
  - "LO-10.7"
last_verified: "2026-07"
---

# Etki/Efor ve Risk/Değer Değerlendirme Şablonu

**Kitap bağlantısı:** Cilt 1, Bölüm 10 — Yapay Zekâ ile Günlük Hayat ve İş Akışları,
10.12 (Etki/Efor Matrisi), 10.13 (Risk/Değer Matrisi) ve 10.16 (Yapay Zekâ Ne Zaman
Kullanılmamalı?).

## Ne Yapar?

Bölüm 10, onlarca aday iş akışının hepsini aynı anda kurmanın zamanın çoğunu
kurulum işine harcamak anlamına geldiğini gösterir; bir öncelik sırası gerekir.
Etki/efor matrisi "bunu kurmaya değer mi?" sorusuna, risk/değer matrisi ise "bu
çıktıya ne kadar güvenilebilir, ne kadar denetim gerekir?" sorusuna cevap verir.
Aynı görev iki matriste farklı köşeye düşebilir.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, doldurduğunuz bir görev
listesini iki matriste sınıflandırır ve tek bir öncelik sırasına dizer:

- `impact_effort_matrix.py`: her görevi etki/efor matrisinin dört çeyreğinden
  ve risk/değer matrisinin dört çeyreğinden birine yerleştirir; iki çeyrek
  sırasının en kötüsünü alarak birleşik bir öncelik puanı üretir.
- `gorev_listesi_ornek.json`: kitaptaki Aylin örneklerinden (müşteri mesajı,
  toplantı notu, sosyal medya, sipariş takip sistemi, kozmetik etiket
  araştırması, vergi beyanı gibi) türetilmiş dokuz görevlik dolu bir liste.
- `gorev_listesi_sablonu.json`: kendi görev listenizi kurmaya başlamak için
  boş bir dosya (`[]`); `gorev_listesi_ornek.json`'daki alan adlarını izleyerek
  kendi görevlerinizi ekleyin.

Vergi beyanı gibi hukuk, sağlık, finans veya kişisel veri içeren görevler
`yuksek_riskli_alan: true` ile işaretlenebilir; bu görevler matris puanından
bağımsız olarak ayrı etiketlenir ve sıralamanın sonuna bırakılır (bkz. 10.16).

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü
tarayıcınızda açın:
<https://lab.ademyuce.tr/cilt-1-prompting/exercises/impact-effort-matrix/impact_effort_matrix.html>
İsterseniz `impact_effort_matrix.html` dosyasını indirip çift tıklayarak da
açabilirsiniz; kurulum, terminal veya internet bağlantısı gerekmez. Kaydırıcılarla
bir görev girip "Görevi ekle"ye basın; görev hem iki matrisin görsel ızgarasında
bir nokta olarak, hem de öncelik tablosunda bir satır olarak canlı görünür. "Örnek
listeyi yükle" düğmesi kitaptaki dokuz görevlik örneği yükler.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `impact_effort_matrix.py`
dosyasındadır. Önce şablonu kopyalayıp kendi görev listenizi doldurun:

```bash
cp gorev_listesi_sablonu.json benim_gorevlerim.json
# benim_gorevlerim.json içine gorev_listesi_ornek.json'daki alan adlarıyla
# ({"ad": ..., "etki": 1-5, "efor": 1-5, "risk": 1-5, "deger": 1-5}) görev ekleyin
python3 impact_effort_matrix.py benim_gorevlerim.json
```

Hazır örneği görmek için:

```bash
python3 impact_effort_matrix.py
python3 -m pytest -q
```

## Beklenen Çıktı (özet)

```text
9 görev değerlendirildi.

1. Müşteri mesajı cevap taslağı
   Etki/Efor: hızlı kazanç → Önce bunlar kurulur
   Risk/Değer: düşük risk / yüksek değer → Düşük düzeyde insan onayıyla kurulabilir
   Öncelik 1 — hemen kurulmaya uygun
...
9. Vergi beyanı taslağı
   Etki/Efor: hızlı kazanç → Önce bunlar kurulur
   Risk/Değer: yüksek risk / yüksek değer → Kurulur ama sıkı onay noktası zorunlu
   Yüksek riskli karar alanı (10.16) — matris puanından bağımsız olarak tam
   otomasyon önerilmez; ilgili alanın uzmanı onaylamadan uygulanmaz.
```

Vergi beyanı taslağı, etki/efor ekseninde "hızlı kazanç" görünse bile, yüksek
riskli karar alanı işaretlendiği için listenin en sonuna bırakılır — bu, tek bir
puanın hiçbir zaman uzman onayının yerini almadığını gösterir.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3, gerçek API çağrısı yok).
- [x] Örnek çalışıyor (`python3 impact_effort_matrix.py`).
- [x] Test/doğrulama komutu var (`pytest`, 10 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu araç bir kararı otomatik onaylamaz; yalnızca girdiğiniz 1-5 puanlarına göre
  bir öncelik sırası önerir. Puanların kendisi (etki, efor, risk, değer) sizin
  öznel değerlendirmenizdir; araç bu değerlendirmeyi doğrulamaz.
- Dört alanlı 1-5 ölçeği, kitaptaki iki ayrı ikili (düşük/yüksek) matrisin bir
  basitleştirmesidir; gerçek kararlarda daha ince ayrımlar gerekebilir.
- `yuksek_riskli_alan` işareti yalnızca görünürlük sağlar; hukuk, sağlık, finans
  veya kişisel veri içeren bir görevi otomatikleştirmeden önce mutlaka ilgili
  alanın uzmanına danışılmalıdır (bkz. kitap 10.16). Bu araç uzman onayının
  yerine geçmez.

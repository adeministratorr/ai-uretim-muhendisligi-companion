---
volume: 1
chapter: 15
book_section: "Yapay Zekâ Öncüsü Şirketlerden Dersler"
concepts:
  - evals
  - veri yönetişimi
  - pilot ölçümleme
  - geri çekilme eşiği
objectives:
  - "LO-15.6"
  - "LO-15.7"
last_verified: "2026-07"
---

# Yapay Zekâ Pilotu Ölçüm Kartı Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 15 — Yapay Zekâ Öncüsü Şirketlerden Dersler,
15.1, 15.8, 15.9 ve 15.10.

## Ne Yapar?

Gerçek bir API çağrısı yapmadan, bölüm sonundaki beş alanlı pilot tasarımını küçük
bir denetim kartına dönüştürür:

- `pilot_template.json`: hedef, kullanıcı grubu, veri riski, başarı metriği ve pilot
  sonrası karar kriteri için doldurulabilir şablon.
- `case_table.json`: bölümde anılan şirket vakalarını yaşayan tablo biçiminde tutar.
  Bu satırlar kaynak doğrulaması beklediğini açıkça gösterir; doğrulanmış kaynak gibi
  sunulmaz.
- `ai_pilot_scorecard.py`: doldurulan pilot dosyasının ölçülebilirlik, veri riski ve
  geri çekilme eşiği açısından eksiklerini listeler.

## Nasıl Kullanılır?

Önce şablonu kopyalayıp kendi pilot fikrinizi doldurun:

```bash
cp pilot_template.json benim_pilotum.json
python3 ai_pilot_scorecard.py benim_pilotum.json
```

Hazır örneği görmek için:

```bash
python3 ai_pilot_scorecard.py
python3 -m pytest -q
```

## Beklenen Çıktı (özet)

```text
Yaşayan vaka tablosu: Vaka satırı: 10 | Kaynak doğrulaması bekleyen: 10
Durum: geçti
Tamamlanan kontrol: 9/9
Kabul kriteri geçti: beş alan ve dört ölçüt dolduruldu.
```

Bu çıktı, pilotun iyi bir fikir olduğunu kanıtlamaz. Yalnızca tasarımın ölçülebilir
yazıldığını, veri riskinin işaretlendiğini ve başarısızlık durumunda ne yapılacağının
önceden tanımlandığını gösterir.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3, gerçek API çağrısı yok).
- [x] Örnek çalışıyor (`python3 ai_pilot_scorecard.py`).
- [x] Test/doğrulama komutu var (`pytest`, 5 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu araç bir yapay zekâ pilotunu otomatik onaylamaz; yalnızca eksik alanları ve zayıf
  karar eşiğini görünür kılar.
- `case_table.json` yaşayan tablo iskeletidir. Bölümdeki vaka satırları kaynak
  doğrulaması tamamlanana kadar karar dayanağı olarak kullanılmamalıdır.
- Ölçülebilirlik denetimi basit anahtar sözcük ve eşik kontrolleriyle yapılır. Kritik
  kurumsal pilotlarda insan değerlendirmesi ve hukuk/güvenlik kontrolü gerekir.

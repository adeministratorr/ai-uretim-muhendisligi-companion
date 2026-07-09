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

Bölüm 15'in dersi, yapay zekâ pilotunu heves üzerine değil, ölçüm üzerine
kurmaktır. Beş alanlı tasarım pilotun hedefini, kullanıcı grubunu, veri riskini,
başarı metriğini ve pilot sonrası kararı daha başlamadan yazıya bağlar; geri
çekilme eşiği ise hangi sonuçta pilotun durdurulacağını önceden tanımlar.
Başarısız pilotu erken ve ucuz bitirmenin güvencesi budur.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, bölüm sonundaki beş alanlı pilot
tasarımını küçük bir denetim kartına dönüştürür:

- `pilot_template.json`: hedef, kullanıcı grubu, veri riski, başarı metriği ve pilot
  sonrası karar kriteri için doldurulabilir şablon.
- `case_table.json`: bölümde anılan şirket vakalarını tablo biçiminde tutar.
  Bu satırlar kaynak doğrulaması beklediğini açıkça gösterir; doğrulanmış kaynak gibi
  sunulmaz.
- `ai_pilot_scorecard.py`: doldurulan pilot dosyasının ölçülebilirlik, veri riski ve
  geri çekilme eşiği açısından eksiklerini listeler.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/exercises/ai-pilot-scorecard/ai_pilot_scorecard.html>
İsterseniz `ai_pilot_scorecard.html` dosyasını indirip çift tıklayarak da açabilirsiniz;
kurulum, terminal veya internet bağlantısı gerekmez. Örnek pilotu yükleyin veya boş
şablonla kendi pilot fikrinizi doldurun; kontrol sonucu canlı güncellenir.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `ai_pilot_scorecard.py`
dosyasındadır. Önce şablonu kopyalayıp kendi pilot fikrinizi doldurun:

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
Vaka tablosu: Vaka satırı: 10 | Kaynak doğrulaması bekleyen: 10
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
- `case_table.json` tablo iskeletidir. Bölümdeki vaka satırları kaynak
  doğrulaması tamamlanana kadar karar dayanağı olarak kullanılmamalıdır.
- Ölçülebilirlik denetimi basit anahtar sözcük ve eşik kontrolleriyle yapılır. Kritik
  kurumsal pilotlarda insan değerlendirmesi ve hukuk/güvenlik kontrolü gerekir.

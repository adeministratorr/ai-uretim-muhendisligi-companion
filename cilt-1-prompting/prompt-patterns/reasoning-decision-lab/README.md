# Karar Gerekçesi ve Pilot Plan Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 6 — Akıl Yürütme ve Problem Çözme Teknikleri, 6.6 ve 6.8.

```yaml
volume: 1
chapter: 06
book_section: "Akıl Yürütme ve Problem Çözme Teknikleri"
concepts:
  - Tree of Thoughts
  - gerekçeli çıktı
  - planla-uygula-kontrol et döngüsü
  - görev ayrıştırma
objectives:
  - LO-6.4
  - LO-6.5
  - LO-6.6
last_verified: "2026-07"
```

## Ne Yapar?

Gerçek bir API çağrısı yapmadan, Bölüm 6'daki Derya ve 142 numaralı hat
vakasını küçük bir karar laboratuvarına çevirir:

- `build_tree_of_thoughts_prompt`: üç karar dalını ve üç kriteri aynı promptta
  açık biçimde adlandırır.
- `rank_branches`: sefer sıklığı, mahalle erişimi ve bütçe kısıtı kriterlerini
  ağırlıklı puana çevirir.
- `score_branch`: eksik kriteri veya bütçe aşımını uygulanabilirlik engeli
  olarak işaretler.
- `build_pilot_plan`: önerilen dal için dört haftalık pilot planı üretir.
- `validate_pilot_plan`: pilot planın sayısal eşik ve "karşılanmazsa ne olur"
  adımı taşıyıp taşımadığını denetler.

Bu laboratuvar modelin gizli düşünmesini taklit etmez. Bölümün temel ayrımını
uygular: düşünce dökümü değil, kontrol edilebilir gerekçe.

## Nasıl Kullanılır?

Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/prompt-patterns/reasoning-decision-lab
python3 reasoning_decision_lab.py
python3 -m pytest
```

İnternet bağlantısı veya API anahtarı gerekmez. Testler yalnızca Python standart
kütüphanesi ve `pytest` ile çalışır.

## Beklenen Çıktı (özet)

```text
== Tree of Thoughts tablo özeti ==
| Dal | Toplam puan | Durum |
|---|---:|---|
| C - Besleyici hat ekle | 37 | uygulanabilir |
| A - Sefer sıklığını artır | 27 | uygulanabilir |
| B - Hattı ikiye böl | 21 | uygulanabilir |

Önerilen dal: C - Besleyici hat ekle
Gerekçe puanı: 37

== Pilot plan kontrolü ==
Süre: 4 hafta
- Yeşiltepe kaynaklı şikâyet sayısı: 4 hafta sonunda en az %50 azalma
- besleyici hat doluluk oranı: haftalık ortalama %30'un altına düşmemeli
- sabah ana hat doluluk oranı: 07:00-09:00 aralığında %85'in altına inmeli
Doğrulama: geçti
```

Besleyici hat dalı, erişim sorununu doğrudan çözdüğü ve bütçe kısıtını aşmadığı
için öne çıkar. Pilot plan ise öneriyi tek seferlik karara çevirmek yerine
ölçülebilir bir deneme haline getirir.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 reasoning_decision_lab.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu örnek gerçek model çıktısını ölçmez; karar dallarını yerel ve şeffaf
  kurallarla puanlar.
- Ağırlıklar temsilîdir. Kurumsal karar için gerçek yolcu sayımı, maliyet ve saha
  verisi gerekir.
- Sayısal eşik bulunması planı doğru yapmaz. Eşiklerin sahadaki karşılığı insan
  tarafından kontrol edilmelidir.
- Model adı, fiyat veya benchmark iddiası içermez; güncel model bilgisi için
  `docs/model-watch/README.md` kullanılmalıdır.

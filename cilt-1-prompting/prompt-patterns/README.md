# Prompt Anatomisi — Şablon ve Denetim Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 3 — Etkili Prompt'un Anatomisi, 3.2-3.10.

```yaml
volume: 1
chapter: 03
book_section: "Etkili Prompt'un Anatomisi"
concepts:
  - persona
  - görev
  - bağlam
  - format
  - kısıt
  - başarı kriteri
  - değişkenli prompt şablonu
objectives:
  - LO-3.2
  - LO-3.3
  - LO-3.4
  - LO-3.5
last_verified: "2026-07"
```

## Ne Yapar?

Gerçek bir API çağrısı yapmadan, Bölüm 3'teki prompt bileşenlerini küçük bir
Python denetimine çevirir:

- `PromptRecipe`: persona, görev, bağlam, format, kısıt ve başarı kriteri
  alanlarını ayrı tutar.
- `audit_recipe`: eksik bileşenleri bulur ve tarifi zayıf/iyi/profesyonel
  düzeylerinden birine yerleştirir.
- `render_recipe`: köşeli parantezli değişkenleri doldurur; eksik değişken
  varsa çalışmayı durdurur.

Bu laboratuvar serbest metni yorumlayan bir yapay zekâ denetçisi değildir.
Promptu, bölümde anlatıldığı gibi yapılandırılmış bir iş tarifi olarak ele alır.

## Nasıl Kullanılır?

Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/prompt-patterns
python3 prompt_anatomy_lab.py
python3 -m pytest
```

## Beklenen Çıktı (özet)

```text
== Zayıf tarif ==
Düzey: zayıf
Eksik parçalar: persona, bağlam, format, kısıt, başarı kriteri

== İyi tarif ==
Düzey: iyi
Eksik parçalar: persona, bağlam, kısıt, başarı kriteri

== Profesyonel tarif ==
Düzey: profesyonel
Eksik parçalar: yok
Açık değişken: yok
```

Zayıf tarif yalnızca işi adlandırır. İyi tarif görev ve formatı belirtir.
Profesyonel tarif ise promptu kabul edilebilir bir çıktı üretecek iş tarifine
dönüştürür.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 prompt_anatomy_lab.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu örnek gerçek model çıktısını değerlendirmez; yalnızca yapılandırılmış prompt
  tarifinin eksik bileşenlerini denetler.
- Başarı kriterinin "kontrol edilebilir" sayılması basit işaretlere dayanır
  (`en az`, `her`, `hiçbir`, sayı vb.). Kritik işlerde insan denetimi gerekir.
- Değişken doldurmak doğruluk garantisi vermez. Kaynak, veri ve model davranışı
  ayrıca kontrol edilmelidir.

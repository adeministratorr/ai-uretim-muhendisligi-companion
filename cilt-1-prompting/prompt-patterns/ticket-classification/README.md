# Talep Sınıflandırma — Few-Shot ve Şema Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 4 — Temel Prompt Kalıpları, 4.3-4.11.

```yaml
volume: 1
chapter: 04
book_section: "Temel Prompt Kalıpları"
concepts:
  - zero-shot prompting
  - one-shot prompting
  - few-shot prompting
  - karşı örnek
  - yapılandırılmış çıktı
  - şema
  - açık talimat
objectives:
  - LO-4.1
  - LO-4.2
  - LO-4.3
  - LO-4.4
  - LO-4.5
last_verified: "2026-07"
```

## Ne Yapar?

Bölüm 4'teki kalıpların özü örnek yönetimidir. Zero-shot prompt görevi yalnızca
tarif eder; one-shot tek örnekle çıktı biçimini sabitler; few-shot ise dengeli
örnekler ve sınır durumlarını gösteren karşı örneklerle modelin karar çizgisini
netleştirir. Şema, çıktının alanlarını önceden sözleşmeye bağlar; doğrulama da bu
sözleşmenin tutulup tutulmadığını kontrol eder.

Bu laboratuvar, gerçek bir API çağrısı yapmadan, Bölüm 4'teki müşteri destek
talebi örneğini çalışan bir laboratuvara çevirir:

- `build_zero_shot_prompt`: görevi örneksiz tarif eder.
- `build_one_shot_prompt`: tek örnekle biçimi sabitler.
- `build_few_shot_prompt`: dengeli örnek seti, karşı örnek çifti ve JSON şemasıyla
  nihai promptu kurar.
- `classify_ticket_locally`: aynı örnekler üzerinde küçük ve yerel bir sınıflandırma
  kuralı çalıştırır.
- `validate_ticket_output`: çıktının kategori, aciliyet, özet ve önerilen ilk cümle
  alanlarını şemaya göre denetler.

Bu laboratuvar model davranışını taklit etmeye çalışmaz. Amaç, prompt kalıbı ile
çıktı doğrulaması arasındaki farkı görünür kılmaktır.

## Nasıl Kullanılır?

Terminalde bu klasöre geçin:

```bash
cd cilt-1-prompting/prompt-patterns/ticket-classification
python3 ticket_classification_lab.py
python3 -m pytest
```

İnternet bağlantısı veya API anahtarı gerekmez. Testler yalnızca Python standart
kütüphanesi ve `pytest` ile çalışır.

## Beklenen Çıktı (özet)

```text
== Zero-shot ==
Satır sayısı: 1

== One-shot ==
Satır sayısı: 4

== Few-shot + şema ==
Satır sayısı: 21

== Şema çıktısı ==
{"kategori": "İade", "aciliyet": "Normal", "ozet": "Müşteri iade veya değişim sürecinin başlatılmasını istiyor.", "onerilen_ilk_cumle": "İade süreci için gerekli adımları hemen kontrol ediyoruz."}
Doğrulama: geçti
```

Zero-shot prompt yalnızca görevi söyler. One-shot prompt biçimi gösterir. Few-shot
prompt ise örnek çeşitliliğini, karşı örneği, şemayı ve açık talimatı aynı yerde
toplar.

## Kabul Kriteri

- [x] Kurulum adımları açık (saf Python 3; test için `pytest`).
- [x] Örnek çalışıyor (`python3 ticket_classification_lab.py`).
- [x] Test/doğrulama komutu var (`python3 -m pytest`, 6 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu örnek gerçek model çıktısını ölçmez; prompt tasarımı ve çıktı doğrulamasını
  yerel olarak gösterir.
- Yerel sınıflandırıcı küçük anahtar kelime kuralları kullanır; canlı müşteri
  destek yönlendirme sistemi değildir.
- Şema biçimi denetler, doğru kategori seçimini garanti etmez. Kritik işlerde
  retry, fallback veya insan onayı gerekir.

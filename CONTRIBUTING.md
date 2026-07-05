# Katkı Rehberi

Bu depo, kitabın okurlarından katkı kabul eder. Katkı göndermeden önce bu dosyayı okuyun.

## Kabul Edilen Katkı Türleri

- Minimal, uçtan uca çalışan demo.
- Prompt/loop/eval şablonu.
- Agent hata vakası ve çözüm notu.
- Model/araç uyumluluk güncellemesi.
- Web sayfası veya dokümantasyon düzeltmesi.

## Kabul Kriterleri

Bir katkının kabul edilmesi için:

- Çalıştırma adımları açık olmalı.
- Test veya doğrulama adımı bulunmalı.
- Gerçek kişisel veri, secret veya telif riski taşımamalı.
- Tek bir modeli veya aracı reklam gibi parlatmamalı.
- Türkçe açıklama ve gerektiğinde İngilizce terim birlikte verilmeli.

## Yeni Örnek/Lab Eklerken

Yeni bir örnek, lab, tool, MCP server, eval veya production akışı eklemeden önce
`SPEC_TEMPLATE.md` dosyasını doldurun ve PR açıklamasına ekleyin.

## Commit Biçimi

`tip(kapsam): kısa açıklama` — tipler: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
Örnek: `feat(cilt-1): few-shot prompt şablonu eklendi`.

## Davranış Sözleşmesi

Bu repoda çalışan insan katkıları ve coding agent'lar `AGENTS.md` dosyasındaki kurallara
tabidir (özellikle Bölüm 3 "Yasaklı Davranışlar" ve Bölüm 6 "Tool Permission Kuralı").

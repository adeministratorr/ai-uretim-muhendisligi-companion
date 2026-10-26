# Yapay Zekâ ile Üretim Atölyesi: Pusula

Promptlarla proje kurma, skill geliştirme ve ajan sistemlerini doğrulama uygulamaları.

Bu paket, Yapay Zekâ ile Üretim Mühendisliği serisinin dört cildi ile Claude Code rehberini bir uygulama serisinde birleştiren kitap taslağıdır. Çalışma adı Pusula olan yeni proje, kaynaklı araştırma ve karar taslağı hazırlamaya odaklanır. Vardiya örneğinden bağımsızdır.

**Sürüm 0.1.0:** Kitap planı, 36 uygulama promptu, proje dosyası üretim sırası, iki örnek skill ve sentetik veri bulunur. Pusula uygulama kodu ve 36 uygulamanın çalıştırma sonuçları henüz üretilmedi. Dosya denetiminin geçmesi promptların modelle sınandığını göstermez.

## Başlangıç

1. [Kitap planını](KITAP_PLANI.md) ve [proje brifini](brief.md) okuyun.
2. Kendi boş uygulama dizininize `brief.md` dosyasını ve `fixtures/` dizinini kopyalayın. Companion deposunun kökünü uygulama çalışma alanı olarak kullanmayın.
3. Ajanınıza [ortak çalışma sözleşmesini](prompts/00-calisma-sozlesmesi.md) ve [ilk promptu](prompts/01.md) birlikte verin. `[UYGULAMA_KOKU]` yerine kendi boş çalışma dizininizin yolunu yazın.
4. Üretilen dosyaları kontrol edin; ardından [uygulama sırasındaki](UYGULAMALAR.md) bir sonraki adıma geçin. Eksik girdiyi varsayımla tamamlamayın.
5. [Referans belge paketini](reference/README.md) kendi çıktınızla karşılaştırın. Bu paket öğretim için hazırlanmış bir örnektir. Ayrı model oturumlarında çalıştırılmış promptların ham çıktısını içermez.

## Pakette ne var?

- [Kitap fikri ve bölüm düzeni](KITAP_PLANI.md)
- [36 uygulama ve üretilecek dosyalar](UYGULAMALAR.md)
- [Proje dosyalarının görevleri](DOSYA_MIMARISI.md)
- [Kaynak kitapların 100 bölümüne eşleme](KAPSAM.md)
- [Güncel yaklaşımlar ve birincil kaynaklar](YAKLASIMLAR.md)
- [Skill kullanım ve deneme düzeni](SKILLS.md)
- [Üretim aşamaları](URETIM_PLANI.md)
- [Doğrulama kapsamı](DOGRULAMA.md)

Depo kökünden yalnız paket yapısını denetlemek için:

```sh
python3 uygulama-kitabi/pusula/tools/validate_package.py
```

Bu komut ağ veya model çağrısı yapmaz, uygulama kurmaz ve dosya değiştirmez. Sonuç yalnız dosya yolları, uygulama bağımlılıkları, bölüm eşlemesi, JSON ve skill girişlerinin sınırlı biçim denetimidir.

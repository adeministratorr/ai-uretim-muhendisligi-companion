# Pusula uygulama kitabı başlangıç paketi

## Kısa tanım

Mevcut iki kaynak grubunu, farklı bir örnek proje üzerinde promptlarla dosya üreten uygulama serisine dönüştürmek. İlk teslim kitap planı, uygulama promptları, örnek belgeler ve skill paketleridir.

## Kitap bağlantısı

Yapay Zekâ ile Üretim Mühendisliği Cilt 1–4 ve Claude Code rehberi. Bölüm numaraları coverage.json içinde, yeni uygulama numaraları curriculum.json içinde tutulur.

## Okur ve araçlar

Başlangıç uygulamaları Markdown dosyaları ve bir kodlama ajanıyla yürütülür. Paket doğrulayıcısı Python 3 standart kitaplığı kullanır. İleri uygulamaların bağımlılıkları ilgili uygulama başlamadan sürümlenir.

## Kabul ölçütleri

- 36 uygulama için girdi, çıktı, üretim, kontrol ve düzeltme promptu bulunur.
- 100 kaynak bölümün her biri en az bir uygulamaya bağlanır; kapsam düzeyi açık yazılır.
- Proje belgelerinin üretim sırası eksik veya ileri aşamada üretilecek bir girdiye dayanmaz.
- İki skill örneğinin giriş dosyası, gerekli başvuru kaynağı ve deneme vakaları vardır.
- Sentetik veri ve örnek çıktılar gözlenmiş model sonucu olarak sunulmaz.
- Yerel yollar ve paket içi bağlantılar doğrulanır; sır ve gerçek kişisel veri eklenmez.
- GitHub teslimi taslak PR'dır. Web sitesi dağıtımı veya kitap yayını yapılmaz.

## Kapsam sınırı

Tam kitap metni, çalışan Pusula uygulaması, ücretli model denemeleri ve 36 aşamanın bitmiş kod sürümleri bu başlangıç paketinin teslimi değildir. Bunlar URETIM_PLANI.md dosyasında ayrı üretim aşamalarıdır.

## Doğrulama

`python3 uygulama-kitabi/pusula/tools/validate_package.py` paket bütünlüğünü denetler. Yazarın kapsam ve anlatım incelemesi bekler. Model davranışı için skill vakaları ve her promptun gerçek koşu kaydı ayrıca yürütülür.

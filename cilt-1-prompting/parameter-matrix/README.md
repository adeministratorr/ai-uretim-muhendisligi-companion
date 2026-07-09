# Parametre Matrisi — Temperature, Top-p, Top-k Laboratuvarı

**Kitap bağlantısı:** Cilt 1, Bölüm 1 — Yapay Zekâ ve Dil Modellerine Giriş, 1.6-1.8
(Şekil 1.6 — Dört model parametresinin karşılaştırması).

## Ne Yapar?

Gerçek bir API çağrısı yapmadan, kitaptaki "Bugün hava çok ..." örneğindeki aynı
aday tokenlar üzerinde saf Python ile şunları gösterir:

- `softmax_with_temperature`: temperature düştükçe dağılımın nasıl sivrildiğini,
  yükseldikçe nasıl yayıldığını.
- `top_k_filter`: yalnızca en olası k adayı bırakıp geri kalanını sıfırlayarak
  yeniden normalize eder.
- `top_p_filter`: kümülatif olasılık p eşiğine ulaşana kadar adayları tutar.

## Nasıl Kullanılır?

**Kod bilmiyorsanız (önerilen yol):** Laboratuvarın yayındaki sürümünü tarayıcınızda
açın: <https://lab.ademyuce.tr/cilt-1-prompting/parameter-matrix/sampling_lab.html>
İsterseniz `sampling_lab.html` dosyasını indirip çift tıklayarak da açabilirsiniz;
kurulum, terminal veya internet bağlantısı gerekmez. Kaydırıcılarla
temperature/top-k/top-p'yi değiştirip çubukların canlı güncellenmesini izleyebilirsiniz.

**Kod biliyorsanız:** Aynı mantığın Python sürümü `sampling_lab.py` dosyasındadır.

```bash
python3 sampling_lab.py       # demo çıktısı (terminalde metin olarak)
python3 -m pytest             # testler (5 test, bağımlılık: pytest)
```

## Beklenen Çıktı (özet)

```text
temperature=0.2: güzel=99.7%, sıcak=0.2%, kötü=0.0%, mavi=0.0%
temperature=1.0: güzel=67.4%, sıcak=20.3%, kötü=8.2%, mavi=4.1%
temperature=1.8: güzel=49.1%, sıcak=25.2%, kötü=15.3%, mavi=10.4%
```

Düşük temperature'da tek aday baskınlaşır; yüksek temperature'da adaylar
birbirine yaklaşır — kitaptaki Şekil 1.6'nın "Temperature" panelinin sayısal
karşılığıdır.

## Kabul Kriteri

- [x] Kurulum adımları açık (bağımlılık yok, saf Python 3).
- [x] Örnek çalışıyor (`python3 sampling_lab.py`).
- [x] Test/doğrulama komutu var (`pytest`, 5 test).
- [x] Beklenen çıktı gösteriliyor.
- [x] Risk ve sınırlar yazıldı (aşağıda).

## Riskler ve Sınırlar

- Bu, gerçek bir dil modelinin örnekleme mekanizmasının **basitleştirilmiş** bir
  simülasyonudur; gerçek modellerde dağarcık binlerce/on binlerce token içerir.
- Sonuç değerleri temsilîdir; gerçek bir modelin ürettiği olasılıklar sağlayıcıya,
  modele ve prompta göre değişir (kitaptaki "Değerler temsilîdir" notuyla tutarlı).

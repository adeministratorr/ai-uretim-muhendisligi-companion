"""Bir ajana tanımlanan araç listesini "araç listesi + parametre sınırı + onay
noktası" üçlü denetiminden geçiren küçük bir laboratuvar.

Kitap bağlantısı: Cilt 1, Bölüm 13 (Yapay Zekâ Ajanları: Kavramlar), 13.4
("Araç Tanımı Nasıl Görünür?" — GELİŞTİRİCİ NOTU), 13.5 (ajanın beş bileşeni:
model, araç, talimat, bellek, durum) ve 13.10 (araştır-özetle-raporla örneği,
kabul kriterindeki üçlü kontrol).

Gerçek bir API çağrısı yapmaz; modele hiç bağlanmaz. Girdi, bir ajana
tanımlanan araçların statik bir listesidir (ad, izinli parametreler, geri
alınabilirlik, onay noktası); çıktı, hangi araçların riskli işaretlendiğidir.

13.4'teki GELİŞTİRİCİ NOTU'nun vurguladığı gibi araç listesi, bir ajanın
yapabileceklerinin ilk sınırıdır ama tek başına yeterli değildir: bir araç
izinliyse bile hangi parametrelerle çağrılabileceği ayrıca sınırlanmalıdır.
13.9'daki yarı otonom çalışma ilkesi ise geri alınamaz eylemlerin (gönderme,
silme, ödeme gibi) bir onay noktasının arkasında durması gerektiğini söyler.
Bu laboratuvar, bu iki ilkeyi tek bir kuralda birleştirir: parametresi
sınırlanmamış VE geri alınamaz VE onay noktası tanımlanmamış bir araç,
13.10'un kabul kriterindeki üçüncü kontrolün tam olarak yakalamaya çalıştığı
hatadır (araç listesine yanlışlıkla gönderme yetkili bir aracın eklenmesi).
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Arac:
    """Bir ajana tanımlanan tek bir aracı temsil eder (13.4'teki üç bilgiyle
    tutarlı: ad, ne işe yaradığı — burada kısaltılmıştır — ve parametre
    şeması), buna ek olarak 13.9-13.10'dan gelen iki denetim alanı taşır.

    Alanlar:
        ad: Aracın adı (ör. "web_oku").
        izinli_parametreler: Aracın kabul ettiği parametre değerlerinin
            (ör. izin verilen adresler) listesi. Boş demet veya `"*"` içeren
            bir demet, aracın herhangi bir parametreyle çağrılabildiği
            (sınırsız) anlamına gelir — 13.10'daki `web_oku` örneğinin tam
            tersi: o örnekte adres, talimatta tanımlı beş rakiple sınırlıdır.
        geri_alinabilir: Aracın yol açtığı eylem geri alınabilir mi (ör. bir
            sayfa okumak veya taslak oluşturmak) yoksa geri alınamaz mı
            (ör. e-posta göndermek, kayıt silmek, ödeme yapmak — 13.9'daki
            örnek liste).
        onay_noktasi_var: Aracı çalıştırmadan önce bir insana onay isteği
            gösteriliyor mu (13.9'daki yarı otonom çalışma mekanizması).
    """

    ad: str
    izinli_parametreler: tuple[str, ...] = field(default_factory=tuple)
    geri_alinabilir: bool = True
    onay_noktasi_var: bool = False


@dataclass(frozen=True)
class DenetimSonucu:
    """Tek bir aracın denetim sonucu.

    Alanlar:
        arac_adi: Denetlenen aracın adı.
        riskli: 13.10'daki üçlü kontrolün tam olarak arandığı hata durumu
            (parametre sınırsız + geri alınamaz + onay noktası yok) mu?
        gerekceler: Sonuca nasıl varıldığını açıklayan, okunabilir madde
            listesi (hem risk hem güvence gerekçeleri).
    """

    arac_adi: str
    riskli: bool
    gerekceler: tuple[str, ...]


def parametre_sinirsiz_mi(arac: Arac) -> bool:
    """Aracın parametre şeması sınırlanmamış mı?

    Boş bir `izinli_parametreler` listesi veya listede `"*"` joker karakteri
    varsa, araç herhangi bir parametreyle (ör. herhangi bir adresle)
    çağrılabilir demektir — 13.4'teki "araç izinliyse bile hangi
    parametrelerle çağrılabileceği ayrıca sınırlanmalıdır" uyarısının test
    edilebilir hâli.
    """
    return len(arac.izinli_parametreler) == 0 or "*" in arac.izinli_parametreler


def araci_denetle(arac: Arac) -> DenetimSonucu:
    """Tek bir aracı 13.10'daki üçlü kontrole göre denetler.

    Bir araç yalnızca şu üç koşulun **hepsi** birden sağlandığında riskli
    işaretlenir:

    1. Parametre sınırı yok (`parametre_sinirsiz_mi` doğru).
    2. Eylem geri alınamaz (`geri_alinabilir` yanlış).
    3. Onay noktası tanımlanmamış (`onay_noktasi_var` yanlış).

    Üç koşuldan biri bile eksikse araç riskli sayılmaz: parametre sınırlıysa
    araç zaten dar bir alanda çalışır (13.10'daki `web_oku` örneği); eylem
    geri alınabilirse yanlış bir çağrının bedeli düşüktür; onay noktası
    varsa çalıştırılmadan önce bir insan araya girer (13.9).
    """
    sinirsiz = parametre_sinirsiz_mi(arac)
    riskli = sinirsiz and not arac.geri_alinabilir and not arac.onay_noktasi_var

    gerekceler: list[str] = []
    if sinirsiz:
        gerekceler.append("parametre sınırı yok (herhangi bir değerle çağrılabilir)")
    else:
        gerekceler.append(
            "parametre sınırlı: " + ", ".join(arac.izinli_parametreler)
        )

    if arac.geri_alinabilir:
        gerekceler.append("eylem geri alınabilir")
    else:
        gerekceler.append("eylem geri alınamaz")

    if arac.onay_noktasi_var:
        gerekceler.append("onay noktası tanımlı")
    else:
        gerekceler.append("onay noktası tanımlanmamış")

    return DenetimSonucu(arac_adi=arac.ad, riskli=riskli, gerekceler=tuple(gerekceler))


def arac_listesini_denetle(araclar: list[Arac]) -> list[DenetimSonucu]:
    """Bir ajana tanımlanan tüm araç listesini sırayla denetler."""
    return [araci_denetle(arac) for arac in araclar]


def riskli_araclari_say(sonuclar: list[DenetimSonucu]) -> int:
    """Denetim sonuçları arasında riskli işaretlenen araç sayısını döner."""
    return sum(1 for sonuc in sonuclar if sonuc.riskli)


# 13.10'daki "Araştır → Özetle → Raporla" akışının araç listesi. `eposta_gonder`
# hariç üçü, PROMPT ÖRNEĞİ'ndeki tanıma birebir uygundur; `eposta_gonder`, aynı
# alt bölümün kabul kriterinde tarif edilen "yanlışlıkla eklenmiş gönderme
# yetkili araç" hayalini somutlaştıran, bu laboratuvara özgü bir karşı örnektir.
SELIN_ARAC_LISTESI: list[Arac] = [
    Arac(
        ad="web_oku",
        izinli_parametreler=(
            "rakip1.com/fiyat",
            "rakip2.com/fiyat",
            "rakip3.com/fiyat",
            "rakip4.com/fiyat",
            "rakip5.com/fiyat",
        ),
        geri_alinabilir=True,
        onay_noktasi_var=False,
    ),
    Arac(
        ad="gecmis_raporu_getir",
        izinli_parametreler=("musteri_id", "hafta"),
        geri_alinabilir=True,
        onay_noktasi_var=False,
    ),
    Arac(
        ad="rapor_taslagi_olustur",
        izinli_parametreler=("icerik",),
        geri_alinabilir=True,
        onay_noktasi_var=False,
    ),
    Arac(
        ad="eposta_gonder",
        izinli_parametreler=(),  # sınırsız — kötü tasarım örneği
        geri_alinabilir=False,
        onay_noktasi_var=False,
    ),
]


def demo() -> None:
    sonuclar = arac_listesini_denetle(SELIN_ARAC_LISTESI)
    print("Selin'in ajanına tanımlı araç listesi denetleniyor (13.10):\n")
    for sonuc in sonuclar:
        etiket = "RİSKLİ" if sonuc.riskli else "güvenli"
        print(f"- {sonuc.arac_adi}: {etiket}")
        for gerekce in sonuc.gerekceler:
            print(f"    · {gerekce}")
    toplam_riskli = riskli_araclari_say(sonuclar)
    print(f"\nToplam {len(sonuclar)} araçtan {toplam_riskli} tanesi riskli işaretlendi.")
    if toplam_riskli:
        print(
            "Not: eposta_gonder, 13.10'un kabul kriterindeki üçüncü kontrolün "
            "yakalamak için tasarlandığı hatayı gösterir — talimatta tarif "
            "edilmeyen bir gönderme yetkisi araç listesine sızmıştır."
        )


if __name__ == "__main__":
    demo()

import pytest

from impact_effort_matrix import (
    BASE_DIR,
    Gorev,
    degerlendir,
    format_rapor,
    json_yukle,
    level,
    onceliklendir,
)


def test_level_esik_dogru_calisir():
    assert level(1) == "düşük"
    assert level(2) == "düşük"
    assert level(3) == "yüksek"
    assert level(5) == "yüksek"


def test_gecersiz_olcek_degeri_reddedilir():
    with pytest.raises(ValueError):
        Gorev(ad="Test görevi", etki=6, efor=2, risk=2, deger=2)


def test_bos_ad_reddedilir():
    with pytest.raises(ValueError):
        Gorev(ad="   ", etki=3, efor=3, risk=3, deger=3)


def test_hizli_kazanc_ceyregi():
    gorev = Gorev(ad="Hızlı kazanç örneği", etki=5, efor=1, risk=1, deger=1)
    degerlendirme = degerlendir(gorev)
    assert degerlendirme.ie_ceyrek == "hızlı kazanç"
    assert degerlendirme.ie_eylem == "Önce bunlar kurulur"
    assert degerlendirme.ie_sira == 1


def test_kacin_ceyregi():
    gorev = Gorev(ad="Kaçın örneği", etki=1, efor=5, risk=1, deger=1)
    degerlendirme = degerlendir(gorev)
    assert degerlendirme.ie_ceyrek == "kaçın"
    assert degerlendirme.ie_sira == 4


def test_dusuk_risk_yuksek_deger_ceyregi():
    gorev = Gorev(ad="Düşük risk yüksek değer örneği", etki=3, efor=3, risk=1, deger=5)
    degerlendirme = degerlendir(gorev)
    assert degerlendirme.rv_ceyrek == "düşük risk / yüksek değer"
    assert degerlendirme.rv_eylem == "Düşük düzeyde insan onayıyla kurulabilir"


def test_oncelik_puani_iki_ceyregin_en_kotusudur():
    # Etki/efor "hızlı kazanç" (sıra 1) ama risk/değer "yüksek risk / yüksek
    # değer" (sıra 3) olan bir görev, tek eksende iyi görünse bile 3. öncelik
    # kademesine düşmelidir — kitap 10.13'ün "aynı iş akışı iki matriste farklı
    # köşeye düşebilir" ilkesi.
    gorev = Gorev(ad="Riskli ama hızlı görev", etki=4, efor=2, risk=5, deger=4)
    degerlendirme = degerlendir(gorev)
    assert degerlendirme.ie_sira == 1
    assert degerlendirme.rv_sira == 3
    assert degerlendirme.oncelik_puani == 3
    assert not degerlendirme.otomasyona_uygun


def test_yuksek_riskli_alan_matris_puanindan_bagimsiz_etiketlenir_ve_sona_birakilir():
    iyi_puanli_ama_riskli = Gorev(
        ad="Vergi beyanı taslağı", etki=5, efor=1, risk=1, deger=5, yuksek_riskli_alan=True
    )
    sikinti_yok = Gorev(ad="Sıradan hızlı kazanç", etki=5, efor=1, risk=1, deger=5)

    siralanmis = onceliklendir([iyi_puanli_ama_riskli, sikinti_yok])

    assert siralanmis[0].gorev.ad == "Sıradan hızlı kazanç"
    assert siralanmis[1].gorev.ad == "Vergi beyanı taslağı"
    assert "Yüksek riskli karar alanı" in siralanmis[1].oncelik_etiketi


def test_ornek_dosyasi_beklenen_sirayla_yuklenir():
    gorevler = json_yukle(BASE_DIR / "gorev_listesi_ornek.json")
    assert len(gorevler) == 9

    siralanmis = onceliklendir(gorevler)
    ilk_uc = [d.gorev.ad for d in siralanmis[:3]]
    assert ilk_uc == [
        "Müşteri mesajı cevap taslağı",
        "Sosyal medya paylaşımı — rutin ürün tanıtımı",
        "Toplantı notu özeti ve görev çıkarma",
    ]
    assert siralanmis[-1].gorev.ad == "Vergi beyanı taslağı"
    assert siralanmis[-1].gorev.yuksek_riskli_alan is True


def test_sablon_dosyasi_bos_listedir():
    gorevler = json_yukle(BASE_DIR / "gorev_listesi_sablonu.json")
    assert gorevler == []
    assert "boş" in format_rapor(onceliklendir(gorevler))

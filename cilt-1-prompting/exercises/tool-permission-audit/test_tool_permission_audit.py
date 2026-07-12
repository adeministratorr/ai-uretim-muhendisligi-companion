from tool_permission_audit import (
    SELIN_ARAC_LISTESI,
    Arac,
    araci_denetle,
    arac_listesini_denetle,
    parametre_sinirsiz_mi,
    riskli_araclari_say,
)


def test_parametre_sinirsiz_mi_bos_liste_sinirsiz_sayilir():
    arac = Arac(ad="test_araci", izinli_parametreler=())
    assert parametre_sinirsiz_mi(arac) is True


def test_parametre_sinirsiz_mi_yildiz_sinirsiz_sayilir():
    arac = Arac(ad="test_araci", izinli_parametreler=("*",))
    assert parametre_sinirsiz_mi(arac) is True


def test_parametre_sinirsiz_mi_dolu_liste_sinirli_sayilir():
    arac = Arac(ad="web_oku", izinli_parametreler=("rakip1.com", "rakip2.com"))
    assert parametre_sinirsiz_mi(arac) is False


def test_sinirsiz_geri_alinamaz_onaysiz_arac_riskli_isaretlenir():
    # 13.10'daki kabul kriterinin üçüncü kontrolünün yakalamak için var
    # olduğu tam hata: parametre sınırı yok + geri alınamaz + onay yok.
    arac = Arac(
        ad="eposta_gonder",
        izinli_parametreler=(),
        geri_alinabilir=False,
        onay_noktasi_var=False,
    )
    sonuc = araci_denetle(arac)
    assert sonuc.riskli is True


def test_parametre_sinirli_arac_geri_alinamaz_olsa_bile_riskli_degil():
    # 13.4'teki ilke: parametre sınırı, araç izinliyse bile araca eklenen
    # tek başına yeterli olmayan ama gerekli bir korumadır.
    arac = Arac(
        ad="odeme_yap",
        izinli_parametreler=("musteri_faturasi_12345",),
        geri_alinabilir=False,
        onay_noktasi_var=False,
    )
    sonuc = araci_denetle(arac)
    assert sonuc.riskli is False


def test_onay_noktasi_tanimliysa_sinirsiz_geri_alinamaz_arac_riskli_degil():
    # 13.9'daki yarı otonom çalışma: geri alınamaz bir eylem, onay
    # noktasının arkasına konursa riskli işaretlenmez.
    arac = Arac(
        ad="kayit_sil",
        izinli_parametreler=(),
        geri_alinabilir=False,
        onay_noktasi_var=True,
    )
    sonuc = araci_denetle(arac)
    assert sonuc.riskli is False


def test_geri_alinabilir_arac_sinirsiz_ve_onaysiz_olsa_bile_riskli_degil():
    # Geri alınabilir eylemlerde (ör. okuma) bedel düşük olduğu için tek
    # başına parametre sınırının eksikliği riskli sayılmaz.
    arac = Arac(
        ad="web_oku",
        izinli_parametreler=(),
        geri_alinabilir=True,
        onay_noktasi_var=False,
    )
    sonuc = araci_denetle(arac)
    assert sonuc.riskli is False


def test_gerekceler_sinirli_parametreleri_listeler():
    arac = Arac(ad="gecmis_raporu_getir", izinli_parametreler=("musteri_id", "hafta"))
    sonuc = araci_denetle(arac)
    assert any("musteri_id" in gerekce for gerekce in sonuc.gerekceler)


def test_arac_listesini_denetle_selin_ornegindeki_riskli_sayisi():
    sonuclar = arac_listesini_denetle(SELIN_ARAC_LISTESI)
    assert len(sonuclar) == len(SELIN_ARAC_LISTESI)
    assert riskli_araclari_say(sonuclar) == 1
    riskli_adlar = [sonuc.arac_adi for sonuc in sonuclar if sonuc.riskli]
    assert riskli_adlar == ["eposta_gonder"]


def test_web_oku_araci_riskli_degil():
    sonuclar = arac_listesini_denetle(SELIN_ARAC_LISTESI)
    web_oku_sonucu = next(s for s in sonuclar if s.arac_adi == "web_oku")
    assert web_oku_sonucu.riskli is False

# SPEC_TEMPLATE.md

Bu şablon, companion repo içinde yeni bir örnek, lab, tool, MCP server, eval veya production akışı geliştirmeden önce doldurulur.

---

## 1. Kısa Tanım

Bu çalışma ne üretecek?

```text
Örnek: AI tarafından yazılan testlerin gerçekten hata yakalayıp yakalamadığını mutation testing ile ölçen küçük bir Python lab'ı.
```

---

## 2. Kitap Bağlantısı

- Cilt:
- Bölüm:
- Alt başlık:
- İlgili kavramlar:

---

## 3. Hedef Okuyucu

- Başlangıç / orta / ileri:
- Gerekli ön bilgi:
- Gerekli araçlar:

---

## 4. Kabul Kriterleri

- [ ] Kurulum adımları açık.
- [ ] Örnek çalışıyor.
- [ ] Test veya doğrulama komutu var.
- [ ] Beklenen çıktı gösteriliyor.
- [ ] Risk ve sınırlar yazıldı.
- [ ] Web bölüm sayfasından linklenebilir.

---

## 5. Kapsam Dışı

Bu çalışmada özellikle yapılmayacak şeyler:

- Gerçek API key kullanmak.
- Gerçek production verisine veya canlı servise bağlanmak.
- Gereksiz büyük framework bağımlılığı kurmak.
- Oyuncak ama öğretmeyen örnek üretmek.

---

## 6. Dosya Planı

```text
cilt-2-loops/mutation-tests/
├── README.md
├── src/
├── tests/
└── pyproject.toml
```

---

## 7. Doğrulama Planı

Çalıştırılacak komutlar:

```bash
python -m pytest
```

Başarı ölçütü:

```text
Testler önce geçer; sonra kasıtlı hata enjekte edildiğinde en az bir test hatayı yakalar.
```

---

## 8. Riskler

- Agent testleri zayıflatabilir.
- Örnek fazla soyut kalabilir.
- Kullanılan araç sürümü değişebilir.

Azaltma:

- Test silme ve assertion zayıflatma PR devre kesiciyle yakalanır.
- README gerçek dünya bağlamıyla yazılır.
- Sürüm ve son güncelleme notu tutulur.

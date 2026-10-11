# Model geçişleri ve API uyumluluğu | Sessiz değişiklikleri yakalamak

**Kaynak kontrolü:** 11 Ekim 2026 · **Kapsam:** Doğrudan resmî sağlayıcı belgelerindeki geçiş örnekleri ve önerilen denetim yöntemi. Canlı hesap/istek testi yapılmadı.

Bir API isteğinin `200 OK` dönmesi, uygulamanın hâlâ **aynı modeli** çalıştırdığı anlamına gelmez. Sağlayıcı eski model adını yeni sürüme yönlendirebilir, önizlemeyi kapatabilir, çağrıyı farklı ücretlendirebilir veya `tool_calls` davranışını değiştirebilir. Bu yüzden güncellemeyi yalnızca paket sürümü değişikliği olarak görmeyiz.

## Ekim 2026 itibarıyla dikkat çeken geçişler

| Sağlayıcı | Eski / değişen kullanım | Güncel yön | Risk ve doğrulama |
|---|---|---|---|
| **DeepSeek** | `deepseek-v4-flash`, `deepseek-v4-flash-vision-exp` | `deepseek-flash` (V4.1-Flash); eski isimler geçici yönlendirme | Eski ad çalışsa bile model değişmiş olabilir. [Resmî V4.1 notu](https://api-docs.deepseek.com/news/news260910/) |
| **DeepSeek V4-Pro** | 14 Eylül için yönlendirme duyurulmuştu | Güncel başlangıç sayfası `deepseek-v4-pro` kimliğini kullanılabilir modeller arasında listeliyor | Belgeler tarih sırasıyla okunmalı; **canlı model ve fatura doğrulaması gerekli.** [Başlangıç notu](https://api-docs.deepseek.com/quick_start/pricing-details-cny/) |
| **DeepSeek eski adlar** | `deepseek-chat`, `deepseek-reasoner` | V4 ailesine geçiş | 24 Temmuz 2026 için kapatma duyurusu var; artık güvenmeyin. [V4 notu](https://api-docs.deepseek.com/news/news260424/) |
| **xAI** | `grok-code-fast-1`, `grok-4-1-fast-*`, `grok-3` | 15 Mayıs 2026'dan itibaren Grok 4.3'e yönlendirme duyurulmuştu; yeni işler için güncel model dizinini kullan | Hata olmadan davranış/fiyat değişebilir. [Geçiş](https://docs.x.ai/developers/migration/may-15-retirement) |
| **Google** | `gemini-3-pro-preview` | `gemini-3.1-pro-preview` | Eski önizleme 9 Mart 2026'da kapandı. [Takvim](https://ai.google.dev/gemini-api/docs/deprecations/) |
| **Google TTS** | `gemini-3.1-flash-tts-preview` | `gemini-3.8-flash-tts` / Lite | 17 Kasım 2026 için kapanış tarihi belirtilmiş. [Takvim](https://ai.google.dev/gemini-api/docs/deprecations/) |
| **OpenAI** | `chat-latest`, genel “en son model” takibi | Üretimde açık model ID / snapshot stratejisi | `chat-latest` güncellenen alias; deney ve ürün geliştirme için farklı. [Changelog](https://developers.openai.com/api/docs/changelog) |
| **Tencent** | Eski Hunyuan API/model ID'leri | TokenHub, sağlayıcının güncel HY model kimlikleri | **Platform değişikliği** söz konusu; yalnızca `model` alanını düzeltmek yetmeyebilir. [Göç](https://cloud.tencent.com/document/product/1729/131925) |
| **ByteDance** | Doubao Seed 2.0 Pro/Code | Seed 2.1 Pro/Turbo | 8 Ağustos 2026 kapanış notu bulunuyor. [Tarife/göç](https://docs.volcengine.com/docs/aidap/Billing_items_and_prices_of_large_model_access?lang=en) |
| **Mistral** | Large 4'e üretimde geçiş | 11 Ekim itibarıyla **önizleme** | Large 3 ile karıştırma; ağırlık yayımlama planı henüz gerçekleşmiş sayılmaz. [Duyuru](https://mistral.ai/news/mistral-large-4/) |

## Uyumluluk matrisi: “OpenAI-compatible” yazısı yeter mi?

Aşağıdaki alanlar **her sağlayıcı için tek tek test edilir**, çünkü kabul edilen HTTP biçimi ile semantik destek aynı değildir.

| Yetenek | Testte aranacak şey |
|---|---|
| Temel chat | `system` / `user` / `assistant` sıralaması, yanıt şeması |
| Responses API | Yanıt nesnesi, state, tool continuation ve hata kodları |
| Structured outputs | JSON Schema strict davranışı, bozuk yanıt ve eksik alan |
| Function/tool calling | Paralel çağrı, argüman türleri, çağrı kimliği ve dönüş bağlama |
| Reasoning | `reasoning_effort` veya sağlayıcıya özel `thinking` alanı; desteklenmeyen değer |
| Streaming | Kısmi JSON parçaları, final usage ve cancel sonrası durum |
| Çok biçimli girdi | Görsel/PDF/ses/video boyutu, dosya formatları, giriş sırası |
| Uzun bağlam | Sistem prompt'undan kritik talimat hatırlama, kaynak bulma, bağlam sonundaki bilgi |
| Token / caching | Tokenizer farkı, cache yazma/okuma, TTL, gizli reasoning maliyeti |
| Bölge ve veri | Nerede işleniyor, log retention, data residency, sözleşme |
| Durum kodları | 429, 5xx, timeout; üstel geri çekilme; idempotency |
| Fiyat | Uzun bağlam katmanı, batch, araç çağrısı, önbellek, özel hız kademesi |

## Sürüm yükseltme kontrol listesi

- [ ] Değişiklik kaynağı birincil duyuru veya model kartından doğrulandı.
- [ ] **Tam model ID / snapshot / sağlayıcı / bölge** kayıt altına alındı.
- [ ] Ürün arayüzündeki isim yerine gerçek API model kimliği belirlendi.
- [ ] Fiyat, bağlam, maksimum çıktı, cache ve araç ücretleri yeniden hesaplandı.
- [ ] JSON Schema, tool-call, uzun bağlam ve Türkçe kalite testleri yeniden koşuldu.
- [ ] Modelin araç izinlerini aşmadığı kontrol edildi.
- [ ] Şema ve araç davranışlarındaki geriye dönük uyumsuzluklar belgelendi.
- [ ] Canary, rollback ve durdurma eşiği belirlendi.
- [ ] Kitabın ilgili lab'ına kullanılan modelin kontrol tarihi eklendi.
- [ ] Değişiklik küçük bir PR ile gözden geçirildi.

## Örnek sürüm kayıt şablonu

```yaml
migration_id: MW-2026-10-001
checked_at: "2026-10-11"
provider: "example-provider"
previous_model: "example-old"
new_model: "example-new"
endpoint: "example-endpoint"
region: "example-region"
source_urls: []
behavioral_differences: []
regression_suite: "not-run"
cost_impact: "not-measured"
rollback_model: "example-old"
approval: "pending-human-review"
terminal_state: "needs-review"
```

Bu YAML bir **şablondur**, gerçek migrasyon yapıldığı anlamına gelmez.

## Üretim ilkesi

Alias'ın işlevi geliştiriciye kolaylık sağlamaktır; **tekrarlanabilirlik sözü değildir**. Tekrarlanabilir eğitim/lab ve kritik uygulamalarda mümkünse sabit sürümü kullanın. Sabitlemenin mümkün olmadığı servislerde sürümü, dönen model kimliğini, yanıt şemasını ve maliyeti düzenli gözlemleyin. Kodun çalışması yeterli değil; beklenen davranışı koruması gerekir.

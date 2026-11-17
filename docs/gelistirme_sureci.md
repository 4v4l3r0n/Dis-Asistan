# Uygulama Geliştirme Aşamaları — DişAsistan (PRJIC20250202)

Bu doküman, proje başlangıcından teslimine kadar izlenen geliştirme aşamalarını özetler.

---

## Aşama 1: Analiz ve Teknoloji Kararları
- Proje gereksinimleri analiz edildi ve 8 haftalık yol haritası (`docs/YOL_HARITASI.md`) oluşturuldu.
- **Workflow Aracı:** Self-hosted **n8n** (Docker) seçildi. Gerekçe: Görsel iş akışı, yerleşik Chat Trigger arayüzü, Postgres Chat Memory desteği ve kural bazlı akışlarda esneklik.
- **Eğitim / Bilgi Tabanı Metodu:** Fine-tuning yerine **RAG (Retrieval-Augmented Generation)** seçildi.
- **LLM & Embedding:** Google Gemini API (Free Tier) — `gemini-2.5-flash` / `gemini-2.5-flash-lite` ve `gemini-embedding-001`.
- Versiyon kontrolü için `source_code/` altında Git başlatıldı.

## Aşama 2: Yerel Altyapı (Docker Compose)
- `docker-compose.yml` ile üç temel servis konteynerize edildi:
  1. `chatbot-n8n` (Port `5678`)
  2. `chatbot-postgres` (PostgreSQL 16, Port `5432`)
  3. `chatbot-qdrant` (Qdrant Vector DB, Port `6333`)
- Hassas bilgiler `.env` dosyasında izole edildi (`.gitignore` ile korundu), şablon olarak `.env.example` eklendi.

## Aşama 3: Temel Chatbot ve Konuşma Geçmişi
- `workflows/chatbot.json` oluşturuldu: `Chat Trigger` → `AI Agent` → `Google Gemini Chat Model`.
- `Postgres Chat Memory` node'u bağlanarak `n8n_chat_histories` tablosunda oturum bazlı (`sessionId`) sohbet geçmişi saklandı.
- `prompts/system_prompt.md` ile Türkçe dil, konu sınırlandırması ve tıbbi yönlendirme kuralları tanımlandı.

## Aşama 4: Veri Seti Hazırlama ve Vektörleştirme
- T.C. Sağlık Bakanlığı, Türk Dişhekimleri Birliği (TDB), WHO ve NIH/NIDCR açık kaynaklarından derlenen 20 başlıklı Türkçe bilgi tabanı (`data/processed/agiz_dis_sagligi_kb.json`) hazırlandı ve `docs/veri_kaynaklari.md` içinde belgelendi.
- `scripts/ingest_qdrant.py` ile tüm belgeler `gemini-embedding-001` (3072 boyut) kullanılarak vektörleştirildi ve Qdrant `agiz_dis_sagligi` koleksiyonuna yüklendi.

## Aşama 5 & 6: RAG Entegrasyonu, Guardrail ve KVKK
- `AI Agent` node'una **Qdrant Vector Store** aracı (`agiz_dis_sagligi_bilgi_tabani`) eklendi.
- Yanıtların sonunda KVKK bağlantısı ve acil durum uyarılarının LLM'e bırakılmadan kesin çalışması için **KVKK ve Güvenlik Kontrolü** (`Code` node) eklendi.
- `workflows/kvkk_sayfasi.json` ile `http://localhost:5678/webhook/kvkk` adresinde canlı KVKK Aydınlatma Metni web sayfası yayına alındı (`docs/kvkk_aydinlatma_metni.md`).

## Aşama 7 & 8: Otomatik Test, Değerlendirme ve Teslim
- 12 senaryoluk test seti (`tests/test_sorulari.json`) ve otomatik değerlendirme scripti (`scripts/evaluate_chatbot.py`) geliştirildi.
- Test sonuçları ve Gemini Free Tier kota bulguları `docs/degerlendirme_raporu.md` dosyasına kaydedildi.
- Sistem mimarisi (`docs/mimari.md`), kurulum kılavuzu (`README.md`) ve tüm workflow dosyaları Git üzerinde düzenli commit geçmişiyle teslimata hazır hale getirildi.

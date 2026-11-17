# Ağız ve Diş Sağlığı AI Chatbot

AI agent'lar ve bir LLM aracılığıyla kullanıcıların ağız ve diş sağlığı sorularını Türkçe yanıtlayan chatbot (Proje No: PRJIC20250202).

- **Workflow:** n8n (self-hosted, Docker)
- **Yöntem:** RAG (Retrieval-Augmented Generation)
- **Konuşma geçmişi:** PostgreSQL
- **Vektör DB:** Qdrant

Detaylı dokümantasyon:
- [Yol Haritası](docs/YOL_HARITASI.md)
- [Sistem Mimarisi](docs/mimari.md)
- [Geliştirme Aşamaları](docs/gelistirme_sureci.md)
- [Veri Kaynakları ve RAG](docs/veri_kaynaklari.md)
- [KVKK Aydınlatma Metni](docs/kvkk_aydinlatma_metni.md)
- [Değerlendirme ve Test Raporu](docs/degerlendirme_raporu.md)

## Kurulum ve Çalıştırma

### 1. Gereksinimler
- **Docker Desktop** (çalışır durumda olmalıdır)
- **Google Gemini API Key** ([Google AI Studio](https://aistudio.google.com/) üzerinden ücretsiz)

### 2. Ortam Değişkenleri
`.env.example` dosyasını baz alarak `.env` dosyası oluşturun:
```bash
copy .env.example .env
```
`.env` içerisindeki `GEMINI_API_KEY` alanına aldığınız API anahtarını ekleyin.

### 3. Servisleri Başlatma
Terminalde `source_code` dizinindeyken:
```bash
docker compose up -d
```

Bu komut ile şu servisler ayağa kalkacaktır:
| Servis | Port | Açıklama |
|---|---|---|
| **n8n** | `http://localhost:5678` | AI Agent Workflow motoru ve Chat arayüzü |
| **Qdrant** | `http://localhost:6333` | Vektör Veritabanı (RAG bilgi tabanı) |
| **PostgreSQL** | `localhost:5432` | n8n veritabanı ve sohbet hafızası (Chat Memory) |

### 4. n8n İlk Kurulum ve Workflow'ları Yükleme
1. Tarayıcınızdan `http://localhost:5678` adresine gidin ve yönetici hesabınızı oluşturun.
2. **Credentials** bölümünden **Google Gemini API** ve **Postgres** (`Host: postgres`, `Database: n8n`, `User: n8n`) bağlantılarını tanımlayın.
3. **Qdrant API** bağlantısı için URL alanına `http://qdrant:6333` yazın (API Key boş bırakılır).
4. `workflows/kvkk_sayfasi.json` ve `workflows/chatbot.json` dosyalarını n8n'e **Import from File...** ile aktarıp yayınlayın (**Publish / Active**).

### 5. RAG Bilgi Tabanını Qdrant'a Yükleme
```bash
pip install requests
python scripts/ingest_qdrant.py
```

### 6. Otomatik Değerlendirme Testi
```bash
python scripts/evaluate_chatbot.py --url http://localhost:5678/webhook/<CHAT_WEBHOOK_ID>/chat
```

### 7. Servisleri Durdurma
```bash
docker compose down
```
*(Veriler Docker volume'larında kalıcı olarak saklanır, silinmez.)*


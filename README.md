# Ağız ve Diş Sağlığı AI Chatbot

AI agent'lar ve bir LLM aracılığıyla kullanıcıların ağız ve diş sağlığı sorularını Türkçe yanıtlayan chatbot (Proje No: PRJIC20250202).

- **Workflow:** n8n (self-hosted, Docker)
- **Yöntem:** RAG (Retrieval-Augmented Generation)
- **Konuşma geçmişi:** PostgreSQL
- **Vektör DB:** Qdrant

Detaylı plan: [docs/YOL_HARITASI.md](docs/YOL_HARITASI.md)

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

### 4. n8n İlk Kurulum
1. Tarayıcınızdan `http://localhost:5678` adresine gidin.
2. Bir sahip (owner) hesabı oluşturun (ad, e-posta, şifre).
3. Credentials menüsünden **Google Gemini** ve **Postgres** bağlantılarını tanımlayın.

### 5. Servisleri Durdurma
```bash
docker compose down
```
*(Veriler `volumes/` içinde kalıcı olarak saklanır, silinmez.)*


# Veri Kaynakları ve Bilgi Tabanı Hazırlama (RAG)

Bu doküman, **DişAsistan** chatbotunun RAG (Retrieval-Augmented Generation) bilgi tabanında kullanılan açık veri kaynaklarını, veri hazırlama yöntemini ve vektör veritabanı yapısını açıklar.

---

## 1. Kullanılan Açık Kaynaklar

Bilgi tabanı, genel halk sağlığı bilgilendirmesi amacıyla aşağıdaki güvenilir ve açık erişimli kaynakların içeriklerinden derlenerek Türkçe olarak yapılandırılmıştır:

| Kaynak | Kurum / Tür | Kapsam |
|---|---|---|
| **T.C. Sağlık Bakanlığı** (Halk Sağlığı Genel Müdürlüğü — Ağız ve Diş Sağlığı) | Kamu Kurumu | Günlük ağız hijyeni, fırçalama teknikleri, çocuk ve gebelikte diş sağlığı |
| **Türk Dişhekimleri Birliği (TDB)** — Halk Sağlığı Bilgilendirme Yayınları | Meslek Birliği | Diş ipi kullanımı, diş eti hastalıkları, diş taşı, ağız kokusu |
| **Dünya Sağlık Örgütü (WHO)** — *Oral Health Fact Sheets* | Uluslararası Kurum | Diş çürükleri, periodontal hastalıklar, ağız kanserleri, risk faktörleri ve korunma |
| **NIH / NIDCR** (National Institute of Dental and Craniofacial Research) | Açık Kamu Verisi (Public Domain) | Diş hassasiyeti, kanal tedavisi bilgilendirmesi, ortodonti bakımı, diyabet ve ağız sağlığı |

> [!NOTE]
> Tüm içerikler **genel bilgilendirme** amaçlıdır; tanı veya tedavi protokolü içermez. Acil durum ve tedavi taleplerinde kullanıcı her zaman bir diş hekimine yönlendirilir.

---

## 2. Veri Hazırlama ve Parçalama (Chunking)

- **Dosya:** `data/processed/agiz_dis_sagligi_kb.json`
- **Yapı:** Her kayıt bir konunun belirli bir alt başlığını temsil edecek şekilde anlamsal olarak bölünmüştür (`id`, `baslik`, `kategori`, `kaynak`, `icerik`).
- **Parça Boyutu:** Ortalama 400–800 karakter (~100–200 token) uzunluğunda, bağlam bütünlüğü bozulmadan hazırlanmış Türkçe metinler.

---

## 3. Vektörleştirme (Embedding) ve Qdrant Yapısı

- **Embedding Modeli:** Google Gemini `models/gemini-embedding-001`
- **Vektör Boyutu:** `3072`
- **Benzerlik Ölçütü:** Cosine Similarity (`Cosine`)
- **Qdrant Koleksiyonu:** `agiz_dis_sagligi`
- **Payload Şeması (n8n Qdrant Vector Store uyumlu):**
  ```json
  {
    "content": "Metin içeriği...",
    "metadata": {
      "title": "Başlık",
      "category": "Kategori",
      "source": "Kaynak Kurum"
    }
  }
  ```

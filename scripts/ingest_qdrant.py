"""
Ağız ve Diş Sağlığı Bilgi Tabanını Google Gemini Embedding API ile
vektörleştirip Qdrant vektör veritabanına yükleyen script.

Kullanım:
  python scripts/ingest_qdrant.py
  python scripts/ingest_qdrant.py --test "diş eti kanaması neden olur"
"""

import argparse
import json
import os
import time
from pathlib import Path
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
DATA_PATH = ROOT_DIR / "data" / "processed" / "agiz_dis_sagligi_kb.json"

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "agiz_dis_sagligi"
EMBEDDING_MODEL = "models/gemini-embedding-001"
VECTOR_SIZE = 3072


def load_api_key() -> str:
    """`.env` dosyasından GEMINI_API_KEY değerini okur."""
    if os.getenv("GEMINI_API_KEY"):
        return os.getenv("GEMINI_API_KEY").strip()
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("GEMINI_API_KEY bulunamadı (.env dosyasını kontrol edin).")


def get_embedding(text: str, api_key: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    """Gemini Embedding API kullanarak metin için vektör üretir."""
    url = f"https://generativelanguage.googleapis.com/v1beta/{EMBEDDING_MODEL}:embedContent?key={api_key}"
    payload = {
        "model": EMBEDDING_MODEL,
        "content": {"parts": [{"text": text}]},
        "taskType": task_type,
    }
    for attempt in range(4):
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            return resp.json()["embedding"]["values"]
        if resp.status_code == 429:
            wait = 5 * (attempt + 1)
            print(f"  Rate limit (429), {wait}s bekleniyor...")
            time.sleep(wait)
            continue
        raise RuntimeError(f"Embedding API hatası ({resp.status_code}): {resp.text}")
    raise RuntimeError("Embedding API 429 hatası aşılamadı.")


def ensure_collection() -> None:
    """Qdrant koleksiyonunu oluşturur (varsa yeniden oluşturur)."""
    col_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}"
    requests.delete(col_url, timeout=10)
    resp = requests.put(
        col_url,
        json={"vectors": {"size": VECTOR_SIZE, "distance": "Cosine"}},
        timeout=10,
    )
    resp.raise_for_status()
    print(f"Qdrant koleksiyonu hazır: {COLLECTION_NAME} (boyut={VECTOR_SIZE}, Cosine)")


def ingest_all(api_key: str) -> None:
    """Bilgi tabanındaki tüm dokümanları embedding alıp Qdrant'a yükler."""
    items = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    ensure_collection()

    points = []
    for idx, item in enumerate(items, start=1):
        full_text = f"{item['baslik']}\n\n{item['icerik']}\n\nKaynak: {item['kaynak']}"
        vector = get_embedding(full_text, api_key, task_type="RETRIEVAL_DOCUMENT")
        points.append(
            {
                "id": item["id"],
                "vector": vector,
                "payload": {
                    "content": full_text,
                    "metadata": {
                        "title": item["baslik"],
                        "category": item["kategori"],
                        "source": item["kaynak"],
                    },
                },
            }
        )
        print(f"[{idx}/{len(items)}] Vektörleştirildi: {item['baslik']}")
        time.sleep(0.4)  # Free tier rate limit koruması

    upsert_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points?wait=true"
    resp = requests.put(upsert_url, json={"points": points}, timeout=30)
    resp.raise_for_status()
    print(f"\nBaşarılı! Toplam {len(points)} kayıt Qdrant'a yüklendi.")


def test_search(query: str, api_key: str, top_k: int = 3) -> None:
    """Örnek bir sorgu ile Qdrant semantik aramasını test eder."""
    q_vector = get_embedding(query, api_key, task_type="RETRIEVAL_QUERY")
    search_url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/query"
    resp = requests.post(
        search_url,
        json={"query": q_vector, "limit": top_k, "with_payload": True},
        timeout=15,
    )
    resp.raise_for_status()
    results = resp.json().get("result", {}).get("points", [])
    print(f"\nSorgu: '{query}' (En yakın {len(results)} sonuç)")
    print("-" * 60)
    for r in results:
        meta = r["payload"]["metadata"]
        print(f"Skor: {r['score']:.4f} | {meta['title']} ({meta['source']})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Qdrant RAG Ingestion ve Test")
    parser.add_argument("--test", type=str, help="Sadece test sorgusu çalıştır")
    args = parser.parse_args()

    api_key = load_api_key()
    if args.test:
        test_search(args.test, api_key)
    else:
        ingest_all(api_key)


if __name__ == "__main__":
    main()

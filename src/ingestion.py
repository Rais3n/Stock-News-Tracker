from src.orchestrator import clean_news_orchestrator
from rag.qdrant_store import QdrantStore


def ingest(
    qdrant: QdrantStore, ticker: str, date_from: str, date_to: str, api_key: str
) -> tuple[int, int]:
    articles = clean_news_orchestrator(ticker, date_from, date_to, api_key)
    saved = qdrant.add_embeddings(articles)
    return len(articles), saved

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rag.chunker import create_chunks
from rag.embeddings import create_embedding
from app.models import Article
from qdrant_client.models import Record
import numpy as np
import uuid


class QdrantStore:

    def __init__(self):
        self.client = QdrantClient(
            url="http://localhost:6333"
        )

        self.collection_name = "stock_news"
        self.create_collection()

    def create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE
                )
            )

    def add_embeddings(self, articles: list[Article]):
        if not articles:
            return
        points = []
        texts = [article.embedding_text for article in articles]
        embeddings = create_embedding(texts)
        for article, vector in zip(articles, embeddings):
            point = PointStruct(
                id=article.id,
                vector=vector.tolist(),
                payload={
                    "ticker": article.ticker,
                    "text": article.embedding_text
                }
            )
            points.append(point)
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def get_by_ticker(self, ticker: list[str] | str, limit: int = 5) -> list[Record]:
        tickers = [ticker] if isinstance(ticker, str) else ticker
        params = {"must": [{"key": "ticker", "match": {"any": tickers}}]}
        records, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=params,
            limit=limit,
            with_vectors=True,
            with_payload=True
        )
        return records
    
    @staticmethod
    def filter_by_threshold(records: list[Record],threshold: float = 0.6) -> list[dict]:
        accepted_records: list[dict] = []
        accepted_vectors: list[np.ndarray] = []
        for record in records:
            current_vector = np.array(record.vector, dtype=np.float32)
            is_duplicate = False
            for vector in accepted_vectors:
                similarity = float(np.dot(current_vector,vector))
                if similarity >= threshold:
                    is_duplicate = True
                    break
            if not is_duplicate:
                accepted_records.append(record.payload)
                accepted_vectors.append(current_vector)
        return accepted_records
                
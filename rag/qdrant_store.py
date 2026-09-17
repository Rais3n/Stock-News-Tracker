from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rag.chunker import create_chunks
from rag.embeddings import create_embedding
from app.models import Article
from qdrant_client.models import Record
import numpy as np
from collections import defaultdict


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

    def add_embeddings(self, articles: list[Article], dedup_threshold: float = 0.8):
        if not articles:
            return
        points = []
        texts = [article.embedding_text for article in articles]
        embeddings = create_embedding(texts)
        accepted_vectors: defaultdict[str,list[np.ndarray]] = defaultdict(list)
        for article, vector in zip(articles, embeddings):
            ticker = article.ticker
            existing = accepted_vectors[ticker]
            if existing and np.any(np.dot(np.vstack(existing),vector) >= dedup_threshold):
                continue
            accepted_vectors[ticker].append(vector)
            point = PointStruct(
                id=article.id,
                vector=vector.tolist(),
                payload={
                    "ticker": ticker,
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
        all_records: list[Record] = []
        for t in tickers:
            params = {"must": [{"key": "ticker", "match": {"value": t}}]}
            records, _ = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=params,
                limit=limit,
                with_vectors=True,
                with_payload=True
            )
            all_records.extend(records)
        return all_records
    
    @staticmethod
    def filter_by_threshold(records: list[Record],threshold: float = 0.6) -> list[dict]:
        accepted_records: list[dict] = []
        accepted_vectors: defaultdict[str,list[np.ndarray]] = defaultdict(list)
        for record in records:
            current_vector = np.array(record.vector, dtype=np.float32)
            current_ticker = record.payload.get('ticker','') if record.payload else ''
            is_duplicate = False
            for vector in accepted_vectors[current_ticker]:
                similarity = float(np.dot(current_vector,vector))
                if similarity >= threshold:
                    is_duplicate = True
                    break
            if not is_duplicate:
                accepted_records.append(record.payload)
                accepted_vectors[current_ticker].append(current_vector)
        return accepted_records
                
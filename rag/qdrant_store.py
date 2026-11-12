import numpy as np
import uuid
from collections import defaultdict


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Record, PayloadSchemaType     
from rag.chunker import create_chunks
from rag.embeddings import create_embedding
from app.models import Article


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
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="publish_timestamp",
                field_schema=PayloadSchemaType.INTEGER,
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
                id=self.make_point_id(article.id,ticker),
                vector=vector.tolist(),
                payload={
                    "ticker": ticker,
                    "text": article.embedding_text,
                    "publish_timestamp": article.publish_timestamp
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
                order_by={
                    "key": "publish_timestamp",
                    "direction": "desc"
                },
                limit=limit,
                with_vectors=True,
                with_payload=True
            )
            all_records.extend(records)
        return all_records


    @staticmethod
    def make_point_id(article_id: int, ticker: str) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_URL,f"{ticker}:{article_id}")

    
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

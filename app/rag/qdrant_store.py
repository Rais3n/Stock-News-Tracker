from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.rag.chunker import create_chunks
from app.rag.embeddings import create_embedding
import uuid


class QdrantStore:

    def __init__(self):
        self.client = QdrantClient(
            url="http://localhost:6333"
        )

        self.collection_name = "stock_news"
        self.create_collection(self)

    def create_collection(self):
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE
                )
            )

    def add_embeddings(self, json):
        points = []
        text = json["summary"]
        chunks = create_chunks(text)
        embeddings = []
        for chunk in chunks:
            embedding = create_embedding(chunk)
            embeddings.append(embedding)

        for chunk, embedding in zip(chunks, embeddings):

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": chunk
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )


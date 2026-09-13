from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

def create_embedding(chunk):
    return model.encode(chunk)
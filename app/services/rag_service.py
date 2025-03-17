import numpy as np
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)
COLLECTION_NAME = "user_rag_collection"

def get_embeddings(texts):
    vectors = []
    for text in texts:
        resp = client.embeddings.create(input=text, model="text-embedding-3-small")
        vectors.append(np.array(resp.data[0].embedding))
    return vectors

def create_qdrant_collection(embedding_size: int):
    collections = qdrant_client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=embedding_size, distance=models.Distance.COSINE)
        )

def store_chunks(chunks):
    texts = [chunk.page_content for chunk in chunks]
    vectors = get_embeddings(texts)
    create_qdrant_collection(len(vectors[0]))
    points = [
        models.PointStruct(id=i, vector=vec.tolist(), payload={"text": text})
        for i, (vec, text) in enumerate(zip(vectors, texts))
    ]
    for i in range(0, len(points), 100):
        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points[i:i+100])

def retrieve_chunks(query, top_k=5):
    query_vec = get_embeddings([query])[0]
    results = qdrant_client.search(collection_name=COLLECTION_NAME, query_vector=query_vec.tolist(), limit=top_k)
    return [res.payload['text'] for res in results]

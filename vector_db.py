import collections
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="docs_local", dim=384):
        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
    
    def upsert(self, ids, vectors, payloads):
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)

    
    def search(self, query_vector, top_k: int = 5):
        response = self.client.query_points(
            collection_name = self.collection,
            query = query_vector,
            with_payload = True,
            limit = top_k
        )
        context = []
        sources = set()

        for r in response.points:
            payload = r.payload or {}
            text = payload.get("text", "")
            src = payload.get("source", "unknown")
            if text:
                context.append(text)
                sources.add(src)
        
        return {"contexts": context, "sources": list(sources)}
            
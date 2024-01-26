from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

class Embedder():
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant = QdrantClient("http://localhost:6333")
        
    def query_books(self, query):
        """
        Query the book database with a given query string.
        Args:
            query (str): The query string.
        Returns:
            list: A list of hits.
        """
        hits = self.qdrant.search(
            collection_name="my_books", query_vector=self.encoder.encode(query).tolist(), limit=3
        )
        for hit in hits:
            print(hit.payload, "score:", hit.score)
        return hits
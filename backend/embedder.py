from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client import models
from random import randint

class Embedder():
    def __init__(self):
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant = QdrantClient("http://qdrant:6333")
        
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
    
    def add_book(self, book):
        """
        Add a book to the database.
        Args:
            book (dict): The book to add.
        """
        self.qdrant.upload_records(
            collection_name="my_books",
            records=[
                models.Record(
                    id=randint(1, 999999), vector=self.encoder.encode(book["description"]).tolist(), payload=book
                )
            ]
        )
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from data import documents

encoder = SentenceTransformer("all-MiniLM-L6-v2")

qdrant = QdrantClient(":memory:")

qdrant.recreate_collection(
    collection_name="my_books",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.COSINE,
    ),
)

qdrant.upload_records(
    collection_name="my_books",
    records=[
        models.Record(
            id=idx, vector=encoder.encode(doc["description"]).tolist(), payload=doc
        )
        for idx, doc in enumerate(documents)
    ],
)

def query_books(query):
	hits = qdrant.search(collection_name="my_books", query_vector=encoder.encode(query).tolist(), limit=3)
	for hit in hits:
		print(hit.payload, "score:", hit.score)

while True:
	query = input(">> ")
	if query == "exit":
		break
	query_books(query)
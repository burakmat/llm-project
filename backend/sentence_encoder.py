from qdrant_client import models, QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import SentenceTransformer
from data import documents

encoder = SentenceTransformer("all-MiniLM-L6-v2")

# qdrant = QdrantClient(":memory:")

qdrant = QdrantClient("http://localhost:6333")

try:
    qdrant.create_collection(
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

except UnexpectedResponse as e:
    if e.status_code == 400:
        print(
            "Collection already exists. Skipping collection creation and records upload."
        )

else:
    print("Collection is created and records are uploaded.")


def query_books(query):
    hits = qdrant.search(
        collection_name="my_books", query_vector=encoder.encode(query).tolist(), limit=3
    )
    for hit in hits:
        print(hit.payload, "score:", hit.score)


while True:
    query = input(">> ")
    if query == "exit":
        break
    query_books(query)

from django.apps import AppConfig
from ..embedder import Embedder

embedder = None

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready():
        from qdrant_client.http.exceptions import UnexpectedResponse
        from qdrant_client import models
        from data import documents
        global embedder
        embedder = Embedder()

        try:
            embedder.qdrant.create_collection(
                collection_name="my_books",
                vectors_config=models.VectorParams(
                    size=embedder.encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
                    distance=models.Distance.COSINE,
                ),
            )
            embedder.qdrant.upload_records(
                collection_name="my_books",
                records=[
                    models.Record(
                        id=idx, vector=embedder.encoder.encode(doc["description"]).tolist(), payload=doc
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

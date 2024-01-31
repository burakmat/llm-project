from django.apps import AppConfig
from embedder import Embedder

embedder = None

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
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
            books_list = []
            with open("booksummaries.txt", 'r', encoding='utf-8') as file:
                for line in file:
                    fields = line.strip().split('\t')

                    wikipedia_id, freebase_id, title, author, pub_date, genres, plot_summary = fields[:7]

                    book_info = {
                        "id": wikipedia_id,
                        "name": title,
                        "author": author,
                        "description": plot_summary[:100]
                    }

                    books_list.append(book_info)

            embedder.qdrant.upload_records(
                collection_name="my_books",
                records=[
                    models.Record(
                        id=int(book["id"]), vector=embedder.encoder.encode(book["description"]).tolist(), payload=book
                    )
                    for book in books_list[:50]
                ],
            )
        except UnexpectedResponse as e:
            if e.status_code == 400:
                print(
                    "Collection already exists. Skipping collection creation and records upload."
                )

        else:
            print("Collection is created and records are uploaded.")

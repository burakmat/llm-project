books_list = []
with open("booksummaries.txt", 'r', encoding='utf-8') as file:
    for line in file:
        fields = line.strip().split('\t')

        wikipedia_id, freebase_id, title, author, pub_date, genres, plot_summary = fields[:7]

        book_info = {
            "id": wikipedia_id,
            "name": title,
            "author": author,
            "publication": pub_date,
            "description": plot_summary
        }

        books_list.append(book_info)

print(books_list[0]["description"][:100])
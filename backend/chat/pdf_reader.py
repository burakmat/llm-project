from langchain_community.document_loaders import PyPDFLoader

book_path = "../../sample_book.pdf"

loader = PyPDFLoader(book_path)

pages = loader.load_and_split()

print(pages[2])
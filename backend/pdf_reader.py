from langchain_community.document_loaders import PyPDFLoader

book_path = "../sample_book.pdf"

def get_pdf_text(path):
    book_path = "../sample_book.pdf"
    loader = PyPDFLoader(path)
    pages = loader.load_and_split()
    read = ""
    for page in pages[:10]:
        read += page.page_content[:200]
    return read
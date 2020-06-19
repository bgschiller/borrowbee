from background_task import background
from .models import Book
from .api import fetch_book_details, BookDetails
from dataclasses import asdict


@background()
def save_book_details(isbns):
    details = fetch_book_details(isbns)
    if len(details) != len(isbns):
        print("failed to find some books on API:", set(isbns) - set(details))
    books = Book.objects.filter(isbn__in=details)
    if len(books) != len(details):
        print("failed to find some books in DB:", set(books) - set(details))
    for book in books:
        book.__dict__.update(asdict(details[book.isbn]))
    Book.objects.bulk_update(books, list(BookDetails.__dataclass_fields__))

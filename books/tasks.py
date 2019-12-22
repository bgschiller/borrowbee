from background_task import background
from .models import Book
from .api import fetch_book_details
from dataclasses import asdict


@background()
def save_book_details(isbn):
    details = fetch_book_details(isbn)
    print("details", details)
    num_altered = Book.objects.filter(isbn=isbn).update(**asdict(details))
    print("isbn", isbn, "altered", num_altered)
    if num_altered != 1:
        raise Book.DoesNotExist(isbn)

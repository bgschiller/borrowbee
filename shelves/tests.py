from django.test import TestCase
from .models import Shelf, Shelving
from books.models import Book, BookCopy

# Create your tests here.
def test_create_shelf(mk_logged_in_client):
    user, client = mk_logged_in_client()
    assert not Shelf.objects.filter(owner=user).exists()
    response = client.post("/shelves/add", {"name": "Sci-fi"})
    assert response.status_code == 302
    shelf_id = response.url.split("/")[-1]
    shelf = Shelf.objects.get(pk=shelf_id)
    assert shelf.owner_id == user.id
    assert shelf.name == "Sci-fi"


def test_shelf_detail(mk_logged_in_client):
    user, client = mk_logged_in_client()
    shelf = Shelf.objects.create(name="Sci-fi", owner=user)
    book = Book.objects.create(title="A Deepness in the Sky", isbn="0-312-85683-0")
    book_copy = BookCopy.objects.create(book=book, owner=user)

    resp = client.get(f"/shelves/{shelf.id}")
    assert resp.status_code == 200
    assert f'<option value="{book_copy.id}">' in resp.getvalue().decode(resp.charset)


def test_shelving_create(mk_logged_in_client):
    user, client = mk_logged_in_client()
    shelf = Shelf.objects.create(name="Sci-fi", owner=user)
    book = Book.objects.create(title="A Deepness in the Sky", isbn="0-312-85683-0")
    book_copy = BookCopy.objects.create(book=book, owner=user)

    resp = client.post(
        f"/shelves/{shelf.id}/shelvings/add", {"book_copy": book_copy.id}
    )
    assert resp.status_code == 302
    assert resp.url == f"/shelves/{shelf.id}"
    assert Shelving.objects.filter(shelf=shelf, book_copy=book_copy).exists()

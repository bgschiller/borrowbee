from django.db import models
from django.conf import settings
from django.urls import reverse


class Book(models.Model):
    isbn = models.CharField(unique=True, max_length=20, db_index=True)
    olid = models.CharField(unique=True, null=True, max_length=20, db_index=True)
    title = models.CharField(max_length=255, null=True, default=None)
    description = models.TextField(null=True, default=None)

    def cover_photo(self):
        return f"http://covers.openlibrary.org/b/olid/{self.olid}-L.jpg"


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("bookcopy-detail", kwargs={"bookcopy_id": self.pk})

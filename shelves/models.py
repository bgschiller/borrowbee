from django.db import models
from django.conf import settings
from django.urls import reverse


class Shelf(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    book_copies = models.ManyToManyField(
        "books.BookCopy", related_name="shelves", through="Shelving"
    )

    def get_absolute_url(self):
        return reverse("shelf-detail", kwargs={"shelf_id": self.id})

    class Meta:
        verbose_name_plural = "Shelves"


class Shelving(models.Model):
    shelf = models.ForeignKey(Shelf, null=False, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(
        "books.BookCopy", null=False, on_delete=models.CASCADE
    )


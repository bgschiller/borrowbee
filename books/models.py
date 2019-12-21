from django.db import models
from django.conf import settings
from django.urls import reverse

class Book(models.Model):
  isbn = models.CharField(unique=True, max_length=20)
  olid = models.CharField(unique=True, null=True, max_length=20)
  name = models.CharField(max_length=255)

class BookCopy(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='copies')
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)

  def get_absolute_url(self):
    return reverse('bookcopy-detail', kwargs={'bookcopy_id': self.pk})

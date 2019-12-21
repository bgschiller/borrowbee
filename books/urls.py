from django.urls import path

from .views import (
  BookCopyCreate,
  BookCopyIndex,
  BookCopyDetail,
  BookCopyDelete,
)

urlpatterns = [
  path('', BookCopyIndex.as_view(), name='my-bookcopies'),
  path('add', BookCopyCreate.as_view(), name='add-bookcopy'),
  path('<int:bookcopy_id>', BookCopyDetail.as_view(), name='bookcopy-detail'),
  path('<int:bookcopy_id>/remove', BookCopyDelete.as_view(), name='remove-bookcopy'),
]
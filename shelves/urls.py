from django.urls import path
from .views import (
    ShelfIndex,
    ShelfDetail,
    ShelfCreate,
    ShelfDelete,
    ShelvingCreate,
    ShelvingDelete,
)

urlpatterns = [
    path("", ShelfIndex.as_view(), name="my-shelves"),
    path("add", ShelfCreate.as_view(), name="shelf-create"),
    path("<int:shelf_id>", ShelfDetail.as_view(), name="shelf-detail"),
    path("<int:shelf_id>/delete", ShelfDelete.as_view(), name="shelf-delete"),
    path(
        "<int:shelf_id>/shelvings/add", ShelvingCreate.as_view(), name="shelving-create"
    ),
    path(
        "<int:shelf_id>/shelvings/<int:shelving_id>/delete",
        ShelvingDelete.as_view(),
        name="shelving-delete",
    ),
]


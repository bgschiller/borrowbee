from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Shelf, Shelving


class UserOwnsShelfMixin(UserPassesTestMixin):
    def test_func(self):
        shelf_id = self.kwargs["shelf_id"]
        return Shelf.objects.filter(owner_id=self.request.user.id, id=shelf_id).exists()


class UserOwnsShelvingMixin(UserPassesTestMixin):
    def test_func(self):
        shelving = Shelving.objects.filter(
            id=self.kwargs["shelving_id"]
        ).select_related("shelf", "book_copy")
        return (
            shelving.shelf.owner_id == self.request.user.id
            and shelving.book_copy.owner_id == self.request.user.id
        )

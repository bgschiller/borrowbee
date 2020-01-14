from django.forms import ModelForm
from .models import Shelf, Shelving


class CreateShelfForm(ModelForm):
    class Meta:
        model = Shelf
        fields = ["name"]


class CreateShelvingForm(ModelForm):
    class Meta:
        model = Shelving
        fields = ["book_copy"]


from django import forms


class CreateBookCopyForm(forms.Form):
    isbn = forms.CharField(label="isbn", max_length=20)

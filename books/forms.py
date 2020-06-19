from django import forms


class CreateBookCopyForm(forms.Form):
    isbns = forms.CharField(
        label="isbns", widget=forms.Textarea({"placeholder": "isbns"})
    )

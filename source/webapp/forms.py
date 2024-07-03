from django import forms
from django.forms import widgets


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=50, required=True, label="Name")
    author = forms.CharField(
        max_length=50,
        required=False,
        label="Author",
        widget=widgets.Input(attrs={"placeholder": "Author"}),
    )
    content = forms.CharField(
        max_length=3000,
        required=True,
        label="Content",
        widget=forms.Textarea(attrs={"cols":40, "rows":4, "placeholder":"Content"}),
    )
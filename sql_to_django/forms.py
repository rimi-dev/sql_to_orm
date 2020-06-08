from django import forms

from sql_to_django.widgets import DivContentEditable


class QueryInputForm(forms.Form):
    query = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Please input working SQL query.'}))
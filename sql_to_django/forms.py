from django import forms

from sql_to_django.widgets import DivContentEditable


class QueryInputForm(forms.Form):
    fk_check = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input', 'disabled': 'true'}))
    query = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '정상작동하는 SQL 구문을 넣어주세요.'}))
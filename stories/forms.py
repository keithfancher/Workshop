from django import forms

class SearchForm(forms.Form):
    search_string = forms.CharField(label='')

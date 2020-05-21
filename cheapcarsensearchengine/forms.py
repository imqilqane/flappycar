from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(max_length=60, widget=forms.TextInput(attrs={
        'id':'search',
        'placeholder':'Search',
        'autocomplete':'off',
        'type':'text',
        }))
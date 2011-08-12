from django import forms
from django.forms import ModelForm

from workshop.stories.models import Story


class SearchForm(forms.Form):
    search_string = forms.CharField(label='')


class StoryForm(ModelForm):
    # make these look less stupid
    title = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'size': 64}))
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 25, 'cols': 50}))

    class Meta:
        model = Story
        fields = ('title', 'text')

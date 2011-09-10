from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from workshop.stories.models import Story, Author


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


class AuthorForm(ModelForm):
    
    class Meta:
        model = Author
        fields = ('profile',)


class BetterUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", help_text="I will never send you spam. I will only email you for damn good reasons.")

    class Meta:
        model = User
        fields = ('username', 'email')

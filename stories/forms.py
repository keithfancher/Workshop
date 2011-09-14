from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from workshop.stories.models import Story, Author


class SearchForm(forms.Form):
    q = forms.CharField(label='')


class StoryForm(ModelForm):
    # make these look less stupid
    title = forms.CharField(max_length=100,
        widget=forms.TextInput(attrs={'size': 61}))
    author_note = forms.CharField(widget=forms.Textarea(attrs={'class': 'author_note'}), required=False,
                                                        help_text="Optional. Give us a little context, if you like.")
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 25, 'cols': 50}),
                                                 help_text="Just copy/paste it right in. No formatting as of yet.")

    class Meta:
        model = Story
        fields = ('title', 'author_note', 'text')


class AuthorForm(ModelForm):

    class Meta:
        model = Author
        fields = ('byline', 'author_bio',)


class BetterUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", help_text="I will never send you spam. I will only email you for damn good reasons.")

    class Meta:
        model = User
        fields = ('username', 'email')

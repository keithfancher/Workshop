from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from workshop.stories.forms import SearchForm
from workshop.stories.models import Author
from workshop.stories.models import Story


def index(request):
    return render_to_response('index.html',
        context_instance=RequestContext(request))

# TODO: can replace this w/ generic view... do I want to?
def stories(request):
    story_list = Story.objects.all()
    return render_to_response('stories.html', 
        {'stories': story_list},
        context_instance=RequestContext(request))

def story(request, story_id):
    story = Story.objects.get(id=story_id)
    # TODO: add some error checking here
    return render_to_response('story.html',
        {'story': story},
        context_instance=RequestContext(request))

# TODO: can replace this w/ generic view... do I want to?
def authors(request):
    author_list = Author.objects.all()
    return render_to_response('authors.html', 
        {'authors': author_list},
        context_instance=RequestContext(request))

def author(request, author_id):
    author = Author.objects.get(id=author_id)
    stories = author.story_set.all()
    # TODO: error checking
    return render_to_response('author.html', 
        {'author': author, 'stories': stories},
        context_instance=RequestContext(request))

def search(request):
    if 'search_string' in request.GET:
        query = request.GET['search_string']
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            # TODO: search here
            return render_to_response('search_results.html', 
                {'form': form, 'query': query})
    else:
        form = SearchForm()
    return render_to_response('search_form.html',
        {'form': form},
        context_instance=RequestContext(request))        

# TODO: don't let this happen if already logged in?
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("index.html") # TODO: redirect to where?
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html",
        {'form': form},
        context_instance=RequestContext(request))

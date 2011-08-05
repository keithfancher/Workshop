from django.http import HttpResponse
from django.shortcuts import render_to_response

from workshop.stories.forms import SearchForm
from workshop.stories.models import Author
from workshop.stories.models import Story


def index(request):
    return render_to_response('index.html')

def stories(request):
    story_list = Story.objects.all()
    return render_to_response('stories.html', {'stories': story_list})

def story(request, story_id):
    story = Story.objects.get(id=story_id)
    # TODO: add some error checking here
    return render_to_response('story.html', {'story': story})

def authors(request):
    author_list = Author.objects.all()
    return render_to_response('authors.html', {'authors': author_list})

def author(request, author_id):
    author = Author.objects.get(id=author_id)
    stories = author.story_set.all()
    # TODO: error checking
    return render_to_response('author.html', {'author': author, 'stories': stories})

def about(request):
    return render_to_response('about.html')

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
    return render_to_response('search_form.html', {'form': form})        

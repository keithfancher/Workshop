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

def authors(request):
    author_list = Author.objects.all()
    return render_to_response('authors.html', {'authors': author_list})

def about(request):
    return render_to_response('about.html')

def search(request):
    if 'search_string' in request.GET:
        query = request.GET['search_string']
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            # search here TODO
            return render_to_response('search_results.html', 
                {'form': form, 'query': query})
    else:
        form = SearchForm()
    return render_to_response('search_form.html', {'form': form})        

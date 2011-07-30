from django.http import HttpResponse
from django.shortcuts import render_to_response

from workshop.stories.forms import SearchForm


def index(request):
    return render_to_response('index.html')

def stories(request):
    return render_to_response('stories.html')

def authors(request):
    return render_to_response('authors.html')

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

from django.db.models import Q
from django.http import HttpResponseForbidden
from django.template import RequestContext, loader

from workshop.stories.models import Story
from workshop.stories.models import Author


# Because there's no fucking Http403 exception??? Seriously? At least in Django
# 1.1...
def error_403(request):
    t = loader.get_template('403.html')
    c = RequestContext(request)
    return HttpResponseForbidden(t.render(c))

def search_stories(query):
    results = Story.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query)
    )
    return results

def search_authors(query):
    results = Author.objects.filter(
        Q(byline__icontains=query) | Q(author_bio__icontains=query)
    )
    return results

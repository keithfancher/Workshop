from datetime import date

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from workshop.stories.forms import SearchForm
from workshop.stories.forms import StoryForm
from workshop.stories.forms import AuthorForm
from workshop.stories.forms import BetterUserCreationForm
from workshop.stories.models import Author
from workshop.stories.models import Story


#
# View the index page
#
def index(request):
    return render_to_response('index.html',
        context_instance=RequestContext(request))

#
# View the list of stories
#
def stories(request):
    story_list = Story.objects.all()
    return render_to_response('stories.html', 
        {'stories': story_list},
        context_instance=RequestContext(request))

#   
# View a given story
#
def story(request, story_id):
    # Check if story exists
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        error_text = "That story doesn't exist!"
        return render_to_response('error.html',
            {'error_text': error_text},
            context_instance=RequestContext(request))

    # Check if it's our own story
    # get_profile() fails if it's Anon user, so check that too...
    if request.user.is_authenticated():
        own_story = request.user.get_profile().owns_story(story_id)
    else:
        own_story = False

    return render_to_response('story.html',
        {'story': story, 'own_story': own_story},
        context_instance=RequestContext(request))

#    
# Create a new story    
#
@login_required    
def new_story(request):
    # If a POST request, create new story
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            # Need to set author as current user
            new_story = form.save(commit=False)
            new_story.author = request.user # TODO: should this be user.id?
            new_story.pub_date = date.today()
            new_story.save() # have to explicitly save here
            return HttpResponseRedirect('/story/' + str(new_story.id) + '/')

    # If a GET request, display the form
    else:
        form = StoryForm()
        return render_to_response('new_story.html',
            {'form': form},
            context_instance=RequestContext(request))

#    
# Edit an existing story
#
@login_required    
def edit_story(request, story_id):
    # Check if story exists
    try:
        story = Story.objects.get(id=story_id)
    except:
        error_text = "That story doesn't exist!"
        return render_to_response('error.html',
            {'error_text': error_text},
            context_instance=RequestContext(request))

    # Check if user owns the story
    if not request.user.get_profile().owns_story(story_id):
        error_text = "That ain't yours to edit, okay?"
        return render_to_response('error.html',
            {'error_text': error_text},
            context_instance=RequestContext(request))

    # It's a POST request, save the story
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid(): # do I need to check this?
            form.save()
            return HttpResponseRedirect('/story/' + story_id + '/')

    # It's a GET request, just display the form
    else:
        form = StoryForm(instance=story)
        return render_to_response('edit_story.html',
            {'story': story,'form': form},
            context_instance=RequestContext(request))

#
# View the list of authors (users)
#
def authors(request):
    author_list = User.objects.all()
    return render_to_response('authors.html', 
        {'authors': author_list},
        context_instance=RequestContext(request))

#
# View a given author's profile page
#
def author(request, author_id):
    author = User.objects.get(id=author_id)
    stories = author.story_set.all()
    # TODO: error checking
    return render_to_response('author.html', 
        {'author': author, 'stories': stories},
        context_instance=RequestContext(request))

#
# Lets a logged in user view their profile
#
@login_required    
def profile(request):
    author = request.user
    stories = author.story_set.all()
    # TODO: error checking
    return render_to_response('registration/profile.html', 
        {'stories': stories},
        context_instance=RequestContext(request))

#
# Edit your profile
#
@login_required    
def edit_profile(request):
    # POST request, save the profile
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/profile/')

    # GET request, display the form
    else:
        form = AuthorForm(instance=request.user.get_profile())
        return render_to_response('registration/edit_profile.html',
            {'form': form},
            context_instance=RequestContext(request))            

#
# Search authors and stories. TODO: Doesn't exist yet!
#
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

#
# View the registration page
#
def register(request):
    # TODO: don't let this happen if already logged in?
    if request.method == 'POST':
        form = BetterUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("index.html") # TODO: redirect to where?
    else:
        form = BetterUserCreationForm()
    return render_to_response("registration/register.html",
        {'form': form},
        context_instance=RequestContext(request))

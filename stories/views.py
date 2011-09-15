from datetime import date

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from workshop.stories.forms import SearchForm
from workshop.stories.forms import StoryForm
from workshop.stories.forms import AuthorForm
from workshop.stories.forms import BetterUserCreationForm
from workshop.stories.models import Author
from workshop.stories.models import Story
from workshop.stories.helpers import error_403, search_stories, search_authors


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
    return render_to_response('stories/index.html',
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
        raise Http404

    # Check if it's our own story
    # get_profile() fails if it's Anon user, so check that too...
    if request.user.is_authenticated():
        own_story = request.user.get_profile().owns_story(story_id)
    else:
        own_story = False

    return render_to_response('stories/show.html',
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
            # Need to set author and date before saving
            new_story = form.save(commit=False)
            new_story.author = request.user
            new_story.pub_date = date.today()
            new_story.save() # have to explicitly save here
            return HttpResponseRedirect('/stories/' + str(new_story.id) + '/')

    # If a GET request, display the form
    else:
        form = StoryForm()

    # Make sure to return a response even if form is invalid... re-show form
    return render_to_response('stories/new.html',
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
    except Story.DoesNotExist:
        raise Http404

    # Check if user owns the story
    if not request.user.get_profile().owns_story(story_id):
        return error_403(request)

    # It's a POST request, save the story
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/stories/' + story_id + '/')

    # It's a GET request, just display the form
    else:
        form = StoryForm(instance=story)

    return render_to_response('stories/edit.html',
        {'story': story,'form': form},
        context_instance=RequestContext(request))

#
# Delete an existing story and attached comments
#
@login_required
def delete_story(request, story_id):
    # Make sure the story exists
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        raise Http404

    # Check if user owns the story
    if not request.user.get_profile().owns_story(story_id):
        return error_403(request)

    # If it's a POST request, delete the story and attached comments
    if request.method == 'POST':
        # Check a hidden value in the form, sort-of confirmation
        # TODO: does this matter at all? Probably not. Probably delete this.
        confirmation = request.POST.get('confirm', 'false')

        # If it's true, delete the story and its comments
        if confirmation == 'true':
            Comment.objects.filter(object_pk=story.id).delete()
            story.delete()
            return render_to_response('stories/deleted_message.html',
                context_instance=RequestContext(request))

        # If the hidden field not set correctly, just re-show the confirmation
        else:
            return render_to_response('stories/delete.html',
                context_instance=RequestContext(request))

    # If it's a GET request, show the confirmation page
    else:
        return render_to_response('stories/delete.html',
            context_instance=RequestContext(request))

#
# View the list of authors (users)
#
def authors(request):
    author_list = User.objects.all()
    return render_to_response('authors/index.html',
        {'authors': author_list},
        context_instance=RequestContext(request))

#
# View a given author's profile page
#
def author(request, author_id):
    try:
        author = User.objects.get(id=author_id)
    except User.DoesNotExist:
        raise Http404

    stories = author.story_set.all()
    return render_to_response('authors/show.html',
        {'author': author, 'stories': stories},
        context_instance=RequestContext(request))

#
# Lets a logged in user view their profile
#
@login_required
def profile(request):
    author = request.user
    stories = author.story_set.all()
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
            return HttpResponseRedirect('/profile/')

    # GET request, display the form
    else:
        form = AuthorForm(instance=request.user.get_profile())
        return render_to_response('registration/edit_profile.html',
            {'form': form},
            context_instance=RequestContext(request))

#
# Search authors and stories.
#
def search(request):
    # show results for given query
    if 'q' in request.GET:
        query = request.GET['q']
        story_results = search_stories(query)
        author_results = search_authors(query)
        return render_to_response('search_results.html',
                                  {'query': query,
                                   'story_results': story_results,
                                   'author_results': author_results},
                                  context_instance=RequestContext(request))
    # otherwise just show form
    else:
        form = SearchForm()
        return render_to_response('search_form.html', {'form': form},
                                  context_instance=RequestContext(request))

#
# View the registration page
#
def register(request):
    if request.method == 'POST':
        form = BetterUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # have to call authenticate for login() to work, even though the
            # user object is returned by form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user) # actually log in new user
            return HttpResponseRedirect("/profile/")
    else:
        form = BetterUserCreationForm()
    return render_to_response("registration/register.html",
        {'form': form},
        context_instance=RequestContext(request))

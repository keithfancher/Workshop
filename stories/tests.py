from datetime import date

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from workshop.stories.models import Story


"""
TOTEST:
- must be logged in to post comments
- comments form
- signup/signin forms
- profile form

doesn't exist yet:
- if logged in, login link should redirect to profile page?
"""


class CommentsTest(TestCase):
    def setUp(self):
        pass

class StoryFormsTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

        # add an existing story to the db
        self.story = Story()
        self.story.title = "This is a great story, yeah?"
        self.story.author = self.user
        self.story.pub_date = date.today()
        self.story.text = "This is the text of the story. Awesome!"
        self.story.save()

    def test_new_story_form_invalid(self):
        """invalid new story input should show errors and re-display the new
        story form"""
        self.c.login(username='test', password='test')
        data = {'title': '', 'text': ''}
        response = self.c.post('/stories/new/', data)
        # should be re-rendering the new story template, with errors
        self.assertTemplateUsed(response, 'stories/new.html')

    def test_new_story_form_valid(self):
        """valid new story input should create new story and redirect to it"""
        self.c.login(username='test', password='test')
        data = {'title': 'a title', 'text': 'some text'}
        response = self.c.post('/stories/new/', data)
        # should be redirecting to the new story... it's the second story after
        # the one added in setUp, so it should be number 2
        self.assertRedirects(response, '/stories/2/')

    def test_edit_story_form_invalid(self):
        """invalid edit story form should show errors and redisplay form"""
        self.c.login(username='test', password='test')
        data = {'title': '', 'text': ''}
        response = self.c.post('/stories/' + str(self.story.id) + '/edit/',
                               data)
        # should be re-rendering the edit story template, with errors
        self.assertTemplateUsed(response, 'stories/edit.html')

    def test_edit_story_form_valid(self):
        """valid edit story form should show save the story and redirect to
        it"""
        self.c.login(username='test', password='test')
        data = {'title': 'A better story', 'text': 'Way cool, man.'}
        response = self.c.post('/stories/' + str(self.story.id) + '/edit/',
                               data)
        self.assertRedirects(response, '/stories/' + str(self.story.id)  + '/')


class StoriesTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user1 = User.objects.create_user('test1', 'test1@example.com',
                                              'test1')
        self.user2 = User.objects.create_user('test2', 'test2@example.com',
                                              'test2')
        # add an existing story to the db
        self.story = Story()
        self.story.title = "This is a great story, yeah?"
        self.story.author = self.user1
        self.story.pub_date = date.today()
        self.story.text = "This is the text of the story. Awesome!"
        self.story.save()

    def test_user_cant_edit_others_story(self):
        self.c.login(username='test2', password='test2')
        response = self.c.get('/stories/1/edit/')
        self.failUnlessEqual(response.status_code, 403)

    def test_user_cant_delete_others_story(self):
        self.c.login(username='test2', password='test2')
        response = self.c.get('/stories/1/delete/')
        self.failUnlessEqual(response.status_code, 403)

    def test_create_story(self):
        pass


class UrlTest(TestCase):

    # these don't require authentication, or anything special
    urls_basic = ('/',
                  '/about/',
                  '/search/',
                  '/login/',
                  '/logout/',
                  '/register/',
                  '/stories/',
                  '/authors/',
                  '/stories/1/',
                 )

    # these require the user to be logged in
    urls_auth = ('/profile/',
                 '/profile/edit/',
                 '/stories/new/',
                 '/stories/1/edit/',
                 '/stories/1/delete/',
                )

    # fail!
    should_404 = ('/stories/23423423423/',
                  '/stories/asdffsadfasdf/',
                  '/authors/asdfasdfsda/',
                  '/authors/23423423/',
                  '/fsdafower/',
                 )

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

        # add an existing story to the db, owned by self.user
        self.story = Story()
        self.story.title = "This is a great story, yeah?"
        self.story.author = self.user
        self.story.pub_date = date.today()
        self.story.text = "This is the text of the story. Awesome!"
        self.story.save()

    def test_basic_urls(self):
        """basic URLs should return response code 200"""
        self.url_test_helper(self.urls_basic, 200)

    def test_auth_urls_anon(self):
        """auth URLs should redirect if not logged in"""
        self.url_test_helper(self.urls_auth, 302)

    def test_auth_urls_logged_in(self):
        """auth URLs should return response 200 if logged in"""
        self.c.login(username='test', password='test')
        self.url_test_helper(self.urls_auth, 200)

    def test_bad_urls(self):
        """bad URLs should return 404 response code"""
        self.url_test_helper(self.should_404, 404)

    def url_test_helper(self, urls, expected_response):
        """Loops through a list of URLs and makes sure each one returns the
        expected response."""
        for url in urls:
            response = self.c.get(url)
            self.failUnlessEqual(response.status_code, expected_response)

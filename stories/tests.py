from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from workshop.stories.models import Story


"""
- edit story form properly validates

- can't edit others' story
- can't edit others' profile
- can't delete others' story
- logged out user can't edit/delete anything (story/profile)

- must be logged in to post comments

- test the forms (signup, sign in, add/edit story, profile)
- test the URLs?
- test that URLs get correct views?

doesn't exist yet:
(- if logged in, login link should redirect to profile page)
"""


class CommentsTest(TestCase):
    def setUp(self):
        pass

class StoryFormsTest(TestCase):
    def setUp(self):
        self.c = Client()
        user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_new_story_form_invalid(self):
        """invalid input should show errors and re-display the new story form"""
        self.c.login(username='test', password='test')
        data = {'title': '', 'text': ''}
        response = self.c.post('/stories/new/', data)
        # should be re-rendering the new story template, with errors
        # use assertFormError()?
        self.assertTemplateUsed(response, 'stories/new.html')

    def test_new_story_form_valid(self):
        """valid input should create new story and redirect to it"""
        self.c.login(username='test', password='test')
        data = {'title': 'a title', 'text': 'some text'}
        response = self.c.post('/stories/new/', data)
        # should be redirecting to the new story... it's the first added, so it
        # should be number 1
        self.assertRedirects(response, '/stories/1/')


class StoriesTest(TestCase):
    def setUp(self):
        self.c = Client()
        user1 = User.objects.create_user('test1', 'test1@example.com', 'test1')
        user2 = User.objects.create_user('test2', 'test2@example.com', 'test2')

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
                 )

    # these require the user to be logged in
    urls_auth = ('/profile/',
                 '/profile/edit/',
                 '/stories/new/',
                )

    should_404 = ('/stories/23423423423/',
                  '/stories/asdffsadfasdf/',
                  '/authors/asdfasdfsda/',
                  '/authors/23423423/',
                  '/fsdafower/',
                 )

    def setUp(self):
        self.c = Client()
        user = User.objects.create_user('test', 'test@example.com', 'test')

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

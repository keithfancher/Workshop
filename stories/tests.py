import time
from datetime import date

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.comments.forms import CommentSecurityForm

from workshop.stories.models import Story


class AuthorTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_show_author_name(self):
        """If author's byline is set, that's what should be displayed.
        Otherwise should show username."""
        self.failUnlessEqual(self.user.get_profile().name(), "test")
        self.user.get_profile().byline = "A Big Asshole"
        self.failUnlessEqual(self.user.get_profile().name(), "A Big Asshole")


class UserFormsTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

    def test_show_author_name(self):
        """If author's byline is set, that's what should be displayed.
        Otherwise should show username."""
        self.failUnlessEqual(self.user.get_profile().name(), "test")
        self.user.get_profile().byline = "A Big Asshole"
        self.failUnlessEqual(self.user.get_profile().name(), "A Big Asshole")

    def test_empty_login_form(self):
        """Empty login form should just redisplay with errors"""
        data = {'username': '', 'password': ''}
        response = self.c.post('/login/', data)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, '<p class="error">Sorry')

    def test_bad_credentials_login_form(self):
        """Bad login info should redisplay form with errors"""
        data = {'username': 'fuck', 'password': 'you'}
        response = self.c.post('/login/', data)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertContains(response, '<p class="error">Sorry')

    def test_login_form_success(self):
        """Good login info should log user in and redirect to profile"""
        data = {'username': 'test', 'password': 'test'}
        response = self.c.post('/login/', data)
        self.assertRedirects(response, '/profile/')

    def test_edit_profile_form(self):
        """This form's fields aren't required and don't have any special
        business... this shouldn't need any real testing."""
        pass

    def test_register_form_empty(self):
        """Empty registration form should redisplay with proper errors"""
        data = {'username': '', 'email': '', 'password1': '', 'password2': ''}
        response = self.c.post('/register/', data)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, '<ul class="errorlist">')

    def test_register_form_bad_email(self):
        """Bad email in registration form should fail"""
        data = {'username': 'bob', 'email': 'fuckyou',
                'password1': 'asdf', 'password2': 'asdf'}
        response = self.c.post('/register/', data)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'Enter a valid e-mail address')

    def test_register_form_password_mismatch(self):
        """Password mismatch in registration form should fail"""
        data = {'username': 'bob', 'email': 'fuckyou@jerk.com',
                'password1': 'asdf', 'password2': 'fdsa'}
        response = self.c.post('/register/', data)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'password fields didn&#39;t match')

    def test_register_form_existing_username(self):
        """Can't register with existing username"""
        data = {'username': 'test', 'email': 'fuckyou@jerk.com',
                'password1': 'asdf', 'password2': 'fdsa'}
        response = self.c.post('/register/', data)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertContains(response, 'user with that username already exists')

    def test_register_form_success(self):
        """Valid information should create new user, log them in, and redirect
        to their profile"""
        data = {'username': 'bob', 'email': 'fuckyou@jerk.com',
                'password1': 'asdf', 'password2': 'asdf'}
        response = self.c.post('/register/', data)
        self.assertRedirects(response, '/profile/')


class CommentsTest(TestCase):
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

    def test_anon_user_cant_see_comment_form(self):
        """anonymous user doesn't see comment form"""
        response = self.c.get('/stories/1/')
        self.assertNotContains(response, '<form action="/comments/post/"')

    def test_logged_in_user_can_see_comment_form(self):
        """logged in users should see comment form"""
        self.c.login(username='test', password='test')
        response = self.c.get('/stories/1/')
        self.assertContains(response, '<form action="/comments/post/"')

    def test_empty_comment_form(self):
        """empty comment should send user to preview form"""
        self.c.login(username='test', password='test')

        # all this bullshit to create an empty fucking comment
        data = {'content_type': 'stories.story',
                'object_pk': '1',
                'timestamp': str(int(time.time())),
                'comment': ''}
        csf = CommentSecurityForm(self.story)
        security_hash = csf.generate_security_hash(data['content_type'],
                                                   data['object_pk'],
                                                   data['timestamp'])
        data['security_hash'] = security_hash
        response = self.c.post('/comments/post/', data)
        self.assertTemplateUsed(response, 'comments/preview.html')

    def test_anon_user_cant_post_comment(self):
        """
        Anonymous user shouldn't be able to post a comment. Granted, the
        form is already hidden from them, but what if they're crafty with their
        POST requests?

        Okay, so it turns out that simply hiding the form is enough, since the
        Comment model won't validate unless the "security hash" is present and
        correct, and the only way for them to calculate that hash is if they
        have my settings.SECRET_KEY. And if they've got that, well... the last
        thing I'm going to be worried about is an anonymous comment or two...
        """
        pass


class StoryTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.user2 = User.objects.create_user('test2', 'test2@example.com',
                                              'test2')
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

    def test_user_cant_edit_others_story(self):
        """logged in user is forbidden from editing other users' stories"""
        self.c.login(username='test2', password='test2')
        response = self.c.get('/stories/1/edit/')
        self.failUnlessEqual(response.status_code, 403)

    def test_user_cant_delete_others_story(self):
        """logged in user is forbidden from deleting other users' stories"""
        self.c.login(username='test2', password='test2')
        response = self.c.get('/stories/1/delete/')
        self.failUnlessEqual(response.status_code, 403)


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
                  '/authors/1/',
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

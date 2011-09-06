from django.test import TestCase
from django.test.client import Client


"""
- if logged in, login link should redirect to profile page
- can't edit others' story
- can't edit others' profile
- can't delete others' story
- logged out user can't edit/delete anything (story/profile)

- must be logged in to post comments

- test the forms (signup, sign in, add/edit story, profile)
- test the URLs?
"""


class UrlTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_basic_urls(self):
        urls_200 = ('/',
                    '/about/',
                    '/search/',
                   )
        self.url_test_helper(urls_200, 200)


    def test_auth_urls(self):
        urls_200 = ('/accounts/login/', 
                    '/accounts/logout/', 
                    '/accounts/register/',
                   )
        urls_302 = ('/accounts/profile/',
                    '/accounts/profile/edit/',
                   )

        self.url_test_helper(urls_200, 200)
        self.url_test_helper(urls_302, 302)

    def test_stories_urls(self):
        urls_200 = ('/stories/',)
        urls_302 = ('/story/new/',)
        urls_404 = ('/story/asdfsdafsda/',
                    '/story/23423432432/')

        self.url_test_helper(urls_200, 200)
        self.url_test_helper(urls_302, 302)
#        self.url_test_helper(urls_404, 404)

    def test_authors_urls(self):
        urls_200 = ('/authors/',)
        urls_404 = ('/authors/sadfsadfsadfsad/',
                    '/authors/23423423423/',
                   )
        self.url_test_helper(urls_200, 200)
#        self.url_test_helper(urls_404, 404)

    def url_test_helper(self, urls, expected_response):
        """Loops through a list of URLs and makes sure each one returns the
        expected response."""
        for url in urls:
            response = self.c.get(url)
            self.failUnlessEqual(response.status_code, expected_response)

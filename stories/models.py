from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Author(models.Model):
    # Makes Author essentially a "user profile", extending User.
    user = models.ForeignKey(User, unique=True)
    author_bio = models.TextField(blank=True,
                                  help_text="Tell us a little about yourself.")
    byline = models.CharField(max_length=100, blank=True,
                              help_text="If you leave this blank, your username will be displayed instead.")

    # Does this Author own a given Story?
    def owns_story(self, story_id):
        try:
            self.user.story_set.get(id=story_id)
        except Story.DoesNotExist:
            return False
        return True

    # If user has a byline, display that. Otherwise show username.
    def name(self):
        if self.byline:
            return self.byline
        else:
            return self.user.username

    def __unicode__(self):
        return self.name()

#    class Meta:
#        ordering = ['last_name']


class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True) # changed from Author to User
    pub_date = models.DateField()
    text = models.TextField() # no max size?
    author_note = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    # VERY basic formatting
    #
    # TODO: Probably delete this, since in order to actually use it I need to
    # allow HTML to NOT be escaped, which is bad. Replacing with
    # add_line_breaks() function below, which rules.
    def web_output(self):
        # make different first par later
        web_out = '<p class="story_par">' + self.text
        return web_out.replace("\n", '</p><p class="story_par">') + '</p>'

    # This doubles every line break for the inputted story. This allows users
    # to just copy/paste from Word/OOo documents, and the |linebreaks filter
    # will properly split up the paragraphs. My previous solution (using
    # web_output) was NOT safe, and allowed user-input HTML.
    #
    # This should be called when the story is first created, but after that it
    # shouldn't need to be used anymore.
    def add_line_breaks(self):
        self.text = self.text.replace("\n", "\n\n")

    class Meta:
        ordering = ['title']


# creates an Author object for every User created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Author.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

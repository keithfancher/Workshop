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

    # Override Model.save() so the text is always preprocessed before it's
    # saved.
    def save(self, *args, **kwargs):
        self.preprocess_text()
        super(Story, self).save(*args, **kwargs)

    # This turns indent-style paragraphs into a more web-friendly format. This
    # allows users to simply copy/paste their stories in straight from a word
    # processor rather than typing or formatting by hand.
    def preprocess_text(self):
        self.text = self.text.replace("\t", "\n") # AHA! 1 or two \n's though?

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'stories'

    def __unicode__(self):
        return self.title


# creates an Author object for every User created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Author.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

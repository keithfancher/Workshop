from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Author(models.Model):
    # Makes Author essentially a "user profile", extending User.
    user = models.ForeignKey(User, unique=True)
    profile = models.TextField()

    # Does this Author own a given Story?
    def owns_story(self, story_id):
        try:
            self.user.story_set.get(id=story_id)
        except Story.DoesNotExist:
            return False
        return True

    # Output the user's full name
    def __unicode__(self):
        return self.user.get_full_name()

#    class Meta:
#        ordering = ['last_name']


class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, blank=True) # changed from Author to User
    pub_date = models.DateField()
    text = models.TextField() # no max size?

    def __unicode__(self):
        return self.title

    # VERY basic formatting
    # TODO: sanitize! and make better
    def web_output(self):
        # make different first par later
        web_out = '<p class="story_par">' + self.text
        return web_out.replace("\n", '</p><p class="story_par">') + '</p>'

    class Meta:
        ordering = ['title']


# creates an Author object for every User created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Author.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)        

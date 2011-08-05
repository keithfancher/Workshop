from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    user_name = models.CharField(max_length=30, blank=True) # ???
#    profile = models.TextField() # TODO: breaking everything, figure out adding columns later

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']


class Story(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, blank=True)
    pub_date = models.DateField()
    text = models.TextField() # no max?

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


# are comments handled elsewhere in Django?
# class Comment(models.Model):

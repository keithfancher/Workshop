from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template

from workshop.stories import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^workshop/', include('workshop.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^login/$', login), # TODO: check if already logged in/out?
    (r'^logout/$', logout),
    (r'^register/$', views.register),
    (r'^profile/$', views.profile),
    (r'^profile/edit/$', views.edit_profile),

    (r'^$', views.index),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^search/$', views.search),

    (r'^authors/$', views.authors),
    (r'^authors/(\d+)/$', views.author),

    (r'^stories/$', views.stories),
    (r'^stories/(\d+)/$', views.story),
    (r'^stories/new/$', views.new_story),
    (r'^stories/(\d+)/edit/$', views.edit_story),
    (r'^stories/(\d+)/delete/$', views.delete_story), #TODO: use DELETE http
)

# Serve static files, but only in dev environment
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

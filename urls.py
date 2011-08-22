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

    # TODO: login redirects to nonexistent page
    (r'^accounts/login/$', login), # TODO: check if already logged in/out?
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', views.register),
    (r'^accounts/profile/$', views.profile),
    (r'^accounts/profile/edit/$', views.edit_profile),

    (r'^$', views.index),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^authors/$', views.authors),
    (r'^author/(\d+)/$', views.author),
    (r'^search/$', views.search),
    (r'^stories/$', views.stories),
    (r'^story/(\d+)/$', views.story),
    (r'^story/(\d+)/edit/$', views.edit_story),
    (r'^story/(\d+)/delete/$', views.delete_story),
    (r'^story/new/$', views.new_story),

    (r'^comments/', include('django.contrib.comments.urls')),
)

# Serve static files, but only in dev environment
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

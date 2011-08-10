from django.conf.urls.defaults import *
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

    (r'^accounts/login/$', login), # TODO: check if already logged in/out?
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', views.register),
    (r'^accounts/profile/$', direct_to_template, {'template': 'registration/profile.html'}),

    (r'^$', views.index),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
    (r'^authors/$', views.authors),
    (r'^author/(\d+)/$', views.author),
    (r'^search/$', views.search),
    (r'^stories/$', views.stories),
    (r'^story/(\d+)/$', views.story),
)

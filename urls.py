from django.conf.urls.defaults import *

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

    (r'^$', views.index),
    (r'^about/$', views.about),
    (r'^authors/$', views.authors),
    (r'^author/(\d+)/$', views.author),
    (r'^search/$', views.search),
    (r'^stories/$', views.stories),
    (r'^story/(\d+)/$', views.story),
)

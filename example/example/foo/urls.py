from django.conf.urls import *

urlpatterns = patterns('foo.views',
    # Listing URL
    url(r'^$', view='browse', name='foo.browse'),

    # Detail URL
    url(r'^(?P<slug>(?!overview\-)[\w\-\_\.\,]+)/$', view='detail', name='foo.detail'),
)
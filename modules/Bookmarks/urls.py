from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
    url(r'^bookmark/(?P<actionType>[\w|\W]+)/(?P<deviceID>\d+)/(?P<commandID>\d+)/$', 'Bookmarks.views.bookmark'),
    url(r'^bookmark_actions/$', 'Bookmarks.views.bookmarkActions'),
)

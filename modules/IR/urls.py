from django.conf.urls.defaults import patterns, include, url

urls = patterns('', 
   url(r'^ir/transceivers/$', 'IR.views.transceivers'),
   url(r'^ir/devices/$', 'IR.views.devices'),
   url(r'^ir/device/(?P<num>\d+)/$', 'IR.views.device'),
   url(r'^ir/transceiverSearch/$', 'IR.views.transceiverSearch'),
   url(r'^ir/recordAction/$', 'IR.views.recordAction'),
   url(r'^ir/$', 'IR.views.main'),
)

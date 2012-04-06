from django.conf.urls.defaults import *

urlpatterns = patterns('django_wm.views',
    url(r'^payment/$', 'request_payment'),
    url(r'^process/$', 'process_payment'),
)

from django.conf.urls import url
from . import views

import os
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

urlpatterns = [
    # ex: /visiondemo
    url(r'^$', views.index, name='index'),
    # ex: /visiondemo/fileupload
    url(r'^fileupload/$', views.fileupload, name='fileupload'),
    # ex: /visiondemo/result
    url(r'^result/$', views.result, name='result'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': MEDIA_ROOT}),
]

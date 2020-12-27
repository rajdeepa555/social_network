from django.conf.urls import url
from django.contrib import admin
from .views import (createpost, detail_post_view, postpreference)

urlpatterns = [
     url(r'^create/', createpost, name='createpost'),
     url(r'^(?P<id>\d+)/$', detail_post_view, name='detail'),
     url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$', postpreference, name='postpreference'),
     ]
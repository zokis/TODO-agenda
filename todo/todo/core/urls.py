# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'todo.core.views',

    url(r'^user/list/$', 'user_list', name="user_list"),
    url(r'^user/form/$', 'user_create', name="user_form"),
    url(r'^user/form/(?P<pk>\d+)/$', 'user_update', name="user_form"),
    url(r'^user/delete/(?P<pk>\d+)/$', 'user_delete', name="user_delete"),
)

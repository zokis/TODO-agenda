# coding: utf-8
from django.conf.urls import patterns, url
from .views import CalendarioJsonListView, CalendarioView

urlpatterns = patterns(
    'todo.agenda.views',
    url(
        r'^calendario/json/$',
        CalendarioJsonListView.as_view(),
        name='calendario_json'
    ),
    url(
        r'^$',
        CalendarioView.as_view(),
        name='calendario'
    ),
)

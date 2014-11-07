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
    url(r'^evento_form/$', 'evento_form', name='evento_form'),
    url(r'^evento_form/(?P<pk>\d+)/$', 'evento_form', name='evento_form'),

    url(r'^departamento_list/$', 'departamento_list', name='departamento_list'),
)

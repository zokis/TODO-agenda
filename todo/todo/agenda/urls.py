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
    url(r'^evento/list/$', 'eventos', name='eventos'),
    url(r'^evento/meus/$', 'meus_eventos', name='meus_eventos'),
    url(r'^evento/form/$', 'evento_form', {'publico': False}, name='evento_form'),
    url(r'^evento/form/(?P<pk>\d+)/$', 'evento_form', {'publico': False}, name='evento_form'),
    url(r'^evento/participar/(?P<pk>\d+)/$', 'participar', name='evento_participar'),
    url(r'^evento/publico/form/$', 'evento_form', {'publico': True}, name='evento_publico_form'),
    url(r'^evento/publico/form/(?P<pk>\d+)/$', 'evento_form', {'publico': True}, name='evento_publico_form'),
    url(r'^evento/delete/(?P<pk>\d+)/$', 'evento_delete', name="evento_delete"),

    url(r'^departamento/list/$', 'departamento_list', name="departamento_list"),
    url(r'^departamento/form/$', 'departamento_create', name="departamento_form"),
    url(r'^departamento/form/(?P<pk>\d+)/$', 'departamento_update', name="departamento_form"),
    url(r'^departamento/delete/(?P<pk>\d+)/$', 'departamento_delete', name="departamento_delete"),
)

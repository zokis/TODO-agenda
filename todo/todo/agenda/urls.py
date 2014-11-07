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


    url(r'^list/departamento/$', 'departamento_list', name="departamento_list"),
    url(r'^create/departamento/$', 'departamento_create', name="departamento_form"),
    url(r'^update/departamento/(?P<pk>\d+)/$', 'departamento_update', name="departamento_form"),
    url(r'^delete/departamento/(?P<pk>\d+)/$', 'departamento_delete', name="departamento_delete"),
)

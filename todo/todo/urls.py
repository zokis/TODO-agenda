# coding: utf-8
from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.views import logout, login

from todo.core.forms import AuthenticationForm


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # ADMIN SITE URL 
    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^', include('todo.core.urls')),

    # Logins
    url(r'^logout/$', logout, {"next_page": "/"}, name="logout"),
    url(
        r'^signin/$',
        login,
        {
            'template_name': 'login.html',
            'authentication_form': AuthenticationForm,
        },
        name="login"
    ),

    # password Reset
    url(
        r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"
    ),
    url(
        r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'
    ),
    url(
        r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'}
    ),
    url(
        r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'
    ),

    url(r'^user/activate/(?P<pk>\d+)/$', 'todo.core.views.user_activate', name="activate_user"),
    url(r'^user/deactivate/(?P<pk>\d+)/$', 'todo.core.views.user_deactivate', name="deactivate_user"),
)

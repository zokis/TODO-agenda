# coding: utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.db.models.loading import get_model
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView
from django.views.generic.list import ListView

from .models import User
from .forms import UserCreationForm, UserChangeForm


class SearchFormListView(FormMixin, ListView):
    '''
        Classe de view para colocar um filtro
        na ListView
    '''

    http_method_names = ['get']
    filter_by_user = False

    def get_form_kwargs(self):
        return {'initial': self.get_initial(), 'data': self.request.GET}

    def get_context_data(self, *args, **kwargs):
        context = super(SearchFormListView, self).get_context_data(*args, **kwargs)
        query_string = self.request.GET.copy()
        query_string.pop('page', '1')
        context['query_string'] = query_string.urlencode()
        return context

    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.get_form_class())
        if self.form.is_valid():
            self.object_list = self.form.get_result_queryset()
        else:
            self.object_list = self.get_queryset()

        if self.filter_by_user:
            self.object_list.by_user(self.request.user)

        context = self.get_context_data(
            object_list=self.object_list,
            form=self.form,
            url_params=request.GET.urlencode()
        )

        return self.render_to_response(context)


@login_required
def generic_delete_from_model(request, app_model=None, object_id=None):
    next = request.GET.get('next', 'home')
    app_name, model_name = app_model.split('.', 1)
    if request.user.has_module_perms(app_name) or request.user.is_superuser:
        model = get_model(app_name, model_name)
        obj = get_object_or_404(model, pk=object_id)
        can_delete = True

        if hasattr(obj, 'user_can_delete'):
            if not obj.user_can_delete(request.user):
                messages.success(request, u"Não foi possível deletar")
                can_delete = False

        if can_delete:
            obj.delete()
            messages.success(request, "Deletado com sucesso")

        return redirect(next)
    raise Http404


class ActivateDeactivateView(DeleteView):
    action = None
    ACTIVATE = 'ACTIVATE'
    DEACTIVATE = 'DEACTIVATE'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.action is not None:
            self.object.is_active = self.action == self.ACTIVATE
        self.object.save()
        return HttpResponseRedirect(success_url)


user_activate = permission_required('core.delete_user')(
    ActivateDeactivateView.as_view(
        model=User,
        success_url=reverse_lazy('usuario_list'),
        action='ACTIVATE'
    )
)
user_deactivate = permission_required('core.delete_user')(
    ActivateDeactivateView.as_view(
        model=User,
        success_url=reverse_lazy('usuario_list'),
        action='DEACTIVATE'
    )
)


class UserListView(ListView):
    def get_queryset(self):
        return User.objects.all().exclude(pk=self.request.user.pk)


user_create = user_passes_test(
    lambda u: u.is_superuser)(CreateView.as_view(form_class=UserCreationForm, model=User, success_url=reverse_lazy('user_list')))
user_delete = user_passes_test(
    lambda u: u.is_superuser)(DeleteView.as_view(model=User, template_name='confirm_delete.html', success_url=reverse_lazy('user_list')))
user_list = user_passes_test(
    lambda u: u.is_superuser)(UserListView.as_view(paginate_by=10))
user_update = user_passes_test(
    lambda u: u.is_superuser)(UpdateView.as_view(form_class=UserChangeForm, model=User, success_url=reverse_lazy('user_list')))

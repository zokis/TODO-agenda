# coding: utf-8
import datetime

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from .models import CalendarioEvento, Departamento
from .serializers import evento_serializer
from .utils import timestamp_to_datetime


class CalendarioJsonListView(ListView):

    template_name = 'agenda/calendario_eventos.html'

    def get_queryset(self):
        queryset = CalendarioEvento.objects.filter(publico=True)
        from_date = self.request.GET.get('from', False)
        to_date = self.request.GET.get('to', False)

        if from_date and to_date:
            queryset = queryset.filter(
                inicio__range=(
                    timestamp_to_datetime(from_date) + datetime.timedelta(-30),
                    timestamp_to_datetime(to_date)
                    )
            )
        elif from_date:
            queryset = queryset.filter(
                inicio__gte=timestamp_to_datetime(from_date)
            )
        elif to_date:
            queryset = queryset.filter(
                fim__lte=timestamp_to_datetime(to_date)
            )

        return evento_serializer(queryset)


class CalendarioView(TemplateView):

    template_name = 'agenda/calendario.html'


class SuperuserRequiredMixin(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(SuperuserRequiredMixin, self).dispatch(*args, **kwargs)


DepartamentoForm = modelform_factory(Departamento)


class DepartamentoCreateView(SuperuserRequiredMixin, CreateView):
    class Meta:
        model = Departamento
        success_url = reverse_lazy('departamento_list')
        form_class = DepartamentoForm


class DepartamentoDeleteView(SuperuserRequiredMixin, DeleteView):
    class Meta:
        template_name = 'confirm_delete.html'
        model = Departamento
        success_url = reverse_lazy('departamento_list')


class DepartamentoListView(SuperuserRequiredMixin, ListView):
    class Meta:
        model = Departamento
        paginate_by = 15


class DepartamentoUpdateView(SuperuserRequiredMixin, ListView):
    class Meta:
        model = Departamento
        success_url = reverse_lazy('departamento_list')
        form_class = DepartamentoForm

departamento_create = DepartamentoCreateView.as_view()
departamento_delete = DepartamentoDeleteView.as_view()
departamento_list = ListView.as_view()
departamento_update = UpdateView.as_view()

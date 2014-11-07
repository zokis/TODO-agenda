# coding: utf-8
import datetime

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import CalendarioEvento, Departamento
from .serializers import evento_serializer
from .utils import timestamp_to_datetime
from .forms import EventoForm, DepartamentoForm


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


@login_required
def evento_form(request, pk=None):
    if pk:
        evento = get_object_or_404(CalendarioEvento, pk=pk)
        meu_evento = evento.owner == request.user
    else:
        meu_evento = True
        evento = None
    if not meu_evento:
        form = EventoForm(request.POST or None, instance=evento, user=request.user)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy('evento_form'))

        return render(
            request,
            'agenda/evento_form.html',
            {
                'form': form,
                'evento': evento
            }
        )
    else:
        return render(
            request,
            'agenda/evento.html',
            {
                'evento': evento
            }
        )


departamento_create = user_passes_test(
    lambda u: u.is_superuser)(CreateView.as_view(model=Departamento, success_url=reverse_lazy('departamento_list')))
departamento_delete = user_passes_test(
    lambda u: u.is_superuser)(DeleteView.as_view(model=Departamento, template_name='confirm_delete.html', success_url=reverse_lazy('departamento_list')))
departamento_list = user_passes_test(
    lambda u: u.is_superuser)(ListView.as_view(queryset=Departamento.objects.all(), paginate_by=10))
departamento_update = user_passes_test(
    lambda u: u.is_superuser)(UpdateView.as_view(model=Departamento, success_url=reverse_lazy('departamento_list')))

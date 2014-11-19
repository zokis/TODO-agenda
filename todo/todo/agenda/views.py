# coding: utf-8
import datetime

from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q

from .models import CalendarioEvento, Departamento
from .serializers import evento_serializer
from .utils import timestamp_to_datetime
from .forms import EventoForm, DepartamentoForm, EventoPublicoForm


class CalendarioJsonListView(ListView):

    template_name = 'agenda/calendario_eventos.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            queryset = CalendarioEvento.objects.filter(Q(owner=self.request.user) | Q(participantes=self.request.user))
        else:
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


class EventosList(ListView):
    template_name = 'agenda/evento_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            queryset = CalendarioEvento.objects.filter(participantes=self.request.user)
        else:
            queryset = CalendarioEvento.objects.filter(publico=True)
        return queryset


eventos = EventosList.as_view()


class MeusventosList(ListView):
    template_name = 'agenda/evento_list.html'

    def get_queryset(self):
        queryset = CalendarioEvento.objects.filter(owner=self.request.user)
        return queryset


meus_eventos = login_required(MeusventosList.as_view())


def participar(request, pk):
    evento = get_object_or_404(CalendarioEvento, pk=pk, publico=True)
    evento.participantes.add(request.user)
    return redirect(reverse_lazy('evento_form', kwargs={'pk': pk}))


def evento_form(request, publico=True, pk=None):
    template_name = 'agenda/evento.html'
    participante = False
    if pk:
        if request.user.is_authenticated():
            evento = get_object_or_404(CalendarioEvento, pk=pk)
            meu_evento = evento.owner == request.user
            participante = True
        else:
            evento = get_object_or_404(CalendarioEvento, pk=pk, publico=True)
            meu_evento = False
            participante = evento.participantes.filter(pk=request.pk).count() >= 1
    else:
        meu_evento = True
        evento = None
    context = {'evento': evento, 'publico': publico, 'participante': participante}

    if meu_evento:
        template_name = 'agenda/evento_form.html'
        if publico:
            action_url = 'evento_publico_form'
            form = EventoPublicoForm(request.POST or None, instance=evento, user=request.user)
        else:
            action_url = 'evento_form'
            form = EventoForm(request.POST or None, instance=evento, user=request.user)
        context['action_url'] = action_url
        if request.method == "POST":
            if form.is_valid():
                form.save()
                form.save_m2m()
                return redirect(reverse_lazy('meus_eventos'))
        context['form'] = form
    return render(
        request,
        template_name,
        context
    )


class EventoDeleteView(DeleteView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != request.user:
            raise Http404

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        if self.object.owner != request.user:
            raise Http404
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


evento_delete = user_passes_test(
    lambda u: u.is_superuser)(DeleteView.as_view(model=CalendarioEvento, template_name='confirm_delete.html', success_url=reverse_lazy('meus_eventos')))


departamento_create = user_passes_test(
    lambda u: u.is_superuser)(CreateView.as_view(form_class=DepartamentoForm, model=Departamento, success_url=reverse_lazy('departamento_list')))
departamento_delete = user_passes_test(
    lambda u: u.is_superuser)(DeleteView.as_view(model=Departamento, template_name='confirm_delete.html', success_url=reverse_lazy('departamento_list')))
departamento_list = user_passes_test(
    lambda u: u.is_superuser)(ListView.as_view(queryset=Departamento.objects.all(), paginate_by=10))
departamento_update = user_passes_test(
    lambda u: u.is_superuser)(UpdateView.as_view(form_class=DepartamentoForm, model=Departamento, success_url=reverse_lazy('departamento_list')))

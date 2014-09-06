# coding: utf-8
import datetime

from django.views.generic import ListView, TemplateView

from .models import CalendarioEvento
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

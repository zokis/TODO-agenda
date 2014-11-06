# coding: utf-8

from django import forms

from .models import CalendarioEvento
from todo.core.models import User


class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        user = kw.pop('user')
        super(EventoForm, self).__init__(*args, **kw)
        if not user.is_superuser:
            self.fields['participantes'].queryset = User.objects.filter().exclude(pk=user.pk)

    class Meta:
        model = CalendarioEvento

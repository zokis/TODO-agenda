# coding: utf-8

from django import forms

from .models import CalendarioEvento
from todo.core.models import User
from todo.agenda.models import Departamento


class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        user = kw.pop('user')
        super(EventoForm, self).__init__(*args, **kw)
        self.fields['participantes'].queryset = User.objects.filter().exclude(pk=user.pk)

        if not user.is_superuser:
            self.fields['participantes'].queryset = Departamento.get_funcionarios_by_user_dpt(user)
            if self.instance:
                if self.instance.publico:
                    self.fields['participantes'].queryset = User.objects.filter().exclude(pk=user.pk)

    class Meta:
        model = CalendarioEvento


class DepartamentoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(DepartamentoForm, self).__init__(*args, **kw)
        self.fields['funcionarios'].required = False

    class Meta:
        model = Departamento

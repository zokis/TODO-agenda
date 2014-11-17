# coding: utf-8

from django import forms

from .models import CalendarioEvento
from todo.core.models import User
from todo.agenda.models import Departamento

from bootstrap_toolkit.widgets import BootstrapDateInput


class EventoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        user = kw.pop('user')
        self.user = user
        super(EventoForm, self).__init__(*args, **kw)
        self.fields['participantes'].queryset = User.objects.all().exclude(pk=user.pk)

        if not user.is_superuser:
            self.fields['participantes'].queryset = Departamento.get_funcionarios_by_user_dpt(user)

    def save(self, commit=True):
        instance = super(EventoForm, self).save(commit=False)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = CalendarioEvento
        exclude = ['owner']
        widgets = {'inicio': BootstrapDateInput, 'fim': BootstrapDateInput}


class EventoPublicoForm(EventoForm):
    def __init__(self, *args, **kw):
        super(EventoPublicoForm, self).__init__(*args, **kw)
        self.fields['participantes'].queryset = User.objects.all().exclude(pk=self.user.pk)

    class Meta(EventoForm.Meta):
        pass


class DepartamentoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(DepartamentoForm, self).__init__(*args, **kw)
        self.fields['funcionarios'].required = False

    class Meta:
        model = Departamento

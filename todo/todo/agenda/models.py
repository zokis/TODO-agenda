# coding: utf-8

from django.db import models
from utils import datetime_to_timestamp

from todo.core.models import User


class CalendarioEvento(models.Model):
    TIPOS = (
        ('', 'Normal'),
        ('event-important', 'Importante'),
        ('event-info', 'Informativo'),
        ('event-inverse', 'Pausa'),
        ('event-special', 'Especial'),
        ('event-success', 'Completo'),
        ('event-warning', 'Cancelado'),
    )
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    descricao = models.TextField(default='')
    inicio = models.DateTimeField(verbose_name=u'Início')
    fim = models.DateTimeField(verbose_name='Fim', null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name='owner')
    participantes = models.ManyToManyField(User, related_name='participantes')
    publico = models.BooleanField()

    @property
    def inicio_timestamp(self):
        return datetime_to_timestamp(self.inicio)

    @property
    def fim_timestamp(self):
        return datetime_to_timestamp(self.fim)

    def get_absolute_url(self):
        return '/evento/form/%d/' % self.pk

    def __unicode__(self):
        return self.nome


class Departamento(models.Model):
    nome = models.CharField(max_length=255)
    funcionarios = models.ManyToManyField(User, related_name='funcionarios')

    @classmethod
    def get_funcionarios_by_user_dpt(cls, user):
        dpts = cls.objects.filter(funcionarios__pk=user.pk)
        funs_pk = set()
        for dpt in dpts:
            for fun in dpt.funcionarios.all():
                funs_pk.add(fun.pk)
        return User.objects.filter(pk__in=list(funs_pk)).exclude(pk=user.pk)

    def __unicode__(self):
        return self.nome

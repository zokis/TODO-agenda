# coding: utf-8

from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def calendario(css_classes):
    return render_to_string(
        'agenda/calendario/calendario.html',
        {'css_classes': css_classes}
    )


@register.simple_tag
def controls(css_classes):
    return render_to_string(
        'agenda/calendario/calendario_controls.html',
        {'css_classes': css_classes}
    )


@register.simple_tag
def calendario_js(*args):
    return render_to_string(
        'agenda/calendario/calendario_js.html'
    )


@register.simple_tag
def calendario_css(*args):
    return render_to_string(
        'agenda/calendario/calendario_css.html'
    )


@register.simple_tag
def calendario_init(*args, **kwargs):
    options = {}

    if "events_url" in kwargs:
        options["events_url"] = kwargs["events_url"]
    else:
        options["events_url"] = '/calendario/json/'

    if "view" in kwargs:
        options["view"] = kwargs["view"]
    else:
        options["view"] = 'month'

    if "width" in kwargs:
        options["width"] = kwargs["width"]
    else:
        options["width"] = '100%'

    if "first_day" in kwargs:
        options["first_day"] = kwargs["first_day"]
    else:
        options["first_day"] = 2

    return render_to_string('agenda/calendario/calendario_init.html', options)

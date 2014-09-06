# coding: utf-8
import json


def evento_serializer(eventos):
    result = [
        {
            "id": evento.pk,
            "title": evento.nome,
            "url": evento.get_absolute_url(),
            "class": evento.tipo,
            "start": evento.inicio_timestamp,
            "end": evento.fim_timestamp
        } for evento in eventos]

    objects_head = {"success": 1}
    objects_head["result"] = result
    return json.dumps(objects_head)

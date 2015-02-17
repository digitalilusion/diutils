# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
import decimal
from django.db.models.base import ModelState


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):

        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, ModelState):
            return None
        else:
            try:
                return json.JSONEncoder.default(self, obj)
            except:
                return None


def HttpResponseJSON(d, request=None, status=200):

    return HttpResponse(
        json.dumps(d, cls=CustomEncoder),
        content_type='application/json',
        status=status,
        )


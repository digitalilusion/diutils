# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models.base import ModelState
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.MIMEImage import MIMEImage
import decimal
import json
import base64
from . import tasks


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
    """Dump a JSON dict and return as HttpResponse JSON"""
    return HttpResponse(
        json.dumps(d, cls=CustomEncoder),
        content_type='application/json',
        status=status,
        )


def getIP(request):
    """Get real IP client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sendHtmlMailExp(to, fro, cc, subject, html, txt, att=None, attContent=None,
                    mime=None, headers=None, attPic=None):

    if cc is None:
        aTo = [to]
    else:
        aTo = [to, cc]
    msg = EmailMultiAlternatives(subject, txt, fro, aTo, headers=headers)
    # TODO: add more types
    msg.attach_alternative(html, 'text/html')
    if att:
        if mime is None:
            msg.attach(att, attContent, 'image/png')
        else:
            msg.attach_file(attContent)
    if attPic:
        try:
            mi = MIMEImage(base64.b64decode(attPic))
            msg.attach(mi)
        except Exception, ex:
            pass
    try:
        ret = msg.send()
        print ret
    except Exception, ex:
        return False
    return True


def simpleEmail(to, fro, subject, template, context=None):

    return enqueueTemplateMail(to, fro,
                               subject, template, context)


def enqueueTemplateMail(to, fro, subject, template, ctx=None,
                        cc=None, headers=None, attPic=None, notify=False):
    if ctx is None:
        ctx = {}
    prefix = settings.EMAIL_SUBJECT_PREFIX if hasattr(settings, 'EMAIL_SUBJECT_PREFIX') else ''
    baseext = settings.BASE_EXT if hasattr(settings, 'EMAIL_BASE_EXT') else ''
    ctx['mail_subject'] = u'%s %s' % (prefix, subject)
    ctx['mail_real_subject'] = subject
    ctx['mail_base_url'] = baseext
    ctx['mail_to'] = to
    html = render_to_string(template, ctx)
    return enqueueMail(to, fro, ctx['mail_subject'], html, html,
                       cc, headers, attPic)


def enqueueMail(to, fro, subject, text, html,
                cc=None, headers=None, attPic=None):
    sendDirect = settings.EMAIL_SEND_DIRECT if hasattr(settings, 'EMAIL_SEND_DIRECT') else False
    if sendDirect:
        # Send email now
        sendHtmlMailExp(
            to, fro, cc, subject, html, text, headers=headers, attPic=attPic)
        return True

    tasks.doSendEmail.delay(
        to, fro, cc, subject, html, text, headers=headers, attPic=attPic)
    return True


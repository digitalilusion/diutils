# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import shared_task


@shared_task
def doSendEmail(to, fro, cc, subject, html, txt, att=None, attContent=None,
                mime=None, headers=None, attPic=None):
    from .funcs import sendHtmlMailExp
    sendHtmlMailExp(to, fro, cc, subject, html,
                    txt, att, attContent, mime, headers, attPic)


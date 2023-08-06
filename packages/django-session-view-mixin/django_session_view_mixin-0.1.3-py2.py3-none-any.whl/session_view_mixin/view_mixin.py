# -*- coding: utf-8 -*-
""" Frankhood >  fhcore.views.thumbnail_mixins
    @author: Frankhood Business Solutions
"""
from __future__ import absolute_import, print_function, unicode_literals
import datetime
import logging

from django.utils import timezone

logger = logging.getLogger('fhcore')


class SessionMixin(object):

    def set_in_session(self, session, expires=None, replace=True, **kwargs):
        kwargs = kwargs or {}
        now = timezone.now()
        for k, v in kwargs.items():
            if not replace and k in session:
                old_value = self.get_from_session(session, k)
                if old_value is not None:
                    continue
            if expires:
                expires_datetime = now + datetime.timedelta(seconds=expires)
                data = {'__value': v, 'expires': expires_datetime}
            else:
                data = v
            session[k] = data

    def get_from_session(self, session, key, default=None):
        if key in session:
            now = timezone.now()
            val = session[key]
            if isinstance(val, dict):
                if '__value' in val:
                    expires = val.get('expires', None)
                    if isinstance(expires, int):
                        expires = now
                    if expires:
                        if expires < now:
                            # Item scaduto, lo elimino
                            session.pop(key)
                            return default
                    return val['__value']
                else:
                    return val
            else:
                return val
        return default

    def remove_from_session(self, session, keys=[]):
        if not isinstance(keys, list):
            keys = [keys]
        for k in keys:
            if k in session:
                del session[k]
                try:
                    session.modified = True
                except Exception:
                    pass


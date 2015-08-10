# -*- coding: utf-8 -*-

from notify.gmail.gmail import GMail,GMailWorker,GMailHandler
from notify.gmail.message import Message
from bson import json_util
from collections import OrderedDict
import json

class GGMail(GMail):

    def __init__(self, **kwargs):
        self._cfg = kwargs.pop('cfg', {})
        self._debug = kwargs.pop('debug', False)
        self._stockids = kwargs.pop('stockids', [])
        self._starttime = kwargs.pop('starttime', None)
        self._endtime = kwargs.pop('endtime', None)
        self._account = self._cfg.pop('GMAIL_ACCOUNT', None)
        self._passwd = self._cfg.pop('GMAIL_PASSWD', None)
        self._to = self._cfg.pop('GMAIL_RCPT', [])
        self._subject = self._cfg.pop('subject', 'best list ...')
        super(GGMail, self).__init__(self._account, self._passwd)

    def create_msg(self):
        subject = self._subject
        to = ";".join(self._to)
        payload = {
            'starttime': self._starttime.strftime("%Y-%m-%d"),
            'endtime': self._endtime.strftime("%Y-%m-%d"),
            'list': self._stockids[:10]
        }
        text = json.dumps(OrderedDict(payload), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=True)
        msg = Message(subject, to=to, text=text)
        return msg

    def send(self, msg):
        super(GGMail, self).send(msg)

# -*- coding: utf-8 -*-

from noify import GMail,GMailWorker,GMailHandler
from message import Message
from bson import json_util
import json

class GGmail(Gmail):

    def __init__(self, **kwargs):
        self._cfg = kwargs.pop('cfg', {})
        self._debug = kwargs.pop('debug', False)
        self._account = self._cfg.pop('GIANT_ACCOUNT', None)
        self._passwd = self._cfg.pop('GMAIL_PASSWD', None)
        self._to = self._cfg.pop('GMAIL_RCPT', [])
        self._stockids = self.pop('stockids', [])
        self._starttime = kwargs.pop('starttime', None)
        self._endtime = kwargs.pop('endtime', None)
        super(GGmail, self).__init__(self._account, self._passwd)

    def create_msg(self):
        subject = "best list"
        to = self._to
        payload = {
            'starttime': self._starttime.strftime("%Y-%m-%d"),
            'endtime': self._endtime.strftime("%Y-%m-%d"), 
            'graph': '',
            'list': self._stockids[:10]
        }
        text = json.dumps(dict(payload), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        msg = Message(subject, to=to, text=text)
        return msg

    def send(self, msg):
        self.send(msg)
# -*- coding: utf-8 -*-

from gmail import GMail,GMailWorker,GMailHandler
from message import Message

class GGmail(Gmail):

    def __init__(self, graph, **kwargs):
        self._cfg = kwargs.pop('cfg', {})
        self._debug = kwargs.pop('debug', False)
        self._account = self._cfg.pop('GIANT_ACCOUNT', None)
        self._passwd = self._cfg.pop('GMAIL_PASSWD', None)
        self._to = self._cfg.pop('GMAIL_RCPT', [])
        self._stockids = self.pop('stockids', [])
        self._graph = graph

    def create_payload(self):
        subject = " watch list"
        to = self._to
        payload = {
            'starttime': None,
            'endtime': None,   
            'list': self._stockids[:10]
        }
        #msg = Message(subject, to=to, text=payload)
        #return msg

    def send(self, msg):
        self.send(msg)
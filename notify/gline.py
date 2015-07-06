# -*- coding: utf-8 -*-

from notify.line.client import LineClient, LineGroup, LineContact
from bson import json_util
from collections import OrderedDict
import json

class GLine(LineClient):
    
    def __init__(self, **kwargs):
        self._cfg = kwargs.pop('cfg', {})
        self._debug = kwargs.pop('debug', False)
        self._stockids = kwargs.pop('stockids', [])
        self._starttime = kwargs.pop('starttime', None)
        self._endtime = kwargs.pop('endtime', None)
        self._account = self._cfg.pop('LINE_ACCOUNT', None)
        self._passwd = self._cfg.pop('LINE_PASSWD', None)
        self._to = self._cfg.pop('LINE_GROUP', [])
        super(GLine, self).__init__(self._account, self._passwd)

    def create_msg(self):
        payload = {
            'subject': "best list ...",
            'starttime': self._starttime.strftime("%Y-%m-%d"),
            'endtime': self._endtime.strftime("%Y-%m-%d"),
            'graph': '',
            'list': self._stockids[:10]
        }
        msg = json.dumps(OrderedDict(payload), sort_keys=True, indent=4, default=json_util.default, ensure_ascii=False)
        return msg

    def send(self, msg):
        for to in self._to:
            group = self.getGroupByName(to)
            if group:
                group.sendMessage(msg)

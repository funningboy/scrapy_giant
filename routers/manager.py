# -*- coding: utf-8 -*-

import yaml
import copy
from datetime import datetime, timedelta
from handler.tasks import collect_hisitem

def parse_task(path, kwargs={}):
	with open(path) as stream:
		stream = yaml.load(stream)
		if 'kwargs' in stream:
			stream['kwargs'].update(kwargs)
			if 'starttime' in stream['kwargs']:
				# try
				stream['kwargs']['starttime'] = eval(stream['kwargs']['starttime'])
			if 'endtime' in stream['kwargs']:
				stream['kwargs']['endtime'] = eval(stream['kwargs']['endtime'])
			stream['kwargs'].update({'debug': True})
		if 'task' in stream:
			pass
		if 'description' in stream:
			pass
		return stream

with open("./routers/table/StockProfileUp0.yaml", 'r') as stream:
	stream = yaml.load(stream)
	if 'Nodes' in stream:
		if isinstance(stream['Nodes'], list):
			for node in stream['Nodes']:
				node = eval(node)
				task = eval(node['task'])
				print task.delay(**node['kwargs']).get()
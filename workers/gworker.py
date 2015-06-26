
from workers.worker import DAGWorker

class GiantWorker(DAGWorker):

	def __init__(self, **kwargs):
		super(GiantWorker, self).__init__()

  	def _collect_incoming_kwargs(self, node):
  		pass
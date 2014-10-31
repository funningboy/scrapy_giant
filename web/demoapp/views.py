from django.http import HttpResponse
from django.views.generic import View
from datetime import datetime, timedelta

from demoapp.tasks import *

class MyView(View):

    def get(self, request, *args, **kwargs):
        #run_scrapy.delay(True).get()
        #rst = run_algorithm.delay(datetime.utcnow() - timedelta(days=60), datetime.utcnow(), ['2317'], True).get()
        rst = add(1, 2)
        return HttpResponse(rst)

# -*- coding: utf-8 -*-

from django.conf import settings
from main.forms import FormSearchItem, FormPortfolioItem

def current_url(request):
    return {'current_url': settings.SITE_DOMAIN + request.path}

def searchform(request):
	return {'searchform': FormSearchItem() }

def portfolioform(request):
	return {'portfolioform': FormPortfolioItem() }
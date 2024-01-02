from django.shortcuts import render
import requests as rq
from django.conf import settings
from django.http import HttpResponseRedirect


def newsapi(params: dict):
    apikey = settings.API_KEY
    url = 'https://newsapi.org/v2/top-headlines'
    if 'apiKey' not in params:
        params['apiKey'] = apikey

    response = rq.get(url=url, params=params)
    return response.json()


def home(request):
    params = {'country': 'in', 'pageSize': 20, 'page': 1}
    if 'category' in request.GET:
        params['category'] = request.GET['category']
    response = newsapi(params)
    context = {'articles': response['articles']}
    return render(request, 'home.html', context=context)
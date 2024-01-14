from django.shortcuts import render, reverse
import requests as request_module
from django.conf import settings
from django.http import HttpResponseRedirect
from home.models import Subscriber
from django.contrib import messages


def trending_api(params):
    apikey = settings.API_KEY
    url = f'https://newsapi.org/v2/top-headlines?apiKey={apikey}'
    response = request_module.get(url=url, params=params)
    return response.json()


def everything_api(params, keyword):
    apikey = settings.API_KEY
    url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={apikey}'
    response = request_module.get(url, params=params)
    return response.json()


def home(request):
    page = request.GET.get('page', default=1)
    category=request.GET.get('category', default='general')
    params_dict = {'country': 'in',
                   'category': category,
                   'page': page}

    news_response = trending_api(params_dict)

    context = {'articles': news_response['articles'],
               'previous': int(page)-1,
               'current': page,
               'next': int(page)+1,
               'url': f'{request.path}?category={category}&'}

    return render(request, 'home.html', context=context)


def about_us(request):
    return render(request, 'about_us.html')


def subscribe(request):
    try:
        email = request.POST.get('email')
        Subscriber.objects.create(email=email)
    except Exception as e:
        messages.error(request, 'Error occurred! Try again with a different email.')
    else:
        messages.success(request, 'Congrats, You successfully became a subscriber.')
    finally:
        return HttpResponseRedirect(redirect_to=reverse('home-page'))


def search(request):
    page = request.GET.get('page', default=1)
    keyword_ = request.GET.get('search')
    params_dict = {'page': page, 'pageSize': 10}
    news_response = everything_api(params_dict, keyword=keyword_)
    context = {'articles': news_response['articles'],
               'url': f'{request.path}?search={keyword_}&',
               'previous': int(page)-1,
               'current': page,
               'next': int(page)+1}
    return render(request, 'home.html', context=context)
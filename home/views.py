from django.shortcuts import render, reverse
import requests as request_module
from django.conf import settings
from django.http import HttpResponseRedirect
from home.models import Subscriber
from django.contrib import messages


Previous = 0
Next = 2

def newsapi(params, q=None):
    apikey = settings.API_KEY
    if q is None:
        url = f'https://newsapi.org/v2/top-headlines?apiKey={apikey}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?q={q}&apiKey={apikey}'
    response = request_module.get(url=url, params=params)
    return response.json()


def everything(params, keyword):
    apikey = settings.API_KEY
    url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={apikey}'
    response = request_module.get(url, params=params)
    return response.json()


def home(request):
    global Next, Previous
    if 'next' in request.GET:
        Next += 1
        Previous += 1
        current = int(request.GET.get('next')) - 1
    elif 'previous' in request.GET:
        Next -= 1
        Previous -= 1
        current = int(request.GET.get('previous')) + 1
    else:
        current = 1

    category = request.GET.get('category', default='general')

    params_dict = {'country': 'in', 'pageSize': 10, 'page': current, 'category': category}
    news_response = newsapi(params_dict)

    context = {'articles': news_response['articles'], 'previous': Previous, 'next': Next, 'current': current}
    return render(request, 'home.html', context=context)


def about_us(request):
    return render(request, 'about_us.html')


def subscribe(request):
    try:
        email = request.POST.get('email')
        Subscriber.objects.create(email=email)
    except Exception as e:
        messages.error(request, 'Error occurred!')
    else:
        messages.success(request, 'Congrats, You successfully became a subscriber.')
    finally:
        return HttpResponseRedirect(redirect_to=reverse('home-page'))


def search(request):
    keyword_ = request.POST.get('search')
    params_dict = {'pageSize': 20, 'page': 1}
    news_response = everything(params_dict, keyword=keyword_)
    # print(news_response)
    context = {'articles': news_response['articles']}
    return render(request, 'home.html', context=context)

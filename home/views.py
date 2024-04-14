from django.shortcuts import render, reverse
import requests as rm
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from home.models import Subscriber
from django.contrib import messages


def trending_api(params):
    params['apiKey'] = settings.API_KEY
    url = 'https://newsapi.org/v2/top-headlines'
    response = rm.get(url=url, params=params)
    return response.json()


def everything_api(params):
    params['apiKey'] = settings.API_KEY
    url = 'https://newsapi.org/v2/everything'
    response = rm.get(url, params=params)
    return response.json()


def extras(resp, page_no, page_size=20):
    if resp['status'] == 'error':
        return HttpResponseBadRequest("Error, Bad Request!")

    if len(resp['articles']) == 0:
        return HttpResponse("No Results Found!")

    if int(page_no) == 1:
        __start = 1
    else:
        __start = page_size * (int(page_no) - 1) + 1

    if int(resp['totalResults']) < page_size * int(page_no):
        __end = int(resp['totalResults'])
    else:
        __end = page_size * int(page_no)

    if __end == int(resp['totalResults']):
        __next_page_disabled = True
    else:
        __next_page_disabled = False

    return __next_page_disabled, __start, __end


def home(request):
    page = request.GET.get('page', default=1)
    category = request.GET.get('category', default='general')

    params_dict = {'country': 'in',
                   'category': category,
                   'page': page}

    news_response = trending_api(params_dict)

    result = extras(news_response, page)
    if isinstance(result, HttpResponse):
        return result
    next_page_disabled, start, end = result

    context = {
        'total_results': news_response['totalResults'],
        'page_start': start,
        'page_end': end,
        'articles': news_response['articles'],
        'previous': int(page)-1,
        'current': page,
        'next': int(page)+1,
        'next_page_disabled': next_page_disabled,
        'url': f'{request.path}?category={category}&'}

    return render(request, 'home.html', context=context)


def about_us(request):
    return render(request, 'about_us.html')


def subscribe(request):
    try:
        email = request.POST.get('email')
        Subscriber.objects.create(email=email)
    except Exception:
        messages.error(request, 'Error occurred! Try again with a different email.')
    else:
        messages.success(request, 'Congrats, You successfully became a subscriber.')
    finally:
        return HttpResponseRedirect(redirect_to=reverse('home-page'))


def search(request):
    page = request.GET.get('page', default=1)
    keyword_ = request.GET.get('search')
    params_dict = {'page': page,
                   'pageSize': 20,
                   'q': keyword_}

    news_response = everything_api(params_dict)

    result = extras(news_response, page)
    if isinstance(result, HttpResponse):
        return result

    next_page_disabled, start, end = result

    context = {'total_results': news_response['totalResults'],
               'page_start': start,
               'page_end': end,
               'page_results': len(news_response['articles']),
               'articles': news_response['articles'],
               'url': f'{request.path}?search={keyword_}&',
               'previous': int(page)-1,
               'current': page,
               'next': int(page)+1,
               'next_page_disabled': next_page_disabled}

    return render(request, 'home.html', context=context)
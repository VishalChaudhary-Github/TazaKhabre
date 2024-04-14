from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home-page'),
    path('about-us/', views.about_us, name='about-us'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('search/', views.search, name='search-news')
]
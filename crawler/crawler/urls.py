from django.urls import path

from crawler import views

urlpatterns = [
    path('', views.crawl_urls, name='crawler')
]

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
	path('', views.posts, name='posts'),
	path('buckets', views.buckets, name='buckets'),
	path('recommend', views.recommend, name='recommend'),
	path('account', views.account, name='account')
]
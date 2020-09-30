from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
	path('posts', views.posts, name='posts'),
	path('posts/<str:posts_to_show>', views.posts, name='posts'),
	path('buckets', views.buckets, name='buckets'),
	path('recommend', views.recommend, name='recommend'),
	path('account', views.account, name='account')
]
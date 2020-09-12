from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import reverse

# Create your views here.


def Home(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('base_note/')
	else:
		return render(request, 'home.html')














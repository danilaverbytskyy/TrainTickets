from http.client import HTTPResponse

from django.shortcuts import render


def home(request):
    return render(request, 'schedule/home.html')


def about(request):
    return render(request, 'schedule/about.html')


def contact(request):
    return render(request, 'schedule/contact.html')
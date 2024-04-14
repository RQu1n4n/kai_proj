from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

# View for the home Page

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def contact(request):
    return render(request, 'kaizen/contact.html', {'title': 'Contact'})
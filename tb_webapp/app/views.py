from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'app/index.html')

def register(request):
    pass

def login(request):
    pass

def logout(request):
    pass
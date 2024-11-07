from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Blog Home</h1>')

def register(request):
    pass

def login(request):
    pass

def logout(request):
    pass
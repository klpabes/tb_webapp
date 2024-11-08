from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm

def index(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
            
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

def login(request):
    pass

def logout(request):
    pass
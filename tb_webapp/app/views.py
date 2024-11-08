from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('index')
            
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, f'You are now logged out!')
    return redirect('login')
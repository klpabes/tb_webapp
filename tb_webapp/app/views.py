from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm, MLForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import pandas as pd

import joblib
from . import ml_models

from app.ml_models.lstm import result

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
    return render(request, 'app/register.html', {'form': form, 'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, f'You are now logged out!')
    return redirect('login')

@login_required
def arima_view(request):
    # put arima in model
    if request.method == "POST":
        form = MLForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            ml_model = joblib.load('app/ml_models/arima_model.joblib')
            pred = mod.predict(start=f"{year}-01-01", end=f"{year}-12-01", typ='levels')
            # date = form.cleaned_data['year'].strftime("%Y-%m-%d")
            # ml_model = joblib.load('app/ml_models/arima_model.joblib')
            # pred = ml_model.predict(date)
            # return render(request, 'app/arima.html', {'form': form, 'pred': round(pred[date], 2), 'successful_submit': True})
            return render(request, 'app/arima.html', {'form': form, 'year': year})
    else:
        form = MLForm()
    return render(request, 'app/arima.html', {'form': form})

@login_required
def expo_view(request):
    if request.method == "POST":
        form = MLForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date'].strftime("%Y-%m-%d")
            ml_model = joblib.load('app/ml_models/expo_model.joblib')
            pred = ml_model.predict(date)
            return render(request, 'app/expo.html', {'form': form, 'pred': round(pred[date], 2), 'successful_submit': True})
            
    else:
        form = MLForm()
    return render(request, 'app/expo.html', {'form': form})

@login_required
def lstm_view(request):
    if request.method == "POST":
        form = MLForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date'].strftime("%Y-%m-%d")    
            pred = result.loc[date].DIAGNOSED
            return render(request, 'app/lstm.html', {'form': form, 'pred': round(pred, 2), 'successful_submit': True})
            
    else:
        form = MLForm()
    return render(request, 'app/lstm.html', {'form': form})
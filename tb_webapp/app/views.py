from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm, MLForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from .utils import get_graph

import joblib
from . import ml_models

from app.ml_models.lstm import result

df = pd.read_csv('app/ml_models/diagnosed_final.csv', parse_dates=['DATE'], index_col='DATE')
df['DATE'] = df.index

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
            pred = np.round(ml_model.predict(start=f"{year}-01-01", end=f"{year}-12-01"), 2)
            filtered = df[df['DATE'].dt.year == int(year)]['DIAGNOSED']
            pred = pd.DataFrame({'DATE':pred.index, 'PREDICTED':pred.values}, index=pred.index)
            pred['MONTH'] = pred['DATE'].dt.month_name()
            df_final = pd.concat([pred['MONTH'], filtered, pred['PREDICTED']], axis=1)
            df_final = df_final.rename(columns={'DIAGNOSED': 'ACTUAL'})
            graphic = get_graph(df_final, year)
            return render(request, 'app/arima.html', {'form': form, 'df':df_final, 'graphic': graphic})
    else:
        form = MLForm()
    return render(request, 'app/arima.html', {'form': form})

@login_required
def expo_view(request):
    if request.method == "POST":
        form = MLForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            ml_model = joblib.load('app/ml_models/expo_model.joblib')
            pred = np.round(ml_model.predict(start=f"{year}-01-01", end=f"{year}-12-01"), 2)
            filtered = df[df['DATE'].dt.year == int(year)]['DIAGNOSED']
            pred = pd.DataFrame({'DATE':pred.index, 'PREDICTED':pred.values}, index=pred.index)
            pred['MONTH'] = pred['DATE'].dt.month_name()
            df_final = pd.concat([pred['MONTH'], filtered, pred['PREDICTED']], axis=1)
            df_final = df_final.rename(columns={'DIAGNOSED': 'ACTUAL'})
            graphic = get_graph(df_final, year)
            return render(request, 'app/expo.html', {'form': form, 'df':df_final, 'graphic': graphic})
            
    else:
        form = MLForm()
    return render(request, 'app/expo.html', {'form': form})

@login_required
def lstm_view(request):
    if request.method == "POST":
        form = MLForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year'] 
            pred = result[result['DATE'].dt.strftime('%Y') == year]
            filtered = df[df['DATE'].dt.year == int(year)]['DIAGNOSED']
            pred = pd.DataFrame({'DATE':pred['DATE'], 'PREDICTED':pred['DIAGNOSED']}, index=pred['DATE'])
            pred['MONTH'] = pred['DATE'].dt.month_name()
            df_final = pd.concat([pred['MONTH'], filtered, pred['PREDICTED']], axis=1)
            df_final = df_final.rename(columns={'DIAGNOSED': 'ACTUAL'})
            graphic = get_graph(df_final, year)
            return render(request, 'app/lstm.html', {'form': form, 'df':df_final, 'graphic': graphic})
            
    else:
        form = MLForm()
    return render(request, 'app/lstm.html', {'form': form})
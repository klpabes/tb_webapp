from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('arima/', views.arima_view, name='arima'),
    path('expo/', views.expo_view, name='expo'),
    path('lstm/', views.lstm_view, name='lstm'),
]

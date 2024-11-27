from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    #path('', indexPage,name='list'),  
    path('', views.indexPage,name='inicio'),
    path('accounts/login/', LoginView.as_view(template_name='home/login.html'), name="login"),
    path('login/', LogoutView.as_view(), name="logout"),
    path('cargarData/', views.cargaDataModels, name="cargarData")
    
]
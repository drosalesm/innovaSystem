from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sucursales_all/',views.lisSucListView.as_view(), name='sucursales_all'),
    path('crear_sucursal/',views.sucursalesCreateView.as_view(), name='crear_sucursal'),
    path('act_sucursal/<int:pk>', views.sucursalUpdateView.as_view(),name='act_sucursal'),
    path('borr_sucursal/<int:pk>', views.sucurDeleteView.as_view(),name='borr_sucursal'),
]
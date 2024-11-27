from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('vendedores/', views.vendedoresInicio,name='vendedores'),
    path('list_vend/', views.lisVendListView.as_view(),name='list_vend'),
    path('crear_vend/',views.vendCreateView.as_view(), name='crear_vend'),
    path('act_vendedor/<int:pk>', views.vendUpdateView.as_view(),name='act_vendedor'),
    path('borr_vend/<int:pk>', views.vendDeleteView.as_view(),name='borr_vend'),
]
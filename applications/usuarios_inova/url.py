from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('usuarios_list/',views.lisUsersView.as_view(), name='usuarios_list'),
    path('crear_usuario/',views.registroUser.as_view(), name='crear_usuario'),
    path('actu_usuario/<int:pk>', views.actualizarUser.as_view(),name='actu_usuario'),
    path('borr_usuario/<int:pk>', views.usersDeleteView.as_view(),name='borr_usuario'),
]
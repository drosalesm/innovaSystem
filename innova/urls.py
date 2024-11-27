
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    #incluimos las URLS de las apps
    re_path('',include('applications.pacientes.url')),
    re_path('',include('applications.home.url')),
    re_path('',include('applications.ordenes.url')),
    re_path('',include('applications.sucursales.url')),
    re_path('',include('applications.facturacion.url')),
    re_path('',include('applications.vendedores.url')),
    re_path('',include('applications.examenes.url')),
    re_path('',include('applications.usuarios_inova.url')),
]

urlpatterns+=staticfiles_urlpatterns()
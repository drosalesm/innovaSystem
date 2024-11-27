from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('Pacientes/',views.lisPacInfListView.as_view(), name='pacientes_opc'),
    path('lisPacOpcListView/',views.lisPacOpcListView.as_view(), name='pacientes_list'),
    path('pacCreateView/',views.pacCreateView.as_view(), name='crear_pacientes'),
    path('pacUpdateView/<int:pk>', views.pacUpdateView.as_view(),name='act_pacientes'),
    path('pacDeleteView/<int:pk>', views.pacDeleteView.as_view(),name='borr_pacientes'),
#    path('lisPacOpcListView/',views.listPacientes, name='pacientes_list'),    
    path('web_cam/',views.openCamera, name='web_cam'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
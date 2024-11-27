from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [   
    #urls del examen medico
    path('ex_med_list/',views.lisExamenMedListView.as_view(), name='ex_med_list'),
    path('ex_med_creat/<int:pk>',views.creExamenMedCreateView.as_view(), name='ex_med_creat'),
    path('ex_med_borr/<int:pk>', views.delExmMedDeleteView.as_view(),name='ex_med_borr'),
    path('ex_med_upd/<int:pk>', views.updExamenMedUpdateView.as_view(),name='ex_med_upd'),
    path('ex_med_pdf/<int:pk>', views.exMedPdf.as_view(),name='ex_med_pdf'),
    #urls del examen psicologico
    path('ex_psi_list/',views.lisExamenPsiListView.as_view(), name='ex_psi_list'),
    path('ex_psi_creat/<int:pk>',views.creExamenPsiCreateView.as_view(), name='ex_psi_creat'),
    path('ex_psi_borr/<int:pk>', views.delExmPsiDeleteView.as_view(),name='ex_psi_borr'),
    path('ex_psi_upd/<int:pk>', views.updExamenPsiUpdateView.as_view(),name='ex_psi_upd'),
    path('ex_psi_pdf/<int:pk>', views.exPsiPdf.as_view(),name='ex_psi_pdf'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
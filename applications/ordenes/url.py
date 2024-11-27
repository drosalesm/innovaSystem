from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ordenes_all/',views.lisExcListView.as_view(), name='ordenes_all'),
    path('examenes_opc/',views.lisExcInfListView.as_view(), name='examenes_opc'),
    path('crear_examenes/',views.ordCreateView.as_view(), name='crear_examenes'),
    path('act_ordenes/<int:pk>', views.ordUpdateView.as_view(),name='act_ordenes'),
    path('borr_ordenes/<int:pk>', views.ordDeleteView.as_view(),name='borr_ordenes'),
    path('crear_fact/', views.crearFacturas,name='crear_fact'),
    path('opt_ord/', views.ordatendOp,name='opt_ord'),
    path('att_ord_all/',views.l_ordatendOpListView.as_view(), name='att_ord_all'),
    path('ord_reportes/',views.ordreportes, name='ord_reportes'),
    path('list_fact/',views.listar_facturasListView.as_view(),name='list_fact'),
    #urls de los examenes
    path('att_ord_med/<int:pk>', views.ate_ordenMedica,name='att_ord_med'),
    path('att_ord_psi/<int:pk>', views.ate_ordenPsi,name='att_ord_psi'),
    path('att_ord_vis/<int:pk>', views.ate_ordenVisual,name='att_ord_vis'),
    #----------------
    path('psi_preg/',views.lispregPsiListView.as_view(), name='psi_preg'),
    path('crear_preg_psi/',views.pregPsicoCreateView.as_view(), name='crear_preg_psi'),
    path('act_preg_psi/<int:pk>', views.pregPsicoAcUpdateView.as_view(),name='act_preg_psi'),
    path('borr_preg_psi/<int:pk>', views.pregPsicoBorDeleteView.as_view(),name='borr_preg_psi'),
    path('fin_or/<int:pk>', views.cierre_man_orden,name='fin_or'),
    path('fin_man/<int:pk>', views.fin_man_orden,name='fin_man'),
    path('exm_resultados/', views.ExamResultados,name='exm_resultados'),
    path('recibo_aut/',views.imprimirFactura, name='recibo_aut'),
    #-------------
    path('list_adelantos/',views.listar_adelantosListView.as_view(),name='list_adelantos'),
    path('crear_adelanto/',views.adelantoCreateView.as_view(),name='crear_adelanto'),
    path('borr_adelanto/<int:pk>',views.adelantoDeleteView.as_view(),name='borr_adelanto'),
    path('act_adel/<int:pk>',views.adelUpdateView.as_view(),name='act_adel'),
    #-------------
    path('list_prov/',views.listar_provListView.as_view(),name='list_prov'),
    path('crear_prov/',views.proovCreateView.as_view(),name='crear_prov'),
    path('borr_prov/<int:pk>',views.proovDeleteView.as_view(),name='borr_prov'),
    path('act_prov/<int:pk>',views.provUpdateView.as_view(),name='act_prov'),



 ]

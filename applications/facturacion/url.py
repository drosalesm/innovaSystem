from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('info_fac/',views.lisDetailFacturacion.as_view(), name='info_fac'),
    path('list_fac/',views.listFacturasListView.as_view(), name='list_fac'),
    path('cre_tal_fac/',views.DetFactCreateView.as_view(), name='cre_tal_fac'),
    path('up_fac/<int:pk>', views.infFacturasUpdateView.as_view(),name='up_fac'),
    path('factInfo/', views.factOpciones,name='factInfo'),
    path('del_fac/<int:pk>', views.listFactDeleteView.as_view(),name='del_fac'),
    path('del_fac_info/<int:pk>', views.delInfoFactGen.as_view(),name='del_fac_info'),
    #--Inventario de productos-----------------------------------
    path('list_inv_p/',views.listInvProd.as_view(), name='list_inv_p'),
    path('cre_inv_prod/',views.invtProdCreateView.as_view(), name='cre_inv_prod'),
    path('up_inv_p/<int:pk>', views.invProdUpdateView.as_view(),name='up_inv_p'),
    path('del_inv_prod/<int:pk>', views.delInvProd.as_view(),name='del_inv_prod'),
#reporteria
    path('rep_fact/',views.Rep_Fact_vend, name='rep_fact'),
    path('rep_fact_pdf/',views.Rep_Fact_pdf, name='rep_fact_pdf'),
    path('rep_fact_p/',views.Rep_Fact_prod, name='rep_fact_p'),
    path('recibo/<int:pk>',views.reciboPdf.as_view(), name='recibo'),
    path('obt_cli/',views.getClientes,name='obt_cli'),
    path('rep_cierr/',views.rep_cierre_diario,name='rep_cierr'),
# Arqueo de caja--------------------------------------------
    path('list_caja/',views.listarqcaja.as_view(), name='list_caja'),
    path('crea_arqueo/',views.arqCajaCreateView.as_view(), name='crea_arqueo'),
    path('up_arqueo/<int:pk>', views.arqCajaUpdateView.as_view(),name='up_arqueo'),
    path('del_arqueo/<int:pk>', views.delarqCaja.as_view(),name='del_arqueo'),

]
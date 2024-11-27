import os
from weasyprint import CSS, HTML
from datetime import datetime
from weasyprint import CSS, HTML
from getpass import getuser
from multiprocessing import Array
from django.conf import settings
from urllib.request import Request
from wsgiref import validate
from django import views
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from requests import request
from django.db.models.query import QuerySet
from applications.facturacion.views import reciboPdf
from django.views import View
from applications.pacientes.models import Pacientes
from applications.sucursales.models import sucursales
from applications.facturacion.models import *
from applications.usuarios_inova.views import *
from applications.facturacion.forms import form_bus

from applications.vendedores.models import vendedores
from .models import *
from django.core.paginator import Paginator
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models.functions import Replace
from django.utils.datastructures import MultiValueDictKeyError
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import connection
from django.conf import settings
from django.template.loader import get_template
from datetime import date, datetime,timedelta
from reportlab.pdfgen import canvas
from io import BytesIO

today = date.today()


# Vista de opciones generales del modulo ordenes
@method_decorator(login_required, name='dispatch')
class lisExcInfListView(ListView):
    model = exaOpciones

# Vista para enlistar los ordenes

@method_decorator(login_required, name='dispatch')
class lisExcListView(ListView):
    paginate_by = 7
    model = ordenes


# Vista para crear ordenes
@method_decorator(login_required, name='dispatch')
class ordCreateView(CreateView):
    form_class = examenesForm
    model = ordenes
    success_url = '/ordenes_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context

# Vista para actualizar ordenes

@method_decorator(login_required, name='dispatch')
class ordUpdateView(UpdateView):
    form_class = examenesForm
    model = ordenes
    success_url = '/ordenes_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

# Vista para eliminar ordenes

@method_decorator(login_required, name='dispatch')
class ordDeleteView(DeleteView):
    model = ordenes
    success_url = '/ordenes_all'


#Orden Medica
def ate_ordenMedica(request,pk):
    name_orden=ordenes_emitidas.objects.filter(id=pk).values_list('nombre_orden',flat=True)[0]
    paciente=ordenes_emitidas.objects.filter(id=pk).values_list('paciente',flat=True)[0]
    cod_orden=ordenes_emitidas.objects.filter(id=pk).values_list('cod_ord',flat=True)[0]
    return render(request, 'ordenes/form_med.html',{"name_orden":name_orden,"paciente":paciente,"cod_orden":cod_orden})


#Orden Psicologica
def ate_ordenPsi(request,pk):
    name_orden=ordenes_emitidas.objects.filter(id=pk).values_list('nombre_orden',flat=True)[0]
    paciente=ordenes_emitidas.objects.filter(id=pk).values_list('paciente',flat=True)[0]
    cod_orden=ordenes_emitidas.objects.filter(id=pk).values_list('cod_ord',flat=True)[0]
    psi = examen_psi.objects.all()
    return render(request, 'ordenes/form_psi.html',{"name_orden":name_orden,"paciente":paciente,"cod_orden":cod_orden,"psi":psi})
    
def ate_ordenVisual(request,pk):
    name_orden=ordenes_emitidas.objects.filter(id=pk).values_list('nombre_orden',flat=True)[0]
    paciente=ordenes_emitidas.objects.filter(id=pk).values_list('paciente',flat=True)[0]
    cod_orden=ordenes_emitidas.objects.filter(id=pk).values_list('cod_ord',flat=True)[0]
    return render(request, 'ordenes/form_visual.html',{"name_orden":name_orden,"paciente":paciente,"cod_orden":cod_orden})
    



# -----------------FACTURACION
@login_required
@method_decorator(csrf_exempt)
def crearFacturas(request):
    form_fac = facturaForm(request.POST)
    form_cli = listado_clientes(request.POST)
    form_ord = listado_ordenes(request.POST)
    form_vend=vend_form(request.POST)
    tipo_pago=tpForm(request.POST)
    ult_cli =Pacientes.objects.last()
    form_fecha=form_bus()

    try:

        data_inv=[]
        for inv in inventProd.objects.filter(cantidad_inv__lte=25).all():
            data_inv.append(inv.producto)        

        inv_fuera = json.dumps(data_inv)

        ult_fact=encabezadoFactura.objects.values_list('factura',flat=True).last();

        isv = info_facturas.objects.values_list('isv').distinct()
        isv = str(isv[0]).replace(",", "").replace("(", "").replace(")", "")





        factura = info_facturas.objects.values_list('numeracion').distinct()
        factura = str(factura[0]).replace(",", "").replace(
            "(", "").replace(")", "").replace("'", "")

        usuario=str(request.user)

        user_suc=listUsuarios()
        suc=""



        for us_suc in user_suc:
            data=str(us_suc).replace("'","").replace(")","").replace("(","")
            usuario_model=((data[int(data.find(',')+1):100]).replace(" ","")).replace(" ","")

            if usuario_model==usuario:
                suc=(data[0:int(data.find(','))])





        numero = info_facturas.objects.filter(sucursal=suc).values_list('fac_actual').distinct()


        print('Viendo si llegue aqui...',numero,suc)

        numero = str(numero[0]).replace(",", "").replace("(", "").replace(")", "")




        rango_final = info_facturas.objects.filter(sucursal=suc).values_list('rango_final').distinct()
        rango_final = str(rango_final[0]).replace(",", "").replace("(", "").replace(")", "")

        excede=''
        if int(rango_final) < int(numero):
            excede='Si'
        else:
            excede='No'

        print(int(rango_final),int(numero))




        ubicacionsuc=sucursales.objects.filter(nombre_sucursal=suc).values_list('direccion',flat=True)[0]
        cai=info_facturas.objects.filter(sucursal=suc).values_list('cai',flat=True)[0]

        dir_cli=suc+','+ubicacionsuc




        #Calculando valor correcto para la factura
        if len(numero) < 8:
            digitos=8-len(numero)
        print(digitos)
        for x in range(digitos):
            numero='0'+str(numero)

        factura = factura+numero

        if request.method == 'POST':
            action = (request.POST['action'])
            data = []
            if action == 'autocomplete':
                for i in Pacientes.objects.filter(nombre__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)
            elif action == 'autocomplete_ord':
                for o in ordenes.objects.filter(nombre_orden__icontains=request.POST['term']):
                    item = o.toJSON()
                    item['value'] = o.nombre_orden
                    data.append(item)
            elif request.method == 'POST':
                hedFactura = json.loads(request.POST['hedFactura'])
                head = encabezadoFactura()

                head.nombre = hedFactura['nombre_cliente']
                head.identidad = hedFactura['rtn']
                head.telefono = hedFactura['telefono']
                head.direccion = hedFactura['direccion']
                head.factura = hedFactura['factura']
                head.total_factura = hedFactura['total_facturado']
                head.descuento = hedFactura['descuento']
                head.impuesto = hedFactura['impuesto_cob']
                head.fecha_factura = hedFactura['fecha_facturacion']
                head.sub_total = hedFactura['subtotal']
                head.vendedor=hedFactura['vendedor']
                head.tipo_pago=hedFactura['tipo_pago']

                head.save()
                for i in hedFactura['ordenes']:
                    det = detalleFactura()
                    det.fecha_factura = hedFactura['fecha_facturacion']
                    det.factura = hedFactura['factura']
                    det.cod_ord = i['cod_ord']
                    det.nombre = i['nombre_orden']
                    det.descripcion = i['descripcion_orden']
                    det.precio = float(i['precio_orden'])
                    det.sub_total = float(i['subtotal'])
                    det.cantidad = int(i['cantidad'])
                    det.save()

                orden_trabajo = ordenes_emitidas(request.POST)

                
                for s in hedFactura['ordenes']:
                    orden_trabajo.cod_ord = s['cod_ord']
                    orden_trabajo.nombre_orden = s['nombre_orden']
                    enc = ordenes.objects.filter(
                        cod_ord=s['cod_ord']).values_list('encargado_orden')
                    enc = str(enc[0]).replace("'", "").replace("[", "").replace("]", "").replace(
                        "'", "").replace(",", "").replace("(", "").replace(")", "")
                    orden_trabajo.estado = 'Pendiente'
                    orden_trabajo.encargado_orden = enc
                    orden_trabajo.fecha_emision = datetime.now()
                    cantidad=int(s['cantidad'])

                    id_orden=ordenes.objects.filter(cod_ord=orden_trabajo.cod_ord).filter(nombre_orden=orden_trabajo.nombre_orden).values_list('pk',flat=True)[0]
                    print('Esta es la orden',str(id_orden))
                    det_inv=detalle_inv.objects.filter(ordenes_id=id_orden)

                    for de in det_inv: 
                        producto=inventProd.objects.filter(pk=de.inventprod_id).values_list('producto',flat=True).first()
                        prod_inv=inventProd.objects.filter(pk=de.inventprod_id).values_list('cantidad_inv',flat=True).first()
                        print('Viendo producto e inventario',producto,' ',str(prod_inv))

                        inventProd.objects.filter(pk=de.inventprod_id).update(cantidad_inv=int(prod_inv)-1)           
        
                        prod_inv=inventProd.objects.filter(pk=de.inventprod_id).values_list('cantidad_inv',flat=True).first()
                        print('Nuevo inventario',producto,' ',str(prod_inv))

                    formulario=ordenes.objects.filter(nombre_orden=orden_trabajo.nombre_orden).values_list('formulario',flat=True)[0]    

                    if cantidad > 1:  
                        for r in range(cantidad):
                            #Ingresando el detalle de la factura
                            ordenes_emitidas.objects.create(cod_ord=orden_trabajo.cod_ord,nombre_orden=orden_trabajo.nombre_orden, encargado_orden=enc, estado=orden_trabajo.estado, fecha_emision=orden_trabajo.fecha_emision,paciente=head.nombre,dir_pac=head.direccion,identif_pac=head.identidad)

                            #Ingresando el formulario que corresponde
                            ordenes_emitidas.objects.filter(nombre_orden=orden_trabajo.nombre_orden).update(formulario=formulario)
                    else:
                            #Ingresando el detalle de la factura
                        ordenes_emitidas.objects.create(cod_ord=orden_trabajo.cod_ord,nombre_orden=orden_trabajo.nombre_orden, encargado_orden=enc, estado=orden_trabajo.estado, fecha_emision=orden_trabajo.fecha_emision,paciente=head.nombre,dir_pac=head.direccion,identif_pac=head.identidad)

                            #Ingresando el formulario que corresponde
                        ordenes_emitidas.objects.filter(nombre_orden=orden_trabajo.nombre_orden).update(formulario=formulario)

                            #Restando existencias en inventario

                info_facturas.objects.filter(sucursal=suc).update(fac_actual=int(numero)+1)           

            return JsonResponse(data, safe=False)
        return render(request, 'ordenes/facturafiscal_form.html', {"form_fac": form_fac, "form_cli": form_cli, "form_ord": form_ord, "isv": isv, "factura": factura,"form_vend":form_vend,"dir_cli":dir_cli,"tipo_pago":tipo_pago,"excede":excede,"cai":cai,"ult_cli":ult_cli,'inv_fuera':inv_fuera,'form_fecha':form_fecha,'ult_fact':ult_fact})

    except Exception as e:

        print('Se produjo este error: ',e)

        #return JsonResponse(data, safe=False)
        return render(request, 'home/error.html',{"error":e})



def imprimirFactura(request):        
    ultima_fact=encabezadoFactura.objects.latest('id') 

    usuario=str(request.user)
    user_suc=listUsuarios()
    suc=""

    for us_suc in user_suc:
        data=str(us_suc).replace("'","").replace(")","").replace("(","")
        usuario_model=((data[int(data.find(',')+1):100]).replace(" ","")).replace(" ","")

        if usuario_model==usuario:
            suc=(data[0:int(data.find(','))])

    template=get_template('facturacion/recibo_pdf.html')
    context={
            'fact':REPORTE_FACT.objects.get(pk=ultima_fact.id),
            'suc':sucursales.objects.get(nombre_sucursal=suc),
            'cai':info_facturas.objects.filter(sucursal=suc).values_list('cai',flat=True)[0]            
#                'icon':'{}{}'.format(settings.MEDIA_URL)
            }
    html_template= template.render(context)
    css_url=os.path.join(settings.BASE_DIR,'static/vendor/bootstrap/css/bootstrap.min.css')
    pdf=HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
    response=HttpResponse(pdf,content_type='application/pdf')
    #response['Content-Disposition']='attacment;filename="Recibo_Compra_'+REPORTE_FACT.objects.filter(pk=ultima_fact.id).values_list('nombre',flat=True).first()+'.pdf"'
    return redirect('/rep_fact_pdf') 





class facturaCreateView(CreateView):
    form_class = facturaForm
    model = facturaFiscal
    success_url = '/'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = ordenes.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


@method_decorator(csrf_exempt)
def ordatendOp(request):
    return render(request, 'ordenes/opc_ord_att.html')

@method_decorator(csrf_exempt)
def ordreportes(request):
    return render(request, 'ordenes/opc_reportes.html')


# Vista para enlistar las ordenes a atender

class listar_facturasListView(ListView):
    form_class = headFactForm
    paginate_by=7
    model=encabezadoFactura
    ordering = ['-pk']


    def get_queryset(self):
        cli = self.request.GET.get('search')
        fact = self.request.GET.get('fact')
        if  cli:
            reporte_fact = encabezadoFactura.objects.filter(nombre__contains=cli).order_by('-pk')
        elif fact:
            reporte_fact = encabezadoFactura.objects.filter(factura__contains=fact).order_by('-pk')
        else:            
            reporte_fact = encabezadoFactura.objects.order_by('-pk')            
        return reporte_fact



    def get_context_data(self,**kwargs):
        context = super(listar_facturasListView,self).get_context_data(**kwargs)
        context['fact']=busqueda_fact()
        context['cli']=listado_clientes()        
        return context



class l_ordatendOpListView(ListView):
    paginate_by = 7
    model = ordenes_emitidas

    def get_queryset(self, **kwargs):
        print('Viendo aqui a ver...')
#        rol=usuario_log.objects.values_list('rol',flat=True)[0]       
        rol=0

        if (rol ==0) or (rol ==1) or (rol ==4):
            return ordenes_emitidas.objects.filter(estado='Pendiente').filter(formulario__in=[rol,3]).order_by('-pk')
        else:
            return ordenes_emitidas.objects.filter(estado='Pendiente').order_by('-pk')
    


# Cerrar ordenes manualmente
def cierre_man_orden(request,pk):
    if request.method == 'POST':
        ordenes_emitidas.objects.filter(id=pk).update(estado='Cancelado')  
        return redirect('/att_ord_all')
    finalizar='cancelar'        
    return render(request,'ordenes/cerrar_orden.html',{"finalizar":finalizar})
   

# Cancelar ordenes
def fin_man_orden(request,pk):
    if request.method == 'POST':
        iden=pk

        ordenes_emitidas.objects.filter(id=pk).update(estado='Finalizado')  
        return redirect('/att_ord_all')
    finalizar='fin'
    return render(request,'ordenes/cerrar_orden.html',{"finalizar":finalizar})



#trabajando con el examen psicologico

@method_decorator(login_required, name='dispatch')
class lispregPsiListView(ListView):
    form_class = exam_psicologicoForm
    paginate_by = 7
    model = examen_psi



@method_decorator(login_required, name='dispatch')
class pregPsicoCreateView(CreateView):
    form_class = exam_psicologicoForm
    model = examen_psi
    success_url = '/psi_preg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context


@method_decorator(login_required, name='dispatch')
class pregPsicoAcUpdateView(UpdateView):
    form_class = exam_psicologicoForm
    model = examen_psi
    success_url = '/psi_preg'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


@method_decorator(login_required, name='dispatch')
class pregPsicoBorDeleteView(DeleteView):
    model = examen_psi
    success_url = '/psi_preg'


#Modulo de resultados

@method_decorator(csrf_exempt)
def ExamResultados(request):
    return render(request, 'ordenes/resultados_menu.html')



#Vistas para la funcionalidad de adelantos

class listar_adelantosListView(ListView):
    form_class = form_adelantos
    paginate_by=7
    model=adelantos
    ordering = ['-pk']



@method_decorator(login_required, name='dispatch')
class adelantoCreateView(CreateView):
    form_class = form_adelantos
    model = adelantos
    success_url = '/list_adelantos'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create',
        })
        return context


@method_decorator(login_required, name='dispatch')
class adelantoDeleteView(DeleteView):
    model = adelantos
    success_url = '/list_adelantos'


@method_decorator(login_required, name='dispatch')
class adelUpdateView(UpdateView):
    form_class = form_adelantos
    model = adelantos
    success_url = '/list_adelantos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


#Vistas para ingreso de proveedores

class listar_provListView(ListView):
    form_class = provForm
    paginate_by=7
    model=proveedores
    ordering = ['-pk']




    def get_queryset(self):

        queryset = super().get_queryset()
        fecha_inicio = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_ingreso__range=(fecha_inicio, fecha_fin))
        return queryset.order_by('-pk')



    def get_context_data(self,**kwargs):
        context = super(listar_provListView,self).get_context_data(**kwargs)
        context['form']=form_bus() 

        return context


















@method_decorator(login_required, name='dispatch')
class proovCreateView(CreateView):
    form_class = provForm
    model = proveedores
    success_url = '/list_prov'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create',
        })
        return context


@method_decorator(login_required, name='dispatch')
class proovDeleteView(DeleteView):
    model = proveedores
    success_url = '/list_prov'


@method_decorator(login_required, name='dispatch')
class provUpdateView(UpdateView):
    form_class = provForm
    model = proveedores
    success_url = '/list_prov'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

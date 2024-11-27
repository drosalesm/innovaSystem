import xlwt
import os
from datetime import date, datetime,timedelta
from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings
from weasyprint import CSS, HTML
from django.http import HttpResponse, JsonResponse
from django.views import View
from applications.sucursales.models import sucursales
from applications.usuarios_inova.views import listUsuarios
from applications.ordenes.forms import vend_form,productos_form,listado_clientes
from applications.ordenes.models import *
from applications.pacientes.models import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from .forms import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from applications.ordenes.models import encabezadoFactura,detalleFactura
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.db.models import Sum,Count,Func,F
from openpyxl import Workbook
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.templatetags.static import static




today = date.today()


@method_decorator(login_required, name='dispatch')
class lisDetailFacturacion(ListView):
    paginate_by = 7
    model = info_facturas


@method_decorator(login_required, name='dispatch')
class DetFactCreateView(CreateView):
    form_class = info_facturasForm
    model = info_facturas
    success_url = '/info_fac'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suc = sucursales.objects.values_list('nombre_sucursal',flat=True).distinct()
        
        context.update({
            'view_type': 'create',
            'suc':suc
        })
        return context


@method_decorator(login_required, name='dispatch')    
class delInfoFactGen(DeleteView):
    model = info_facturas
    success_url = '/info_fac'



@method_decorator(login_required, name='dispatch')
class infFacturasUpdateView(UpdateView):
    form_class = info_facturasForm
    model = info_facturas
    success_url = '/info_fac'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
@login_required
@method_decorator(csrf_exempt)
def factOpciones(request):
    return render(request,'facturacion/list_det_facturacion.html')

@method_decorator(login_required, name='dispatch')
class listFacturasListView(ListView):
    paginate_by = 10
    model = encabezadoFactura
    ordering = ['-pk']    


@method_decorator(login_required, name='dispatch')    
class listFactDeleteView(DeleteView):
    model = encabezadoFactura
    success_url = '/list_fac'

    def delete(self, *args, **kwargs):
        id = self.kwargs['pk']
        print(id)
        try:
            fac=encabezadoFactura.objects.filter(pk=id).values_list('factura',flat=True)[0]
            detalleFactura.objects.filter(factura=fac).delete()
            print('Factura eliminada correctamente')
        except Exception as e:
            print('Hubo un problema al borrar la factura')
        return super(listFactDeleteView, self).delete(*args, **kwargs)



#---Inventario de productos

@method_decorator(login_required, name='dispatch')
class listInvProd(ListView):
    form_class = form_inv_prod    
    paginate_by = 10
    model = inventProd
    ordering='-pk'


#@method_decorator(login_required, name='dispatch')
class invtProdCreateView(CreateView):
    form_class = form_inv_prod
    model = inventProd
    success_url = '/list_inv_p'
    template_name = 'facturacion/invt_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'view_type': 'create'
        })
        return context


@method_decorator(login_required, name='dispatch')    
class delInvProd(DeleteView):
    model = inventProd
    success_url = '/list_inv_p'

#@method_decorator(login_required, name='dispatch')
class invProdUpdateView(UpdateView):
    form_class = form_inv_prod
    model = inventProd
    success_url = '/list_inv_p'
    template_name = 'facturacion/invt_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

def Rep_Fact_vend(request):
    form=form_bus()
    fecha_hoy =today.strftime('%Y-%m-%d')
    fecha_atras =(date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    form_vend=vend_form(request.POST)

    reporte=REPORTE_VENTAS.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('vendedor').annotate(total_monto_venta=Sum('monto_venta'),cant_ventas=Sum('conteo')).order_by('-total_monto_venta')

    if request.method=='POST':

        fecha_atras=datetime.strptime(request.POST['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_hoy=datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').strftime('%Y-%m-%d')
        vend=request.POST['vendedor']

        if vend:
            reporte=REPORTE_VENTAS.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).filter(vendedor=vend).values('vendedor').annotate(total_monto_venta=Sum('monto_venta'),cant_ventas=Sum('conteo')).order_by('-total_monto_venta')
        else:
            reporte=REPORTE_VENTAS.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('vendedor').annotate(total_monto_venta=Sum('monto_venta'),cant_ventas=Sum('conteo')).order_by('-total_monto_venta')
        

        return render(request,'facturacion/reporte_ventas.html',{'form':form,'reporte':reporte,'form_vend':form_vend,'fecha_hoy':fecha_hoy,'fecha_atras':fecha_atras})
    return render(request,'facturacion/reporte_ventas.html',{'form':form,'reporte':reporte,'form_vend':form_vend,'fecha_hoy':fecha_hoy,'fecha_atras':fecha_atras})

def getClientes(request):
    if request.method=='POST':
        action = (request.POST['action'])
        data = []
        if action == 'autocomplete':
            print(action)
            for i in Pacientes.objects.filter(nombre__icontains=request.POST['term']):
                item = i.toJSON()
                item['value'] = i.nombre
                data.append(item)
        return JsonResponse(data, safe=False)

def Rep_Fact_pdf(request):
    form=form_bus()
    fecha_fin =today.strftime('%Y-%m-%d')
    fecha_ini =date.today() + timedelta(days=-1)
    fecha_ini=fecha_ini.strftime('%Y-%m-%d')
    form_cli = listado_clientes(request.POST)


    reporte = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).order_by('-pk').all()
    suma_fact = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).aggregate(Sum('total_factura'))['total_factura__sum']


    if request.method=='POST':

        fecha_ini=datetime.strptime(request.POST['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin=datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').strftime('%Y-%m-%d')

        cli=request.POST['search']

        if cli:
            reporte = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).filter(nombre=cli)
            suma_fact = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).filter(nombre=cli).aggregate(Sum('total_factura'))['total_factura__sum']
        else:
            reporte = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).all()
            suma_fact = REPORTE_FACT.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).aggregate(Sum('total_factura'))['total_factura__sum']
        return render(request,'facturacion/reporte_facturas.html',{'form':form,'reporte':reporte,'suma_fact':suma_fact,'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,'form_cli':form_cli})
    return render(request,'facturacion/reporte_facturas.html',{'form':form,'reporte':reporte,'suma_fact':suma_fact,'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,'form_cli':form_cli})

def Rep_Fact_prod(request):
    form=form_bus()
    fecha_fin =today.strftime('%Y-%m-%d')
    fecha_ini =date.today() + timedelta(days=-7)
    fecha_ini=fecha_ini.strftime('%Y-%m-%d')
    form_prod=productos_form()
    reporte=REPORTE_PROD.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).values('nombre').annotate(total_fact=Sum('total_facturado'),cant_ord=Sum('total_ordenes')).order_by('-total_fact')
    
    if request.method=='POST':
        prod=request.POST['producto']
        fecha_ini=datetime.strptime(request.POST['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_fin=datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').strftime('%Y-%m-%d')

        if prod:
            reporte=REPORTE_PROD.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).filter(nombre=prod).values('nombre').annotate(total_fact=Sum('total_facturado'),cant_ord=Sum('total_ordenes')).order_by('-total_fact')
        else:
            reporte=REPORTE_PROD.objects.filter(fecha_factura__range=[fecha_ini,fecha_fin]).values('nombre').annotate(total_fact=Sum('total_facturado'),cant_ord=Sum('total_ordenes')).order_by('-total_fact')

        return render(request,'facturacion/reporte_productos.html',{'form':form,'reporte':reporte,'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,'form_prod':form_prod})
    return render(request,'facturacion/reporte_productos.html',{'form':form,'reporte':reporte,'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,'form_prod':form_prod})
      

       


class reciboPdf1(View):
    def get(self,request,*args,**kwargs):




            usuario=str(request.user)
            user_suc=listUsuarios()
            suc=""
            
            for us_suc in user_suc:
                data=str(us_suc).replace("'","").replace(")","").replace("(","")
                usuario_model=((data[int(data.find(',')+1):100]).replace(" ","")).replace(" ","")

                if usuario_model==usuario:
                    suc=(data[0:int(data.find(','))])


            factura=REPORTE_FACT.objects.get(pk=self.kwargs['pk']),
            n_factura=REPORTE_FACT.objects.values_list('factura').filter(pk=self.kwargs['pk'])[0]
            n_fact_dep=str(n_factura).replace("'","").replace(")","").replace("(","").replace(",","")

            ordenes=detalleFactura.objects.filter(factura=n_fact_dep)

            inf_factu = info_facturas.objects.get(sucursal=suc)

            valor_uno=inf_factu.numeracion
            valor_dos=str(inf_factu.rango_inicial)
            valor_tres=str(inf_factu.rango_final)

            if len(valor_dos) < 8:
                dig_ri=8-len(valor_dos)
            for x in range(dig_ri):
                valor_dos='0'+str(valor_dos)

            if len(valor_tres) < 8:
                dig_rf=8-len(valor_tres)
            for x in range(dig_rf):
                valor_tres='0'+str(valor_tres)

            rango_inicial = inf_factu.numeracion+valor_dos
            rango_final = inf_factu.numeracion+valor_tres
            print(rango_inicial)

            template=get_template('facturacion/recibo_pdf.html')
            context={
                    'fact':factura,
                    'suc':sucursales.objects.get(nombre_sucursal=suc),
                    'fact_parm':info_facturas.objects.get(sucursal=suc),
                    'ord':ordenes,
                    'us':usuario,
                    'ri':rango_inicial,
                    'rf':rango_final,
    #                'icon':'{}{}'.format(settings.MEDIA_URL)
                    }


            html_template= template.render(context)
            css_url=os.path.join(settings.BASE_DIR,'static/vendor/bootstrap/css/bootstrap.min.css')
            pdf=HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            response=HttpResponse(pdf,content_type='application/pdf')
            #response['Content-Disposition']='attacment;filename="Recibo_Compra_'+REPORTE_FACT.objects.filter(pk=self.kwargs['pk']).values_list('nombre',flat=True).first()+'.pdf"'
            return response 








# Nueva implementacion de factura PDF

class reciboPdf(View):
    def get(self, request, *args, **kwargs):


        try:

            usuario=str(request.user)
            user_suc=listUsuarios()
            suc=""
            
            for us_suc in user_suc:
                data=str(us_suc).replace("'","").replace(")","").replace("(","")
                usuario_model=((data[int(data.find(',')+1):100]).replace(" ","")).replace(" ","")

                if usuario_model==usuario:
                    suc=(data[0:int(data.find(','))])


            factura=REPORTE_FACT.objects.get(pk=self.kwargs['pk']),
            n_factura=REPORTE_FACT.objects.values_list('factura').filter(pk=self.kwargs['pk'])[0]
            n_fact_dep=str(n_factura).replace("'","").replace(")","").replace("(","").replace(",","")

            ordenes=detalleFactura.objects.filter(factura=n_fact_dep)

            inf_factu = info_facturas.objects.get(sucursal=suc)

            valor_uno=inf_factu.numeracion
            valor_dos=str(inf_factu.rango_inicial)
            valor_tres=str(inf_factu.rango_final)

            if len(valor_dos) < 8:
                dig_ri=8-len(valor_dos)
            for x in range(dig_ri):
                valor_dos='0'+str(valor_dos)

            if len(valor_tres) < 8:
                dig_rf=8-len(valor_tres)
            for x in range(dig_rf):
                valor_tres='0'+str(valor_tres)

            rango_inicial = inf_factu.numeracion+valor_dos
            rango_final = inf_factu.numeracion+valor_tres

            sucursal_act=sucursales.objects.get(nombre_sucursal=suc)
            fact_param=info_facturas.objects.get(sucursal=suc)


            # Funciones de reportLab.
            response = HttpResponse(content_type='application/pdf')
            pdf = canvas.Canvas(response, pagesize=letter)
            pdf.setFont("Times-Roman", 10)

            image_path = "http://127.0.0.1:8000/static/img/inova_img2.jpeg" 

            pdf.drawImage(image_path, 250, 700, width=80, height=50)
            
            pdf.setTitle("Factura PDF")  # set the document title

            pos=680

            # Add the receipt title.
            pdf.drawCentredString(300, pos, "CEMEP")
            pos=pos-15
            pdf.drawCentredString(300, pos, "CENTRO DE EVALUACIONES MEDICAS Y PSICOLOGICAS")
            pos=pos-15
            pdf.drawCentredString(300,pos,sucursal_act.direccion.upper())
            pos=pos-20
            pdf.drawCentredString(300,pos,"************FACTURA************")
            pos=pos-20
            pdf.drawString(50,pos,"INVERSIONES INOVA S DE RL DE CV")
            pos=pos-15
            pdf.drawString(50,pos,"TELEFONO: "+sucursal_act.telefono+"   "+"CORREO: "+sucursal_act.correo)
            pos=pos-15
            pdf.drawString(50,pos,"RTN: "+sucursal_act.rtn)
            pos=pos-15
            pdf.drawString(50,pos,"CAI: "+inf_factu.cai)

            for fac_p in factura:
                fact_sbt=fac_p.sub_total
                descuento=fac_p.descuento
                impuesto=fac_p.impuesto
                tot_fact=fac_p.total_factura
                t_pago=fac_p.tipo_pago
                cliente=fac_p.nombre.upper()

                pos=pos-15
                pdf.drawString(50,pos,"FACTURA: "+fac_p.factura)
                pos=pos-15
                pdf.drawString(50,pos,"FECHA: "+str(fac_p.fecha_factura))
                pos=pos-15
                pdf.drawString(50,pos,"VENDEDOR: "+fac_p.vendedor.upper())
                pos=pos-20
                pdf.drawString(50,pos,"CLIENTE: "+cliente)
                pos=pos-15
                pdf.drawString(50,pos,"IDENTIDAD / RTN: "+fac_p.identidad)
            pos=pos-20
            pdf.drawString(50,pos,"No COMPRA EXCENTA: No REGISTRO SAG")
            pos=pos-15        
            pdf.drawString(50,pos,"No CONSTANCIA REGISTRO EXONERADO")
            pos=pos-15        
            pdf.drawString(50,pos,"ORIGINAL: CLIENTE COPIA: OBLIGADO TRIBUTARIO EMISOR")
            pos=pos-20
            pdf.drawString(50,pos,"DESCRIPCION                                                                                           CANT.                 P.U               TOTAL")
            pos=pos-15
            pdf.drawString(50,pos,"--------------------------------------------------------------------------------------------------------------------------------------")        


            for ord_act in ordenes:
                pos=pos-15                        
                pdf.drawString(50,pos,ord_act.nombre.upper())            
                pdf.drawString(345,pos,str(ord_act.cantidad))            
                pdf.drawString(415,pos,"L "+str(ord_act.precio))    
                pdf.drawString(470,pos,"L "+str(ord_act.sub_total))    
            pos=pos-15                        
            pdf.drawString(50,pos,"--------------------------------------------------------------------------------------------------------------------------------------")        

            pos=pos-15                        
            pdf.drawString(380,pos,"IMPORTE")
            pdf.drawString(470,pos,"L "+str(fact_sbt))
            pos=pos-15                        
            pdf.drawString(310,pos,"IMPORTE EXPONERADO")
            pos=pos-15                        
            pdf.drawString(338,pos,"IMPORTE EXENTO")
            pos=pos-15                        
            pdf.drawString(342,pos,"IMPORTE ISV 15%")
            pdf.drawString(470,pos,"L "+str(fact_sbt))
            pos=pos-15                        
            pdf.drawString(342,pos,"IMPORTE ISV 18%")
            pos=pos-15                        
            pdf.drawString(304,pos,"DESCUENTO O REBAJAS%")
            pdf.drawString(470,pos,"L "+str(impuesto))
            pos=pos-15                        
            pdf.drawString(390,pos,"ISV 15%")
            pdf.drawString(470,pos,"L "+str(descuento))
            pos=pos-15                        
            pdf.drawString(390,pos,"ISV 18%")
            pos=pos-15                        
            pdf.drawString(394,pos,"TOTAL")
            pdf.drawString(470,pos,"L "+str(tot_fact))

            tipo_pag=""
            if t_pago=='1':
                tipo_pag="EFECTIVO"
            elif t_pago=='2':
                tipo_pag="TARJETA VISA"            
            elif t_pago=='3':
                tipo_pag="TARJETA MASTERCARD"            

            pos=pos-20                        
            pdf.drawString(50,pos,"PAGO: "+tipo_pag)
            pos=pos-15                                
            pdf.drawString(50,pos,"CAJERO CODIGO: "+usuario.upper())
            pos=pos-15
            pdf.drawString(50,pos,"RANGO AUTORIZADO DE FACTURA LIMITE DE EMISIÓN: "+str(inf_factu.fecha_lim_em))
            pos=pos-15
            pdf.drawString(50,pos,rango_inicial+" AL "+rango_final)
    

            response['Content-Disposition'] = 'attachment; filename="factura_'+cliente.replace(" ","_")+'.pdf"'
            pdf.save()



            return response

        except Exception as e:

            return render(request, 'home/error.html',{"error":e})




def rep_cierre_diario(request):
    form=form_bus()
    fecha_hoy =today.strftime('%Y-%m-%d')
    fecha_atras =(date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')    
    fondo_caja=5000


 
    try: 

        tot_ventas = cierre_diario_tot_vent.objects.filter(fecha_factura__range=[fecha_atras, fecha_hoy]).aggregate(total_ventas_sum=Sum('total_ventas')).get('total_ventas_sum', 0) or 0
        cd_vend=cierre_diario_vend.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('vendedor').annotate(total_monto_venta=Sum('monto_venta'),cant_ventas=Sum('total_facturas'),total_adelanto=Sum('monto_adelanto'),total_adelantos=Sum('adelantos'),total_a_pagar=Sum('total_pago')).all()


        cd_tot_ord = str(cierre_diario_vend.objects.filter(fecha_factura__range=[fecha_atras, fecha_hoy]).aggregate(total_fact=Func(Sum('total_facturas'), 0, function='COALESCE'))).replace("{'total_fact':",'').replace('}','')

        tot_adel = adelantos.objects.filter(fecha_solicitud__range=[fecha_atras, fecha_hoy]).aggregate(total_add=Sum('cantidad')).get('total_add',0) or 0
        print(tot_adel)

        det_adel=adelantos.objects.filter(fecha_solicitud__range=[fecha_atras,fecha_hoy]).values('solicitante').annotate(total_monto_sol=Sum('cantidad'),total_cant_adel=Count('cantidad')).all()

        det_prod=cierre_diario_tot_prod.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('nombre').annotate(tot_mont_fact=Sum('total_facturado'),tot_or=Sum('total_ordenes')).all()
        tot_cant_adel = str(adelantos.objects.filter(fecha_solicitud__range=[fecha_atras, fecha_hoy]).aggregate(cant_adel=Func(Count('cantidad'), 0, function='COALESCE'))).replace("{'cant_adel':",'').replace('}','')

        det_mp=cierre_diario_tot_mp.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('tipo_pago').annotate(tot_mont_mp=Sum('total_ventas')).all()

        det_arqueo=rep_arqueo_caja.objects.filter(fecha_registro__range=[fecha_atras,fecha_hoy]).values('billete').annotate(total_cant_bill=Sum('cantidad'),total_cant_mont=Sum('monto_total')).all()
        total_arqueo = str(rep_arqueo_caja.objects.filter(fecha_registro__range=[fecha_atras, fecha_hoy]).aggregate(total_arq=Func(Sum('monto_total'), 0, function='COALESCE'))).replace("{'total_arq':",'').replace('}','')

        tot_vent_efe_c=int(total_arqueo)-fondo_caja




    except Exception as e:

        print('Se produjo este error: ',e)

        #return JsonResponse(data, safe=False)
        return render(request, 'home/error.html',{"error":e})



    if request.method=='POST':


        fecha_atras=datetime.strptime(request.POST['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
        fecha_hoy=datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').strftime('%Y-%m-%d')

        try: 


            tot_ventas = cierre_diario_tot_vent.objects.filter(fecha_factura__range=[fecha_atras, fecha_hoy]).aggregate(total_ventas_sum=Sum('total_ventas')).get('total_ventas_sum', 0) or 0
            cd_vend=cierre_diario_vend.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('vendedor').annotate(total_monto_venta=Sum('monto_venta'),cant_ventas=Sum('total_facturas'),total_adelanto=Sum('monto_adelanto'),total_adelantos=Sum('adelantos'),total_a_pagar=Sum('total_pago')).all()
            cd_tot_ord = str(cierre_diario_vend.objects.filter(fecha_factura__range=[fecha_atras, fecha_hoy]).aggregate(total_fact=Func(Sum('total_facturas'), 0, function='COALESCE'))).replace("{'total_fact':",'').replace('}','')


            tot_adel = adelantos.objects.filter(fecha_solicitud__range=[fecha_atras, fecha_hoy]).aggregate(total_add=Sum('cantidad')).get('total_add',0) or 0
            det_adel=adelantos.objects.filter(fecha_solicitud__range=[fecha_atras,fecha_hoy]).values('solicitante').annotate(total_monto_sol=Sum('cantidad'),total_cant_adel=Count('cantidad')).all()
            tot_cant_adel = str(adelantos.objects.filter(fecha_solicitud__range=[fecha_atras, fecha_hoy]).aggregate(cant_adel=Func(Count('cantidad'), 0, function='COALESCE'))).replace("{'cant_adel':",'').replace('}','')


            det_prod=cierre_diario_tot_prod.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('nombre').annotate(tot_mont_fact=Sum('total_facturado'),tot_or=Sum('total_ordenes')).all()
            det_mp=cierre_diario_tot_mp.objects.filter(fecha_factura__range=[fecha_atras,fecha_hoy]).values('tipo_pago').annotate(tot_mont_mp=Sum('total_ventas'),cantidad_ord=Sum('cantidad_fact')).all()



            det_arqueo=rep_arqueo_caja.objects.filter(fecha_registro__range=[fecha_atras,fecha_hoy]).values('billete').annotate(total_cant_bill=Sum('cantidad'),total_cant_mont=Sum('monto_total')).all()
            total_arqueo = str(rep_arqueo_caja.objects.filter(fecha_registro__range=[fecha_atras, fecha_hoy]).aggregate(total_arq=Func(Sum('monto_total'), 0, function='COALESCE'))).replace("{'total_arq':",'').replace('}','')

            tot_vent_efe_c=int(total_arqueo)-fondo_caja

        except Exception as e:
            print('Hubo un error al calcular el total de ventas',e)        

            return render(request, 'home/error.html',{"error":e})


        return render(request,'facturacion/reporte_cierre.html',{'cd_vend':cd_vend,'form':form,'fecha_atras':fecha_atras,'fecha_hoy':fecha_hoy,'tot_ventas':tot_ventas,'tot_adel':tot_adel,'det_adel':det_adel,'det_prod':det_prod,'det_mp':det_mp,'det_arqueo':det_arqueo,'total_arqueo':total_arqueo,'tot_vent_efe_c':tot_vent_efe_c,'fondo_caja':fondo_caja,'cd_tot_ord':cd_tot_ord,'tot_cant_adel':tot_cant_adel})
    return render(request,'facturacion/reporte_cierre.html',{'cd_vend':cd_vend,'form':form,'fecha_atras':fecha_atras,'fecha_hoy':fecha_hoy,'tot_ventas':tot_ventas,'tot_adel':tot_adel,'det_adel':det_adel,'det_prod':det_prod,'det_mp':det_mp,'det_arqueo':det_arqueo,'total_arqueo':total_arqueo,'tot_vent_efe_c':tot_vent_efe_c,'fondo_caja':fondo_caja,'cd_tot_ord':cd_tot_ord,'tot_cant_adel':tot_cant_adel})

# Vistas para el arqueo de caja

@method_decorator(login_required, name='dispatch')
class listarqcaja(ListView):
    form_class = form_arq_caja    
    paginate_by = 10
    model = arqueo_caja
    ordering = ['-fecha_registro']


    def get_queryset(self):

        queryset = super().get_queryset()
        fecha_inicio = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            print('Tengo las fechas',fecha_inicio,fecha_fin)            
            queryset = queryset.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
        else:
            fecha_fin =today.strftime('%Y-%m-%d')
            fecha_inicio =date.today() + timedelta(days=-1)
            fecha_inicio=fecha_inicio.strftime('%Y-%m-%d')
            queryset = queryset.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
        return queryset.order_by('-pk')



    def get_context_data(self,**kwargs):
        context = super(listarqcaja,self).get_context_data(**kwargs)

        fecha_inicio = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            context['fec_ini']=fecha_inicio 
            context['fecha_fin']=fecha_fin
        else:
            fecha_fin =today.strftime('%Y-%m-%d')
            fecha_inicio =date.today() + timedelta(days=-1)
            fecha_inicio=fecha_inicio.strftime('%Y-%m-%d')

            context['fec_ini']=fecha_inicio 
            context['fecha_fin']=fecha_fin

        context['form']=form_bus() 

        return context





#@method_decorator(login_required, name='dispatch')
class arqCajaCreateView(CreateView):
    form_class = form_arq_caja
    model = arqueo_caja
    success_url = '/list_caja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'view_type': 'create'
        })
        return context


@method_decorator(login_required, name='dispatch')    
class delarqCaja(DeleteView):
    model = arqueo_caja
    success_url = '/list_caja'

#@method_decorator(login_required, name='dispatch')
class arqCajaUpdateView(UpdateView):
    form_class = form_arq_caja
    model = arqueo_caja
    success_url = '/list_caja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
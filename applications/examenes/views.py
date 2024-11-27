import os
from urllib import response
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from weasyprint import CSS, HTML
from applications.ordenes.forms import doctor_form
from requests import request
from applications.vendedores.models import vendedores
from applications.ordenes.models import ordenes_emitidas
from applications.pacientes.models import Pacientes
from applications.vendedores.models import vendedores
from applications.facturacion.forms import form_bus
from applications.ordenes.forms import productos_form,listado_clientes
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import *
from django.template.loader import get_template
from django.template import Context
from datetime import date, datetime,timedelta

today = date.today()

@method_decorator(login_required, name='dispatch')
class lisExamenMedListView(ListView):
    paginate_by = 10
    model = examen_med
    ordering = ['-pk']

    def get_queryset(self):
        fecha_ini = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')
        producto = self.request.GET.get('producto')
        cli = self.request.GET.get('search')



        if fecha_ini and fecha_ini and cli==None:
            reporte_medico = examen_med.objects.filter(fecha__range=[fecha_ini,fecha_fin]).order_by('pk')
        elif fecha_ini and fecha_ini and cli:
            reporte_medico = examen_med.objects.filter(fecha__range=[fecha_ini,fecha_fin]).filter(paciente__contains=cli).order_by('pk')
        else:
            fecha_hoy =today.strftime('%Y-%m-%d')
            fecha_atras =date.today() + timedelta(days=-30)            
            reporte_medico = examen_med.objects.filter(fecha__range=[fecha_atras,fecha_hoy]).order_by('pk')        

            print('Ver...',reporte_medico,fecha_hoy,fecha_atras)

        return reporte_medico

    def get_context_data(self,**kwargs):
        context = super(lisExamenMedListView,self).get_context_data(**kwargs)
        context['form'] = form_bus()
        context['prod']=productos_form()
        context['cli']=listado_clientes()        
        return context



# Vista para crear evaluaciones medicas 
@method_decorator(login_required, name='dispatch')
class creExamenMedCreateView(CreateView):
    form_class = exMedico_Form
    model = examen_med
    success_url = '/ex_med_list'


    def get_context_data(self, **kwargs):

        orden=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('pk','nombre_orden','paciente','identif_pac','cod_ord','dir_pac')[0]
        doctor = vendedores.objects.filter(t_empleado=0).values_list('nombre',flat=True).distinct()
        pac=Pacientes.objects.get(identidad=orden[3])          


        print('ver: ',orden)

        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create',
            'name_orden':orden[1],
            'paciente':orden[2],
            'cod_orden':orden[4],
            'direccion':orden[5],
            'identificacion':orden[3],
            'doctor':doctor,
            'orden':orden[0],
            'pac':pac
        })
        return context

#    def post(self, request, *args, **kwargs):    
#        ordenes_emitidas.objects.filter(id=self.kwargs['pk']).update(estado='Finalizado')  
#        print(request.POST['altura'],request.POST.get['paciente'])  
#        return redirect('/ex_med_list')


#ordenes_emitidas.objects.create(cod_ord=orden_trabajo.cod_ord,nombre_orden=orden_trabajo.nombre_orden, encargado_orden=enc, estado=orden_trabajo.estado, fecha_emision=orden_trabajo.fecha_emision,paciente=head.nombre,dir_pac=head.direccion,identif_pac=head.identidad)


@method_decorator(login_required, name='dispatch')
class updExamenMedUpdateView(UpdateView):
    form_class = exMedico_Form
    model = examen_med
    success_url = '/ex_med_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cod_orden = examen_med.objects.filter(pk=self.kwargs['pk']).values_list('cod_orden', flat=True).first()

        identificacion=ordenes_emitidas.objects.filter(id=cod_orden).values_list('identif_pac',flat=True)[0]

        print(self.kwargs['pk'],identificacion)
        pac=Pacientes.objects.get(identidad=identificacion)    
        print(pac.nombre)
        context.update({
            'view_type': 'update',
            'pac':pac            
        })
        return context





# Vista para eliminar examenes medicos
@method_decorator(login_required, name='dispatch')
class delExmMedDeleteView(DeleteView):
    model = examen_med
    success_url = '/ex_med_list'


#Generar Examen medico en PDF
class exMedPdf(View):
    def get(self,request,*args,**kwargs):
        template=get_template('examenes/pdf_exam.html')
        try:
            context={
                'ord':examen_med.objects.get(pk=self.kwargs['pk']),
                #'icon':'{}{}'.format(settings.MEDIA_URL,examen_med.objects.filter(pk=self.kwargs['pk']).values_list('foto',flat=True).first()),
                'coleg':vendedores.objects.filter(nombre=examen_med.objects.filter(pk=self.kwargs['pk']).values_list('doctor',flat=True).first()).values_list('doc_profesional',flat=True).first(),
                'pac':Pacientes.objects.get(identidad=examen_med.objects.filter(pk=self.kwargs['pk']).values_list('identif_pac',flat=True).first())             
                }
            html_template=template.render(context)
            css_url=os.path.join(settings.BASE_DIR,'static/vendor/bootstrap/css/bootstrap.min.css')
            pdf=HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            response=HttpResponse(pdf,content_type='application/pdf')
        #response['Content-Disposition']='attacment;filename="Evaluacion_Medica_'+examen_med.objects.filter(pk=self.kwargs['pk']).values_list('paciente',flat=True).first()+'.pdf"'
        except:
            return render(request,'examenes/pdf_exam_error.html')
        return response



#-------Vistas para el examen psicologico


@method_decorator(login_required, name='dispatch')
class lisExamenPsiListView(ListView):
    paginate_by = 10
    model = examen_psi
    ordering = ['-pk']


    def get_queryset(self):
        fecha_ini = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')
        producto = self.request.GET.get('producto')
        cli = self.request.GET.get('search')

        if fecha_ini and fecha_ini and cli==None:
            reporte_psi = examen_psi.objects.filter(fecha__range=[fecha_ini,fecha_fin]).order_by('pk')
        elif fecha_ini and fecha_ini and cli:
           reporte_psi = examen_med.objects.filter(fecha__range=[fecha_ini,fecha_fin]).filter(paciente__contains=cli).order_by('pk')
        else:
            fecha_hoy =today.strftime('%Y-%m-%d')
            fecha_atras =date.today() + timedelta(days=-30)            
            reporte_psi = examen_psi.objects.filter(fecha__range=[fecha_atras,fecha_hoy]).order_by('pk')        
        return reporte_psi

    def get_context_data(self,**kwargs):
        context = super(lisExamenPsiListView,self).get_context_data(**kwargs)
        context['form'] = form_bus()
        context['prod']=productos_form()
        context['cli']=listado_clientes()          
        return context




# Vista para crear evaluaciones medicas 
@method_decorator(login_required, name='dispatch')
class creExamenPsiCreateView(CreateView):
    form_class = exPsico_Form
    model = examen_psi
    success_url = '/ex_psi_list'

    def get_context_data(self, **kwargs):
        id_orden=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('id',flat=True)[0]
        name_orden=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('nombre_orden',flat=True)[0]
        paciente=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('paciente',flat=True)[0]
        identidad=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('identif_pac',flat=True)[0]
        cod_orden=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('cod_ord',flat=True)[0]
        direccion=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('dir_pac',flat=True)[0]
        identificacion=ordenes_emitidas.objects.filter(id=self.kwargs['pk']).values_list('identif_pac',flat=True)[0]
        psicologo = vendedores.objects.filter(t_empleado=1).values_list('nombre',flat=True).distinct()

        pac=Pacientes.objects.get(identidad=identificacion)          
        print(pac)

        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create',
            'id_orden':id_orden,            
            'name_orden':name_orden,
            'paciente':paciente,
            'cod_orden':cod_orden,
            'direccion':direccion,
            'identificacion':identificacion,
            'psicologo':psicologo,
            'identidad':identidad,
            'pac':pac            
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.method=='POST':
            resultado=[]
            resultado.append(float(request.POST.get('items_del_one')))
            resultado.append(float(request.POST.get('items_del_two')))
            resultado.append(float(request.POST.get('items_del_thre')))
            resultado.append(float(request.POST.get('items_del_four')))
            resultado.append(float(request.POST.get('items_del_five')))
            resultado.append(float(request.POST.get('items_dem_one')))
            resultado.append(float(request.POST.get('items_dem_two')))
            resultado.append(float(request.POST.get('items_dem_thre')))
            resultado.append(float(request.POST.get('items_dem_four')))
            resultado.append(float(request.POST.get('items_dem_five')))
            resultado.append(float(request.POST.get('items_trans_one')))
            resultado.append(float(request.POST.get('items_trans_two')))
            resultado.append(float(request.POST.get('items_trans_thre')))
            resultado.append(float(request.POST.get('items_trans_four')))
            resultado.append(float(request.POST.get('items_trans_five')))
            resultado.append(float(request.POST.get('items_trans_m_one')))
            resultado.append(float(request.POST.get('items_trans_m_two')))
            resultado.append(float(request.POST.get('items_trans_m_thre')))
            resultado.append(float(request.POST.get('items_trans_m_four')))
            resultado.append(float(request.POST.get('items_trans_m_five')))
            resultado.append(float(request.POST.get('items_ezq_one')))
            resultado.append(float(request.POST.get('items_ezq_two')))
            resultado.append(float(request.POST.get('items_ezq_thre')))
            resultado.append(float(request.POST.get('items_ezq_four')))
            resultado.append(float(request.POST.get('items_ezq_five')))
            resultado.append(float(request.POST.get('items_transt_a_one')))
            resultado.append(float(request.POST.get('items_transt_a_two')))
            resultado.append(float(request.POST.get('items_transt_a_thre')))
            resultado.append(float(request.POST.get('items_transt_a_four')))
            resultado.append(float(request.POST.get('items_transt_a_five')))
            resultado.append(float(request.POST.get('items_dis_one')))
            resultado.append(float(request.POST.get('items_dis_two')))
            resultado.append(float(request.POST.get('items_dis_thre')))
            resultado.append(float(request.POST.get('items_dis_four')))
            resultado.append(float(request.POST.get('items_dis_five')))
            resultado.append(float(request.POST.get('items_trans_sue_one')))
            resultado.append(float(request.POST.get('items_trans_sue_two')))
            resultado.append(float(request.POST.get('items_trans_sue_thre')))
            resultado.append(float(request.POST.get('items_trans_sue_four')))
            resultado.append(float(request.POST.get('items_trans_sue_five')))
            resultado.append(float(request.POST.get('items_t_imp_a_one')))
            resultado.append(float(request.POST.get('items_t_imp_a_two')))
            resultado.append(float(request.POST.get('items_t_imp_a_thre')))
            resultado.append(float(request.POST.get('items_t_imp_a_four')))
            resultado.append(float(request.POST.get('items_t_imp_a_five')))
            resultado.append(float(request.POST.get('items_t_pers_one')))
            resultado.append(float(request.POST.get('items_t_pers_two')))
            resultado.append(float(request.POST.get('items_t_pers_thre')))
            resultado.append(float(request.POST.get('items_t_pers_four')))
            resultado.append(float(request.POST.get('items_t_pers_five')))
            resultado.append(float(request.POST.get('items_trans_dint_one')))
            resultado.append(float(request.POST.get('items_trans_dint_two')))
            resultado.append(float(request.POST.get('items_trans_dint_thre')))
            resultado.append(float(request.POST.get('items_trans_dint_four')))
            resultado.append(float(request.POST.get('items_trans_dint_five')))
            resultado.append(float(request.POST.get('items_t_datt_one')))
            resultado.append(float(request.POST.get('items_t_datt_two')))
            resultado.append(float(request.POST.get('items_t_datt_thre')))
            resultado.append(float(request.POST.get('items_t_datt_four')))
            resultado.append(float(request.POST.get('items_t_datt_five')))
            resultado.append(float(request.POST.get('items_com_per_one')))
            resultado.append(float(request.POST.get('items_com_per_two')))
            resultado.append(float(request.POST.get('items_com_per_thre')))
            resultado.append(float(request.POST.get('items_com_per_four')))
            resultado.append(float(request.POST.get('items_com_per_five')))

            #Calculando resultado de examen psicologico
            if round(sum(resultado)) >= 75:
                res_exm='NO APTO'
            else:
                res_exm='APTO'

            #Ingresando el formulario que corresponde
            ordenes_emitidas.objects.filter(pk=request.POST.get('id_orden')).update(resultado=res_exm)


        return super().post(request, *args, **kwargs)



@method_decorator(login_required, name='dispatch')
class updExamenPsiUpdateView(UpdateView):
    form_class = exPsico_Form
    model = examen_psi
    success_url = '/ex_psi_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


# Vista para eliminar examenes medicos
@method_decorator(login_required, name='dispatch')
class delExmPsiDeleteView(DeleteView):
    model = examen_psi
    success_url = '/ex_psi_list'



#Generar Examen psicologico en PDF
class exPsiPdf(View):
    def get(self,request,*args,**kwargs):
        template=get_template('examenes/pdf_examen_psi.html')
        try:        
            context={
                'ord':examen_psi.objects.get(pk=self.kwargs['pk']),
                'ord_emitida':ordenes_emitidas.objects.filter(pk=15).values_list('resultado',flat=True).first(),                
                #'icon':'{}{}'.format(settings.MEDIA_URL,examen_psi.objects.filter(pk=self.kwargs['pk']).values_list('foto',flat=True).first()),
                'coleg':vendedores.objects.filter(nombre=examen_psi.objects.filter(pk=self.kwargs['pk']).values_list('doctor',flat=True).first()).values_list('doc_profesional',flat=True).first(),
                'pac':Pacientes.objects.get(identidad=examen_psi.objects.filter(pk=self.kwargs['pk']).values_list('identif_pac',flat=True).first())             
                }
            html_template=template.render(context)
            css_url=os.path.join(settings.BASE_DIR,'static/vendor/bootstrap/css/bootstrap.min.css')
            pdf=HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            response=HttpResponse(pdf,content_type='application/pdf')
        #response['Content-Disposition']='attacment;filename="Evaluacion_psicologica_'+examen_psi.objects.filter(pk=self.kwargs['pk']).values_list('paciente',flat=True).first()+'.pdf"'
        except:
            return render(request,'examenes/pdf_exam_error.html')
        return response

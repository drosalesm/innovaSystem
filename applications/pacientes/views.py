from multiprocessing import Array
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from requests import request
from .models import pacOpciones,Pacientes
from .forms import pacientesForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from datetime import date, datetime,timedelta
import os
from applications.facturacion.forms import form_bus


today = date.today()

#Vista de opciones generales del modulo pacientes
@method_decorator(login_required, name='dispatch')
class lisPacInfListView(ListView):
    model = pacOpciones

#Vista para enlistar los pacientes
@method_decorator(login_required, name='dispatch')
class lisPacOpcListView(ListView):
    paginate_by = 10
    model = Pacientes
    form_class = pacientesForm
    ordering = ['-pk']


    def get_queryset(self):

        queryset = super().get_queryset()
        fecha_inicio = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_registro__range=(fecha_inicio, fecha_fin))
        return queryset.order_by('-pk')



    def get_context_data(self,**kwargs):
        context = super(lisPacOpcListView,self).get_context_data(**kwargs)

        fecha_inicio = self.request.GET.get('fecha')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            context['fec_ini']=fecha_inicio 
            context['fecha_fin']=fecha_fin

        context['form']=form_bus() 

        return context



def listPacientes(request):
    pac = Pacientes.objects.all().order_by('-nombre')
    return render(request, 'pacientes/pacientes_list.html', {"pac": pac})


#Vista para crear pacientes
@method_decorator(login_required, name='dispatch')
class pacCreateView(CreateView):
    form_class = pacientesForm
    model = Pacientes
    success_url = '/lisPacOpcListView'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context

#Vista para actualizar pacientes
@method_decorator(login_required, name='dispatch')
class pacUpdateView(UpdateView):
    form_class = pacientesForm
    model = Pacientes
    success_url = '/lisPacOpcListView'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

#Vista para eliminar pacientes
@method_decorator(login_required, name='dispatch')
class pacDeleteView(DeleteView):
    model = Pacientes
    success_url = '/lisPacOpcListView'

def openCamera(request):
    os.system('file.sh')
    print('Se llamo a la camara tio..')
    return redirect('/pacCreateView')
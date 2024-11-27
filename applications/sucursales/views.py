from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from requests import request
from .forms import *
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class lisSucListView(ListView):
    paginate_by = 7
    model = sucursales

class sucursalesCreateView(CreateView):
    form_class = sucursalesForm
    model = sucursales
    success_url = '/sucursales_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context


class sucursalUpdateView(UpdateView):
    form_class = sucursalesForm
    model = sucursales
    success_url = '/sucursales_all'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context


#Vista para eliminar ordenes
class sucurDeleteView(DeleteView):
    model = sucursales
    success_url = '/sucursales_all'

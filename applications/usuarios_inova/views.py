from django.shortcuts import render
from django.urls import reverse_lazy
from requests import request
from urllib.request import Request
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def listUsuarios():
    usuarios=User.objects.values_list('sucursal','username')
    return usuarios

# Create your views here.
class lisUsersView(ListView):
    paginate_by = 7
    model = User
    ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type':'list',
        })
        return context


class registroUser(CreateView):
    model=User
    form_class=FormUser
    success_url='/usuarios_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suc = sucursales.objects.values_list('nombre_sucursal',flat=True).distinct()
        context.update({
            'view_type': 'create',
            'suc':suc,
        })
        return context


@method_decorator(login_required, name='dispatch')
class actualizarUser(UpdateView):
    form_class = FormUser
    model = User
    success_url = '/usuarios_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        suc = sucursales.objects.values_list('nombre_sucursal',flat=True).distinct()        
        context.update({
            'view_type': 'update',
            'suc':suc,            
        })
        return context


@method_decorator(login_required, name='dispatch')
class usersDeleteView(DeleteView):
    model = User
    success_url = '/usuarios_list'
from django.shortcuts import render
from .forms import *
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView


# Create your views here.
def vendedoresInicio(request):
    return render(request,'vendedores/vendedores.html')


class lisVendListView(ListView):
    paginate_by = 7
    model = vendedores


class vendCreateView(CreateView):
    form_class = vendedoresForm
    model = vendedores
    success_url = '/list_vend'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context



class vendUpdateView(UpdateView):
    form_class = vendedoresForm
    model = vendedores
    success_url = '/list_vend'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context

#Vista para eliminar ordenes
class vendDeleteView(DeleteView):
    model = vendedores
    success_url = '/list_vend'
from django import forms
from applications.ordenes.models import encabezadoFactura
from crispy_forms.helper import FormHelper
from xml.dom.minidom import Attr
from .models import *
from applications.vendedores.models import vendedores


class info_facturasForm(forms.ModelForm):
    class Meta:
        model = info_facturas
        fields = ('__all__')

class list_facturas(forms.ModelForm):
    class Meta:
        model = encabezadoFactura
        fields = ('__all__')


class form_inv_prod(forms.ModelForm):
    class Meta:
        model = inventProd
        fields = ('__all__')

class form_arq_caja(forms.ModelForm):
    class Meta:
        model = arqueo_caja
        fields = ('__all__')



class form_bus(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))
    fecha_fact = forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}))


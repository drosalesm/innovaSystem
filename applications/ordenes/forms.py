from django import forms
from .models import  *
from crispy_forms.helper import FormHelper
from applications.vendedores.models import *
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, ButtonHolder

class examenesForm(forms.ModelForm):
    class Meta:
        model = ordenes
        fields = ('__all__')


class exam_psicologicoForm(forms.ModelForm):
    class Meta:
        model = examen_psi
        fields = ('__all__')


class facturaForm(forms.ModelForm):
    class Meta:
        model = facturaFiscal
        fields = ('__all__')
   


class listado_clientes(forms.Form):
    search=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control busqCliente',
        'placeholder':'Busqueda de clientes'
    }),required=False)

class busqueda_fact(forms.Form):
    fact=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control busqCliente',
        'placeholder':'Busqueda de facturas'
    }),required=False)


class listado_ordenes(forms.Form):
    search_ord=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Busqueda de ordenes'
    }),required=False)

class isv_form(forms.Form):
    isv_value = forms.ModelChoiceField(required=False,queryset=ordenes.objects.filter(pk=3).values_list('impuesto_orden'))    


class headFactForm(forms.ModelForm):
    class Meta:
        model = encabezadoFactura
        fields = ('__all__')

class detFactForm(forms.ModelForm):
    class Meta:
        model = detalleFactura
        fields = ('__all__')


class vend_form(forms.Form):
    vendedor = forms.ModelChoiceField(queryset=vendedores.objects.filter(t_empleado=5).values_list('nombre', flat=True).distinct(),
                                        widget=forms.Select(attrs={'class': 'form-control','label':'Hola'}),required=False)

class doctor_form(forms.Form):
    vendedor = forms.ModelChoiceField(queryset=vendedores.objects.filter(t_empleado=0).values_list('nombre', flat=True).distinct(),
                                        widget=forms.Select(attrs={'class': 'form-control','label':'Hola'}),required=False)
 
class psicologo_form(forms.Form):
    vendedor = forms.ModelChoiceField(queryset=vendedores.objects.filter(t_empleado=1).values_list('nombre', flat=True).distinct(),
                                        widget=forms.Select(attrs={'class': 'form-control','label':'Hola'}),required=False)

class productos_form(forms.Form):
    producto = forms.ModelChoiceField(queryset=ordenes.objects.values_list('nombre_orden', flat=True).distinct(),
                                        widget=forms.Select(attrs={'class': 'form-control','label':'orden'}),required=False)



class tpForm(forms.Form):
      tipo_pago = forms.ChoiceField(
               choices = (
                          ('1',"Efectivo"),
                          ('2',"Tarjeta Visa"),
                          ('3',"Tarjeta MasterCard"),     
                          ),
               widget = forms.Select(attrs={'class': 'form-control'}),required=False)


class form_adelantos(forms.ModelForm):

    vendedor = forms.ModelChoiceField(queryset=vendedores.objects.filter(t_empleado=5).all(),required=False)
    proveedor = forms.ModelChoiceField(queryset=proveedores.objects.all(),required=False)
    class Meta:
        model = adelantos
        fields = ['tipo_adelanto', 'cantidad', 'tipo_solicitante', 'solicitante', 'fecha_solicitud']


class provForm(forms.ModelForm):
    class Meta:
        model = proveedores
        fields = ('__all__')

        widgets={
        'nombre':forms.TextInput(attrs={'class':'form-control'}),
        'fecha_ingreso':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        }
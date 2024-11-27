from xml.dom.minidom import Attr
from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class vendedoresForm(forms.ModelForm):
    class Meta:                                                          
        model = vendedores             
        fields = ('__all__')
        widgets={
        'nombre':forms.TextInput(attrs={'class':'textinput textInput form-control'}),
        'identidad':forms.TextInput(attrs={'class':'textinput textInput form-control'}),
        'telefono':forms.TextInput(attrs={'class':'textinput textInput form-control'}),
        'correo':forms.TextInput(attrs={'class':'textinput textInput form-control'}),
        'direccion':forms.TextInput(attrs={'class':'textinput textInput form-control'}),
        'fecha_ingreso':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'estado':forms.TextInput(attrs={'class':'textinput textInput form-control'}),        
        'doc_profesional':forms.TextInput(attrs={'class':'textinput textInput form-control'}),        
        }
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(vendedoresForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['estado'].required = False
        self.fields['doc_profesional'].required = False
        self.fields['correo'].required = False
        self.fields['direccion'].required = False

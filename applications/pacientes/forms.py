from django import forms
from .models import Pacientes

class pacientesForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ('__all__')
        telefono = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control','label':'Hola'}),required=False)


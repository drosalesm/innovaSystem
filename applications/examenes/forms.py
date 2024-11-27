from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class exMedico_Form(forms.ModelForm):
    class Meta:
        model = examen_med
        fields = ('__all__')

        widgets={
        'fecha':forms.DateInput(attrs={'class':'form-control'}),
        'i_card':forms.TextInput(attrs={'class':'form-control'}),
        't_rit':forms.TextInput(attrs={'class':'form-control'}),
        'm_desf':forms.TextInput(attrs={'class':'form-control'}),        
        'p_val':forms.TextInput(attrs={'class':'form-control'})
        }

class exPsico_Form(forms.ModelForm):
    class Meta:
        model = examen_psi
        fields = ('__all__')

        widgets={
        'fecha':forms.DateInput(attrs={'class':'form-control'})
        }




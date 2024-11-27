from tkinter import Widget
from django import forms

from applications.usuarios_inova.models import User
from .models import *
from crispy_forms.helper import FormHelper

class sucursalesForm(forms.ModelForm):
    class Meta:
        model = sucursales
        fields = ('__all__')


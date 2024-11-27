from django import forms
from .models import *
from crispy_forms.helper import FormHelper


class FormUser(forms.ModelForm):
    class Meta:
        model=User
        fields='__all__'
        Widget={
            'rol':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Rol de Usuario'
                }
            ),
            'username':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre de Usuario'
                }
            ),
            'email':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo Electronico'
                }
            )
        }

    def save(self, commit=True):
        user = super(FormUser, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
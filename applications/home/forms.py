from django import forms
from django.apps import apps


class CargarDatosCSVForm(forms.Form):
    archivo_csv = forms.FileField(label='archivo_csv')



class SeleccionarModeloForm(forms.Form):
    modelos = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(SeleccionarModeloForm, self).__init__(*args, **kwargs)
        self.fields['modelos'].choices = self.obtener_opciones_modelos()

    def obtener_opciones_modelos(self):
        opciones = []
        for app_config in apps.get_app_configs():
            for modelo in app_config.get_models():
                opciones.append((f"{modelo.__module__.split('.')[-2]}.{modelo.__name__}", f"{modelo.__module__.split('.')[-2]} - {modelo.__name__}"))


        return opciones
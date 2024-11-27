
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import template
from applications.usuarios_inova.views import *
from .forms import *
from django.http import HttpResponse
import io, csv


# Create your views here.

@login_required
def indexPage(request):
    user=request.user
    print(user)
    return render(request,'home/inicio.html')


@login_required
def indexPage(request):
    user=request.user
    rol=request.user.rol
    print(user,rol)
    usuario_log.objects.update(usuario=str(user))
    usuario_log.objects.update(rol=rol)
    return render(request,'home/inicio.html')


def cargaDataModels(request):
    formCarga=CargarDatosCSVForm()
    if request.method == 'POST':
        form = SeleccionarModeloForm(request.POST)
        if form.is_valid():
            csv_file = request.FILES['archivo_csv']
            # Verificar que el archivo es un archivo CSV
            if not csv_file.name.endswith('.csv'):
                return HttpResponse('Por favor, suba un archivo CSV.')


       # Leer el archivo CSV
            data_set = csv_file.read().decode('latin-1')
            io_string = io.StringIO(data_set)

            csv_reader = csv.reader(io_string, delimiter=';', quotechar='"')

            primera_fila = next(csv_reader)
            num_columnas_csv = len(primera_fila)
#            next(io_string)  # Para omitir la primera fila si contiene encabezados

            modelo_seleccionado_nombre = form.cleaned_data['modelos']
#            app_label = modelo_seleccionado_nombre.split('.')[0]        
            modelo_seleccionado_clase = apps.get_model(modelo_seleccionado_nombre)            
            campos_modelo = modelo_seleccionado_clase._meta.get_fields()            
            nombres_campos = [campo.name for campo in campos_modelo if campo.name != 'id']

            if num_columnas_csv != len(nombres_campos):
                return HttpResponse(f'El número de columnas en el archivo CSV ({num_columnas_csv}) no coincide con el número de campos en el modelo seleccionado ({modelo_seleccionado_nombre}).')


            #Guardar data en modelo seleccionado
            for row in csv_reader:
                instancia_modelo = modelo_seleccionado_clase()
                for idx, valor_campo in enumerate(row):
                    
                    nombre_campo = modelo_seleccionado_clase._meta.fields[idx+1].name

                    if nombre_campo != 'id':
                        setattr(instancia_modelo, nombre_campo, valor_campo)
#                        print('Validando valores:',idx,valor_campo,nombre_campo)                    
                try:
                    instancia_modelo.save()
                except Exception as e: 
                    return HttpResponse(f'Se presento el siguiente error ({e}).')

            return render(request, 'home/cargar_datos_csv.html',{'form': form,'formCarga':formCarga})
    else:
        form = SeleccionarModeloForm()
    return render(request, 'home/cargar_datos_csv.html', {'form': form,'formCarga':formCarga})

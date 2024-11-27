from django.contrib import admin
from .models import *
from applications.home.utils import exportar_a_csv
# Register your models here.



class OrdenesEmitidasAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ordenes_emitidas._meta.fields]  
    list_display_links = ['id']  # Vincula el campo 'id' en la lista de instancias


class adelatosAdmin(admin.ModelAdmin):
    list_display = [field.name for field in adelantos._meta.fields]  
    actions=[exportar_a_csv]

class proveedoresAdmin(admin.ModelAdmin):
    list_display = [field.name for field in proveedores._meta.fields]  
    actions=[exportar_a_csv]

class ordenesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ordenes._meta.fields]  
    actions=[exportar_a_csv]


admin.site.register(proveedores,proveedoresAdmin)
admin.site.register(adelantos,adelatosAdmin)
admin.site.register(ordenes_emitidas,OrdenesEmitidasAdmin)
admin.site.register(encabezadoFactura)
admin.site.register(ordenes,ordenesAdmin)


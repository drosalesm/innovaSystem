from django.contrib import admin
from applications.facturacion.models import *
from applications.home.utils import exportar_a_csv
# Register your models here.

class invAdmin(admin.ModelAdmin):
    list_display = [field.name for field in inventProd._meta.fields]  
    actions=[exportar_a_csv]

admin.site.register(info_facturas)
admin.site.register(inventProd,invAdmin)
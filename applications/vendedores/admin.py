from django.contrib import admin
from applications.vendedores.models import *
from applications.home.utils import exportar_a_csv


class vendedoresAdmin(admin.ModelAdmin):
    list_display = [field.name for field in vendedores._meta.fields]  
    actions=[exportar_a_csv]

admin.site.register(vendedores,vendedoresAdmin)



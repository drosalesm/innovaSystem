from django.contrib import admin
from applications.sucursales.models import *
from applications.home.utils import exportar_a_csv
# Register your models here.




class sucursalesAdmin(admin.ModelAdmin):
    actions = [exportar_a_csv]
    list_display = [field.name for field in sucursales._meta.fields]  


admin.site.register(sucursales,sucursalesAdmin)




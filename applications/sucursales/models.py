from operator import truediv
from django.db import models

# Create your models here.
class sucursales(models.Model):

    nombre_sucursal = models.CharField(max_length=100,verbose_name="Sucursal")
    direccion = models.CharField(max_length=500,verbose_name="Direccion",null=True)
    rtn = models.CharField(max_length=100,verbose_name="RTN",null=True)
    telefono = models.CharField(max_length=100,verbose_name="Telefono",null=True)
    correo =models.EmailField(null=True,blank=True)
    def __str__(self):
        return self.nombre_sucursal
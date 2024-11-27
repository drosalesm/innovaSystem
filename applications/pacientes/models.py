from django.db import models
from django.forms import model_to_dict

# Create your models here.
class Pacientes(models.Model):
    nombre = models.CharField(max_length=100,verbose_name="Nombre paciente")
    identidad = models.CharField(max_length=100,verbose_name="Identidad",unique=True)
    telefono = models.CharField(max_length=8,verbose_name="Numero de telefono")
    direccion = models.CharField(max_length=500, verbose_name="Direccion del paciente") 
    foto = models.ImageField(null=True,blank=True,verbose_name="Foto")
    huella = models.ImageField(null=True,blank=True,verbose_name="huella")
    firma = models.ImageField(null=True,blank=True,verbose_name="firma")
    correo=models.EmailField(null=True,blank=True)
    fecha_registro=models.DateField(null=True,blank=True)

    def __str__(self):
        return self.nombre

    #El metodo exclude no puede convertir ciertos valores como imagenes y fechas
    def toJSON(self):
        items=model_to_dict(self,exclude=['foto','firma','huella'])
        return items


class pacOpciones(models.Model):
    opcion = models.CharField(max_length=100, verbose_name="opciones")
    descripcion = models.CharField(max_length=500, verbose_name="Descripcion opciones") 

    def __str__(self):
        return self.opcion
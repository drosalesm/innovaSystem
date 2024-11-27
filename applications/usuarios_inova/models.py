from django.db import models
from django.forms import CharField
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from applications.sucursales.models import sucursales


TIPOEMPLEADO_CHOICES=(
    ('0','Doctor'),
    ('1','Psicologo'),    
    ('2','Secretario'),
    ('4','Administrador'),
    ('5','Vendedor'),    
    ('6','Usuario Regular'),    
)

# Create your models here.
class User(AbstractUser):
    rol=models.CharField(max_length=200,verbose_name="Tipo de Empleado",null=True,choices=TIPOEMPLEADO_CHOICES)
    sucursal=models.CharField(max_length=50,null=True,blank=True, verbose_name="Sucursal")
     
#Clase para visualizar el usuario logeado 
class usuario_log(models.Model):
      usuario = models.CharField(max_length=100)
      rol=models.IntegerField()
      class Meta:
            managed = False
            db_table = 'usuario_actual'
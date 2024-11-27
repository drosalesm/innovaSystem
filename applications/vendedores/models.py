from django.db import models
from django.forms import model_to_dict



TIPOEMPLEADO_CHOICES=(
    ('0','Doctor'),
    ('1','Psicologo'),    
    ('2','Secretario'),
    ('4','Administrador'),
    ('5','Vendedor'),    
)

# Create your models here.
class vendedores(models.Model):
    nombre = models.CharField(max_length=100,null=True)
    identidad = models.CharField(max_length=100,verbose_name="Descripcion",null=True)
    telefono=models.CharField(max_length=12,verbose_name="Telefono",null=True)
    correo=models.EmailField(null=True)
    direccion=models.CharField(max_length=500,null=True)
    fecha_ingreso = models.DateField(null=True)
    estado=models.CharField(max_length=50,null=True,default="Activo")
    doc_profesional=models.CharField(max_length=50,null=True,verbose_name="Colegiacion")
    t_empleado=models.CharField(max_length=200,verbose_name="Tipo de Empleado",null=True,choices=TIPOEMPLEADO_CHOICES)


    def __str__(self):
        return self.nombre

    def toJSON(self):
        items=model_to_dict(self)
        return items

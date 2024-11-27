from operator import truediv
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import model_to_dict


EXAMENES_CHOICES=(
    ('0','Evaluacion Medica'),
    ('1','Evaluacion Psicologica'),    
    ('3','Evaluacion Completa'),    
)

EMPLEADOS_CHOICES=(
    ('0','Medico'),
    ('1','Psicologo'),    
    ('2','Admin'),
)

CAT_PSI_CHOICES=(
    ('0','ITEMS DELIRIUM'),
    ('1','Ítems a evaluar Demencia'),    
    ('2','Ítems para evaluar trastornos amnésicos y trastornos cognitivos'),
    ('3','Ítems para evaluar trastornos mentales debido a enfermedades medicas no clasificadas'),
    ('4','Ítems para evaluar esquizofrenia y otros trastornos psicóticos'),
    ('5','Ítems para evaluar trastornos del estado de animo'),    
    ('6','Ítems para evaluar trastornos disociativos'),
    ('7','Ítems para evaluar trastornos del sueño de origen diferente al respiratorio'),    
    ('8','Ítems para evaluar trastornos del control de impulsos'),
    ('9','Ítems para evaluar trastornos de la personalidad'),    
    ('10',' Ítems para evaluar trastorno del desarrollo intelectual'),
    ('11','Ítems para evaluar trastornos por déficit de atención'),
    ('12','Ítems para evaluar comportamiento perturbador'),
)

T_ADELANTO_CHOICES=(
    ('0','Parcial'),
    ('1','Completo'), 
)

T_SOLICITANTE=(
    ('0','Colaborador'),
    ('1','Empresa'), 
)


class examen_psi(models.Model):
    pregunta=models.CharField(max_length=500,verbose_name="Ingrese la pregunta")
    tipo_pregunta=models.CharField(max_length=10,verbose_name="Tipo de pregunta",choices=CAT_PSI_CHOICES)
    medicion_si=models.FloatField(verbose_name="Puntaje")
    medicion_no=models.FloatField(verbose_name="Puntaje")
    def __str__(self):
        return self.pregunta


class ordenes(models.Model):
    cod_ord = models.CharField(max_length=100, verbose_name="Codigo de Orden")
    nombre_orden = models.CharField(max_length=100,verbose_name="Nombre de la Orden")
    descripcion_orden = models.CharField(max_length=100,verbose_name="Descripcion")
    precio_orden = models.FloatField(verbose_name="Precio")
    impuesto_orden = models.IntegerField(verbose_name="ISV")
    encargado_orden=models.CharField(max_length=100,verbose_name="Encargado",null=True,choices=EMPLEADOS_CHOICES)
    formulario=models.CharField(max_length=50,verbose_name="Formuarlio a Usar", null =True,choices=EXAMENES_CHOICES)
    def __str__(self):
        return self.nombre_orden

    def toJSON(self):
        items=model_to_dict(self)
        return items


class ordenes_emitidas(models.Model):
    cod_ord = models.CharField(max_length=100, verbose_name="Codigo de Orden")
    nombre_orden = models.CharField(max_length=100,verbose_name="Nombre de la Orden")
    encargado_orden=models.CharField(max_length=100,verbose_name="Encargado",null=True,choices=EMPLEADOS_CHOICES)
    estado=models.CharField(max_length=20,verbose_name="Estado orden")
    fecha_emision=models.DateField(null=True)
    fecha_cierre=models.DateTimeField(null=True)
    paciente=models.CharField(max_length=100,verbose_name="Encargado",null=True)
    resultado=models.CharField(max_length=100,verbose_name="Encargado",null=True)
    formulario=models.CharField(max_length=50,verbose_name="Formuarlio a Usar", null =True,choices=EXAMENES_CHOICES)
    dir_pac=models.CharField(max_length=500,verbose_name="Direccion",null=True)
    identif_pac=models.CharField(max_length=500,verbose_name="Identificacion",null=True)
    resultado=models.CharField(max_length=100,verbose_name="Resultado",null=True)
    def __str__(self):
        return self.nombre_orden

    def toJSON(self):
        items=model_to_dict(self)
        return items



class detalle_inv(models.Model):
      inventprod_id = models.IntegerField()
      ordenes_id = models.IntegerField()

      class Meta:
            managed = False
            db_table = 'facturacion_inventprod_orden_asociada'



class exaOpciones(models.Model):
    opcion = models.CharField(max_length=100, verbose_name="opciones")
    descripcion = models.CharField(max_length=500, verbose_name="Descripcion opciones") 

    def __str__(self):
        return self.opcion



class plant_variable(models.Model):
    codigo_examen = models.CharField(max_length=100, verbose_name="Codigo del Examen")
    nombre_examen = models.CharField(max_length=100,verbose_name="Nombre del Examen")
    descripcion_examen = models.CharField(max_length=100,verbose_name="Descripcion")

    def __str__(self):
        return self.nombre_examen


#FACTURACION

class facturaFiscal(models.Model):
    numero_factura=models.CharField(max_length=100,verbose_name="Numero de Factura")


class encabezadoFactura(models.Model):
    fecha_factura =models.CharField(max_length=20,verbose_name="Fecha")
    nombre = models.CharField(max_length=100,verbose_name="Nombre paciente")
    identidad = models.CharField(max_length=100,verbose_name="Identidad")
    telefono = models.CharField(max_length=8, verbose_name="Numero de telefono")
    direccion = models.CharField(max_length=500, verbose_name="Direccion del paciente") 
    vendedor=models.CharField(max_length=100,verbose_name='Vendedor',null=True)
    factura = models.CharField(max_length=100,verbose_name="Numero de factura")
    sub_total =models.CharField(max_length=100,verbose_name="SubTotal")
    total_factura =models.FloatField()
    descuento=models.FloatField()
    impuesto=models.FloatField()
    tipo_pago=models.CharField(max_length=100,verbose_name="Tipo de Pago",null=True)

    def __str__(self):
        return self.nombre


class detalleFactura(models.Model):
    fecha_factura =models.CharField(max_length=20,verbose_name="Fecha")
    factura = models.CharField(max_length=100,verbose_name="Numero de factura")
    cod_ord = models.CharField(max_length=100, verbose_name="Codigo de Orden")
    nombre = models.CharField(max_length=100,verbose_name="Nombre de la Orden")
    descripcion = models.CharField(max_length=100,verbose_name="Descripcion")
    precio = models.FloatField(verbose_name="Precio")
    cantidad=models.IntegerField()
    sub_total=models.FloatField()

    def __str__(self):
        return self.nombre


class facturas_formated(models.Model):
    fecha_factura =models.DateField()
    nombre = models.CharField(max_length=100,verbose_name="Nombre paciente")
    identidad = models.CharField(max_length=100,verbose_name="Identidad")
    telefono = models.CharField(max_length=8, verbose_name="Numero de telefono")
    direccion = models.CharField(max_length=500, verbose_name="Direccion del paciente") 
    vendedor=models.CharField(max_length=100,verbose_name='Vendedor',null=True)
    factura = models.CharField(max_length=100,verbose_name="Numero de factura")
    sub_total =models.CharField(max_length=100,verbose_name="SubTotal")
    total_factura =models.FloatField()
    descuento=models.FloatField()
    impuesto=models.FloatField()
    tipo_pago=models.CharField(max_length=100,verbose_name="Tipo de Pago",null=True)

    class Meta:
            managed = False
            db_table = 'FACTURAS_FORMATED'


class adelantos(models.Model):
    tipo_adelanto=models.CharField(max_length=50,verbose_name='Tipo de Adelanto',choices=T_ADELANTO_CHOICES)
    cantidad = models.FloatField()
    tipo_solicitante=models.CharField(max_length=100,verbose_name='Tipo de Solicitante',choices=T_SOLICITANTE)
    solicitante=models.CharField(max_length=500,verbose_name='Solicitante')
    fecha_solicitud=models.DateField()

    def __str__(self):
        return self.solicitante


class proveedores(models.Model):
    nombre=models.CharField(max_length=100,verbose_name='Proveedor',null=True)
    fecha_ingreso=models.DateField()
    def __str__(self):
        return self.nombre



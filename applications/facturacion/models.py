from tkinter import CASCADE
from django.db import models
from django.forms import IntegerField
from applications.ordenes.models import ordenes

# Create your models here.

class info_facturas(models.Model):
    fecha_lim_em = models.CharField(max_length=10, verbose_name="DD-MM-YYYY", null=True)
    numeracion = models.CharField(max_length=100, verbose_name="Numeracion Inicial Factura", null=True)
    rango_inicial = models.IntegerField(verbose_name="Rango Inicial Autorizado")
    rango_final = models.IntegerField(verbose_name="Rango Final Autorizado")
    fac_actual = models.IntegerField(verbose_name="Siguiente Factura")
    isv =models.IntegerField(verbose_name="Impuesto a cobrar", null=True)
    sucursal=models.CharField(max_length=500,verbose_name='Sucursal',null=True)
    cai =models.CharField(max_length=500,verbose_name='numero cai',null=True)
    def __str__(self):
        return str(self.fac_actual)


class inventProd(models.Model):
    producto = models.CharField(max_length=100,verbose_name="Producto")
    descripcion = models.CharField(max_length=100,verbose_name="Descripcion Producto")
    cantidad_inv =models.PositiveIntegerField(verbose_name="Cantidad en Inventario")
    precio=models.FloatField(verbose_name="Lps")
    orden_asociada=models.ManyToManyField(ordenes)


class REPORTE_VENTAS(models.Model):
      id=IntegerField()
      fecha_factura = models.DateField()
      vendedor = models.CharField(max_length=100)
      monto_venta = models.FloatField(max_length=100)
      conteo=models.IntegerField()
      class Meta:
            managed = False
            db_table = 'reporte_ventas'



class REPORTE_FACT(models.Model):
      id=IntegerField()
      fecha_factura = models.DateField()
      nombre = models.CharField(max_length=100)
      factura = models.CharField(max_length=100)
      sub_total = models.FloatField(max_length=100)
      descuento = models.FloatField(max_length=100)
      impuesto = models.FloatField(max_length=100)
      total_factura = models.FloatField(max_length=100)
      vendedor=models.CharField( max_length=250)
      identidad=models.CharField(max_length=100)
      tipo_pago=models.IntegerField()

      class Meta:
            managed = False
            db_table = 'reporte_fact'

class REPORTE_PROD(models.Model):
      id=IntegerField()
      fecha_factura = models.DateField()
      nombre = models.CharField(max_length=200)
      total_facturado = models.FloatField()
      total_ordenes = models.IntegerField()

      class Meta:
            managed = False
            db_table = 'reporte_productos'

class cierre_diario_vend(models.Model):
    fecha_factura =models.DateField()
    vendedor=models.CharField(max_length=100,verbose_name='Vendedor',null=True)
    monto_venta=models.FloatField()
    total_facturas=models.PositiveIntegerField()
    monto_adelanto=models.FloatField()
    adelantos=models.PositiveIntegerField()
    total_pago=models.FloatField()

    class Meta:
            managed = False
            db_table = 'cierre_diario_vend'


class cierre_diario_tot_vent(models.Model):
    fecha_factura =models.DateField()
    total_ventas=models.FloatField()

    class Meta:
            managed = False
            db_table = 'rep_total_ventas'


class cierre_diario_tot_prod(models.Model):
    fecha_factura =models.DateField()
    nombre =models.CharField(max_length=150,verbose_name='Productos')
    total_facturado=models.FloatField()
    total_ordenes=models.IntegerField()

    class Meta:
            managed = False
            db_table = 'reporte_productos'


class cierre_diario_tot_mp(models.Model):
    fecha_factura =models.DateField()
    tipo_pago =models.CharField(max_length=150,verbose_name='Productos')
    total_ventas=models.FloatField()
    cantidad_fact=models.IntegerField()

    class Meta:
            managed = False
            db_table = 'rep_metodo_pago'



class arqueo_caja(models.Model):
    T_BILLETE=(
        ('1',1),
        ('2',2), 
        ('5',5),
        ('10',10),         
        ('20',20), 
        ('50',50),
        ('100',100),                 
        ('200',200),
        ('500',500),                 
    )

    fecha_registro =models.DateField(null=True)
    billete =models.CharField(max_length=3,choices=T_BILLETE,null=True)
    cantidad=models.PositiveIntegerField(null=True)
    def __str__(self):
        return self.billete

    @property
    def total(self):
        return int(self.billete) * self.cantidad



class rep_arqueo_caja(models.Model):
    fecha_registro =models.DateField()
    billete =models.CharField(max_length=5,verbose_name='Billete')
    cantidad=models.IntegerField()
    monto_total=models.IntegerField()

    class Meta:
            managed = False
            db_table = 'resumen_arqueo_caja'


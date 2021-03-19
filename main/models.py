# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class divisional(models.Model):
    nombre = models.CharField(max_length=30)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class estado(models.Model):
    nombre = models.CharField(max_length=30)
    divisional =  models.ForeignKey(divisional, on_delete=models.CASCADE)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class ciudad(models.Model):
    nombre = models.CharField(max_length=30)
    estado =  models.ForeignKey(estado, on_delete=models.CASCADE)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre
	
class central(models.Model):
    nombre = models.CharField(max_length=30)
    ciudad =  models.ForeignKey(ciudad, on_delete=models.CASCADE)
    direccion = models.TextField(blank=True, null=True)
    localizacion = models.TextField(blank=True, null=True)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class cluster_ce(models.Model):
    nombre = models.CharField(max_length=30)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre	

class modelo_equipo(models.Model):
    nombre = models.CharField(max_length=150)
    tecnologia = models.CharField(max_length=20)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

	
class equipo(models.Model):
    clli = models.CharField(max_length=25)
    ip_lb0 = models.CharField(max_length=15)
    ip_lb1 = models.CharField(max_length=15)
    cluster = models.ForeignKey(cluster_ce, on_delete=models.CASCADE)
    central = models.ForeignKey(central, on_delete=models.CASCADE)
    unit = models.CharField(max_length=6)
    avm = models.IntegerField()
    modelo_equipo = models.ForeignKey(modelo_equipo, on_delete=models.CASCADE)
    sofware_version = models.CharField(max_length=15)
    status = models.CharField(max_length=10,default="Active")

    #def get_absolute_url(self):
    #	return reverse('inventario:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

class casos(models.Model):
    sr = models.BigIntegerField()
    cobo = models.CharField(max_length=100,null=True)
    fecha = models.CharField(max_length=40,null=True)
    mes = models.CharField(max_length=8,null=True)
    anio = models.IntegerField(null=True)
    clli = models.CharField(max_length=25,null=True)
    ing_telmex = models.CharField(max_length=60,null=True)
    ing_cisco = models.CharField(max_length=60,null=True)
    problema = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    responsable = models.CharField(max_length=20,null=True)
    codigo_cierre = models.CharField(max_length=100,null=True)
    subtipo = models.CharField(max_length=40,null=True)
    detalle_subtipo = models.CharField(max_length=40,null=True)
    tecnologia = models.CharField(max_length=20,null=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class inventario(models.Model):
    id = models.IntegerField(primary_key=True)
    divisional = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    ccentral = models.CharField(max_length=30)
    cluster_ce = models.CharField(max_length=30)
    hostname = models.CharField(max_length=25)
    ip_lb0 = models.CharField(max_length=15)
    casos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventario'

class limpiezas(models.Model):
    clli = models.CharField(max_length=25)
    fecha = models.CharField(max_length=40)
    observacion = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id)
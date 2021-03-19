# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from main import models as principal

# Create your models here.

class cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(blank=True, null=True)
    localizacion = models.TextField(blank=True, null=True)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class dir_divisional(models.Model):
    nombre = models.CharField(max_length=40)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class area_divisional(models.Model):
    nombre = models.CharField(max_length=40)
    dir_divisional = models.ForeignKey(dir_divisional, on_delete=models.CASCADE)

	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class network_partition(models.Model):
    nombre = models.CharField(max_length=40)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre

class sub_network(models.Model):
    nombre = models.CharField(max_length=40)
    network_partition = models.ForeignKey(network_partition, on_delete=models.CASCADE)
	
    def __str__(self):
        return str(self.id) + ' - ' + self.nombre



class equipo_optical(models.Model):
    clli = models.CharField(max_length=10)
    ip = models.CharField(max_length=15)
    ne_id = models.CharField(max_length=15,null=True)
    area_div = models.ForeignKey(area_divisional, on_delete=models.CASCADE)
    central = models.ForeignKey(principal.central, on_delete=models.CASCADE,null=True)
    cliente = models.ForeignKey(cliente, on_delete=models.CASCADE,null=True)
    modelo_equipo = models.ForeignKey(principal.modelo_equipo, on_delete=models.CASCADE,null=True)
    software_version = models.CharField(max_length=25,null=True)
    status = models.CharField(max_length=10,default="Active",null=True)
    sub_network= models.ForeignKey(sub_network, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id)

class inventario_opticos(models.Model):
    id = models.IntegerField(primary_key=True)
    clli = models.CharField(max_length=10)
    ip = models.CharField(max_length=15)
    ne_id = models.CharField(max_length=15)
    dir_divisional = models.CharField(max_length=30)
    area_divisional = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    ciudad = models.CharField(max_length=30)
    central = models.CharField(max_length=30)
    cliente = models.CharField(max_length=30)
    modelo_equipo = models.CharField(max_length=40)
    software_version = models.CharField(max_length=25)
    sub_network = models.CharField(max_length=40)
    network_partition = models.CharField(max_length=40)
    status = models.CharField(max_length=10)
    casos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventario_opticos'

class inventario_piezas_optica(models.Model):
    ne = models.CharField(max_length=15)
    id_ne = models.IntegerField(null=True)
    equipment_type = models.CharField(max_length=30)
    actual_equipment_type = models.CharField(max_length=90)
    physical_location = models.CharField(max_length=30)
    hw_part_number = models.CharField(max_length=30)
    sn = models.CharField(max_length=15)
    equipment_state = models.CharField(max_length=30)
    product_id = models.CharField(max_length=30)
    mes = models.IntegerField()
    anio = models.IntegerField()
    status = models.IntegerField()

    def __str__(self):
        return str(self.id)

class partes_optica(models.Model):
    product_id = models.CharField(max_length=25)
    product_desc = models.CharField(max_length=75)
    tecnology = models.CharField(max_length=10)
    platform = models.CharField(max_length=15)
    end_support = models.DateField()

    def __str__(self):
        return str(self.id)

class version_inventario(models.Model):
    mes = models.IntegerField()
    anio = models.IntegerField()

    def __str__(self):
        return str(self.id)
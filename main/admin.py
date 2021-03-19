# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import divisional, estado, ciudad, central, equipo, modelo_equipo
from optical.models import version_inventario

#Register your models here.
admin.site.register(divisional)
admin.site.register(estado)
admin.site.register(ciudad)
admin.site.register(central)
admin.site.register(equipo)
admin.site.register(modelo_equipo)
admin.site.register(version_inventario)

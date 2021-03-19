# -*- coding: utf-8 -*-
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.views import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.postgres.search import SearchVector
from django.db import connection
from main.models import equipo
from main.models import casos
from main.models import inventario
from main.models import limpiezas
from optical.models import partes_optica
from optical.models import inventario_opticos
from optical.models import equipo_optical
from optical.models import version_inventario
from optical.models import inventario_piezas_optica
from django.views.defaults import page_not_found
from django.contrib.auth.mixins import LoginRequiredMixin
#import datetime
#from datetime import *

import json
from django.http import HttpResponse

def mi_error_404(request):
    nombre_template = '404.html'

    if request.path.startswith('/ce'):
        nombre_template = 'app1_404.html'
    elif request.path.startswith('/optical'):
        nombre_template = 'app2_404.html'
    elif request.path.startswith('/main'):
        nombre_template = 'app3_404.html'
 
    return page_not_found(request, template_name=nombre_template)

class IndexView(LoginRequiredMixin,generic.ListView):
    template_name = 'main/index.html'

    def get_queryset(self):
        return equipo.objects.all()

    #@login_required
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
	context['eq_ce'] = inventario.objects.count()
	context['casos_ce'] = casos.objects.filter(tecnologia='CE').count()
	context['eq_op'] = inventario_opticos.objects.count()
	context['casos_op'] = casos.objects.filter(tecnologia='Optica').count()
	context['casos_resumen_ce'] = casos.objects.raw("select 1 as id, sum(q.sum) as sum, q.responsable from (select sum(1) as sum, TRIM(UPPER(responsable)) as responsable from main_casos where tecnologia = 'CE' group by responsable)q group by q.responsable;");
	context['casos_resumen_optica'] = casos.objects.raw("select 1 as id, sum(q.sum) as sum, q.responsable from (select sum(1) as sum, TRIM(UPPER(responsable)) as responsable from main_casos where tecnologia = 'Optica' group by responsable)q group by q.responsable;");
	context['casos_resumen_cisco_ce'] = casos.objects.raw("select 1 as id,sum(cont) as sum,codigo_cierre from (select SUM(1) as cont,translate(UPPER(codigo_cierre),'_',' ') as codigo_cierre from main_casos where TRIM(UPPER(responsable)) = 'CISCO' and tecnologia = 'CE' group by codigo_cierre)q group by codigo_cierre order by codigo_cierre;");
	context['casos_resumen_cisco_optica'] = casos.objects.raw("select 1 as id,sum(cont) as sum,codigo_cierre from (select SUM(1) as cont,translate(UPPER(codigo_cierre),'_',' ') as codigo_cierre from main_casos where TRIM(UPPER(responsable)) = 'CISCO' and tecnologia = 'Optica' group by codigo_cierre)q group by codigo_cierre order by codigo_cierre;");
	context['casos_resumen_telmex_ce'] = casos.objects.raw("select 1 as id,sum(cont) as sum,codigo_cierre from (select SUM(1) as cont,translate(UPPER(codigo_cierre),'_',' ') as codigo_cierre from main_casos where TRIM(UPPER(responsable)) = 'TELMEX' and tecnologia = 'CE' group by codigo_cierre)q group by codigo_cierre order by codigo_cierre;");
	context['casos_resumen_telmex_optica'] = casos.objects.raw("select 1 as id,sum(cont) as sum,codigo_cierre from (select SUM(1) as cont,translate(UPPER(codigo_cierre),'_',' ') as codigo_cierre from main_casos where TRIM(UPPER(responsable)) = 'TELMEX' and tecnologia = 'Optica' group by codigo_cierre)q group by codigo_cierre order by codigo_cierre;");
	context['inventario_ce'] = casos.objects.raw("select 1 as id,count(*),m.nombre from main_equipo e inner join main_modelo_equipo m on m.id = e.modelo_equipo_id where e.status = \'Active\' group by m.nombre order by count;");
	context['inventario_optica'] = casos.objects.raw("select 1 as id,count(*),m.nombre from optical_equipo_optical e inner join main_modelo_equipo m on m.id = e.modelo_equipo_id where e.status = \'Active\' group by m.nombre order by count;");
	return context


class Inventario(LoginRequiredMixin,generic.ListView):
    template_name = 'ce/inventario.html'

    def get_queryset(self):
        return equipo.objects.all()

    #def get_queryset(self):
    #    return inventario.objects.all().order_by('-casos')

    def get_context_data(self, *args, **kwargs):
        context = super(Inventario, self).get_context_data(**kwargs)
	context['resumen'] =  equipo.objects.raw("select 1 as id,casos,equipos,round ((equipos*100/total::decimal) ,2) as porc from (select casos, count(casos) as equipos, (select count(*) from inventario) as total from inventario group by casos order by equipos)res order by casos desc, equipos desc");
	context['inventario'] = inventario.objects.all().order_by('-casos')
	context['total'] = inventario.objects.count()
	return context

class Inventario2(LoginRequiredMixin,generic.ListView):
    template_name = 'ce/inventario2.html'

    def get_queryset(self):
        return equipo.objects.all()

    #def get_queryset(self):
    #    return inventario.objects.all().order_by('-casos')

    def get_context_data(self, *args, **kwargs):
        context = super(Inventario2, self).get_context_data(**kwargs)
	context['resumen'] =  equipo.objects.raw("select 1 as id,casos,equipos,round ((equipos*100/total::decimal) ,2) as porc from (select casos, count(casos) as equipos, (select count(*) from inventario) as total from inventario group by casos order by equipos)res order by casos desc, equipos desc");
	context['inventario'] = inventario.objects.all().order_by('-casos')
	context['total'] = inventario.objects.count()
	return context



class Inventario_Optico(LoginRequiredMixin,generic.ListView):
    template_name = 'optical/inventario_optico.html'

    def get_queryset(self):
        return equipo.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(Inventario_Optico, self).get_context_data(**kwargs)
	context['resumen'] =  equipo.objects.raw("select 1 as id,casos,equipos,round ((equipos*100/total::decimal) ,2) as porc from (select casos, count(casos) as equipos, (select count(*) from inventario_opticos) as total from inventario_opticos group by casos order by equipos)res order by casos desc, equipos desc");
	context['inventario'] = inventario_opticos.objects.all().order_by('-casos')
	context['total'] = inventario_opticos.objects.count()
	return context



class DetalleEquipo(generic.ListView):
    template_name = 'ce/detalle_equipo.html'

    def get_queryset(self):
        return equipo.objects.all()

    def get_queryset(self):
	equipo_id=self.kwargs['pk']

    def get_context_data(self, *args, **kwargs):
	equipo_id=self.kwargs['pk']
        context = super(DetalleEquipo, self).get_context_data(**kwargs)
	context['detalle'] =  equipo.objects.raw("select e.id,d.nombre as divisional,ed.nombre as estado,cd.nombre as ciudad,c.nombre as ccentral,c.direccion,c.localizacion,cl.nombre as cluster_ce,e.clli,e.ip_lb0,e.ip_lb1,e.unit,e.avm,e.sofware_version,me.nombre as modelo_equipoo from main_equipo e \
inner join main_central c on c.id = e.central_id \
inner join main_cluster_ce cl on cl.id = e.cluster_id \
inner join main_ciudad cd on cd.id = c.ciudad_id \
inner join main_estado ed on ed.id = cd.estado_id \
inner join main_divisional d on d.id = ed.divisional_id \
inner join main_modelo_equipo me on me.id = e.modelo_equipo_id \
where e.id=%s order by e.ip_lb0 asc;",[equipo_id])
	context['limpiezas'] = limpiezas.objects.raw("select 1 as id,lim.fecha,lim.observacion from main_equipo eq inner join main_limpiezas lim on lim.clli =eq.clli where eq.id = %s",[equipo_id])
	context['partes'] = "En construccion"
	return context

class HistoricoCasos(generic.ListView):
    template_name = 'ce/historico_casos.html'

    def get_queryset(self):
	equipo_id=self.kwargs['pk']

    def get_queryset(self):
        return casos.objects.all() 

    def get_context_data(self, *args, **kwargs):
	equipo_id=self.kwargs['pk']
	context = super(HistoricoCasos, self).get_context_data(*args, **kwargs)
	context['tabla'] = casos.objects.raw("select mc.id,mc.sr,mc.cobo,mc.fecha,mc.anio,mc.mes,mc.ing_telmex,mc.ing_cisco,mc.problema,mc.diagnostico,mc.responsable,mc.codigo_cierre,mc.subtipo,mc.detalle_subtipo,mc.observacion \
from main_casos mc inner join main_equipo me on me.clli = mc.clli \
where me.id = %s order by mc.sr",[equipo_id]) 
	context['tabla2'] = casos.objects.raw("select 1 as id,upper(trim(mc.responsable)) as responsable2,count(mc.responsable) as cantidad from main_casos mc inner join main_equipo eo on eo.clli = mc.clli where mc.tecnologia = 'CE' and eo.id = %s  group by responsable2",[equipo_id])
	context['tabla3'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join main_equipo eo on eo.clli = mc.clli where mc.tecnologia = 'CE' and eo.id = %s  group by codigo_cierre",[equipo_id])
	context['tabla4'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join main_equipo eo on eo.clli = mc.clli where mc.tecnologia = 'CE' and eo.id = %s and TRIM(UPPER(responsable)) = 'CISCO' group by codigo_cierre",[equipo_id])
	context['tabla5'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join main_equipo eo on eo.clli = mc.clli where mc.tecnologia = 'CE' and eo.id = %s and TRIM(UPPER(responsable)) = 'TELMEX' group by codigo_cierre",[equipo_id])

	return context

class HistoricoCasosOptica(generic.ListView):
    template_name = 'optical/historico_casos_optica.html'

    def get_queryset(self):
	equipo_id=self.kwargs['pk']

    def get_queryset(self):
        return casos.objects.all() 

    def get_context_data(self, *args, **kwargs):
	equipo_id=self.kwargs['pk']
	context = super(HistoricoCasosOptica, self).get_context_data(*args, **kwargs)
	context['tabla'] = casos.objects.raw("select mc.id,mc.sr,mc.cobo,mc.fecha,mc.anio,mc.mes,mc.ing_telmex,mc.ing_cisco,mc.problema,mc.diagnostico,mc.responsable,mc.codigo_cierre,mc.subtipo,mc.detalle_subtipo,mc.observacion \
from main_casos mc inner join optical_equipo_optical eo on eo.ne_id = mc.clli \
where eo.id = %s order by mc.sr",[equipo_id])
	context['tabla2'] = casos.objects.raw("select 1 as id,upper(trim(mc.responsable)) as responsable2,count(mc.responsable) as cantidad from main_casos mc inner join optical_equipo_optical eo on eo.ne_id = mc.clli where mc.tecnologia = 'Optica' and eo.id = %s  group by responsable2",[equipo_id])
	context['tabla3'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join optical_equipo_optical eo on eo.ne_id = mc.clli where mc.tecnologia = 'Optica' and eo.id = %s  group by codigo_cierre",[equipo_id])
	context['tabla4'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join optical_equipo_optical eo on eo.ne_id = mc.clli where mc.tecnologia = 'Optica' and eo.id = %s and TRIM(UPPER(responsable)) = 'CISCO' group by codigo_cierre",[equipo_id])
	context['tabla5'] = casos.objects.raw("select 1 as id,mc.codigo_cierre,count(mc.codigo_cierre) as cantidad from main_casos mc inner join optical_equipo_optical eo on eo.ne_id = mc.clli where mc.tecnologia = 'Optica' and eo.id = %s and TRIM(UPPER(responsable)) = 'TELMEX' group by codigo_cierre",[equipo_id])
	return context



class Busqueda(generic.ListView):
    template_name = 'ce/inventario.html'

    def get_queryset(self):
        return equipo.objects.all()

    def get_context_data(self, *args, **kwargs):
	q = self.request.GET.get('q') or '-created'
	context = super(Busqueda, self).get_context_data(**kwargs)
	context['resumen'] =  ""
	context['inventario'] = inventario.objects.annotate(search=SearchVector('divisional') + SearchVector('ccentral') + SearchVector('cluster_ce') + SearchVector('hostname') + SearchVector('ip_lb0')).filter(search=q).order_by('-casos')
	context['total'] = inventario.objects.annotate(search=SearchVector('divisional') + SearchVector('ccentral') + SearchVector('cluster_ce') + SearchVector('hostname') + SearchVector('ip_lb0')).filter(search=q).count()
	return context


class BusquedaOptical(generic.ListView):
    template_name = 'optical/inventario_optico.html'

    def get_queryset(self):
        return equipo.objects.all()

    def get_context_data(self, *args, **kwargs):
	q = self.request.GET.get('q') or '-created'
        context = super(BusquedaOptical, self).get_context_data(**kwargs)
	context['resumen'] =  ""
	context['inventario'] = inventario_opticos.objects.annotate(search=SearchVector('sub_network') + SearchVector('central') + SearchVector('cliente') + SearchVector('ne_id') + SearchVector('ip')).filter(search=q).order_by('-casos')
	context['total'] = inventario_opticos.objects.annotate(search=SearchVector('sub_network') + SearchVector('central') + SearchVector('cliente') + SearchVector('ne_id') + SearchVector('ip')).filter(search=q).count()
	return context


class DetalleEquipoOptico(generic.ListView):
    template_name = 'optical/detalle_equipo_optico.html'

    def get_queryset(self):
        return equipo.objects.all()

    def get_queryset(self):
	equipo_id=self.kwargs['pk']

    def get_context_data(self, *args, **kwargs):
	equipo_id=self.kwargs['pk']
        context = super(DetalleEquipoOptico, self).get_context_data(**kwargs)
	context['detalle'] =  equipo.objects.raw(" SELECT eo.id, eo.clli, eo.ip, eo.ne_id, \
        dd.nombre AS dir_divisional, \
        ad.nombre AS area_divisional, \
        e.nombre AS estado, \
        cd.nombre AS ciudad, \
        c.nombre AS ccentral, \
        c.direccion as dir_central, \
        c.localizacion as local_central, \
        cc.nombre AS cliente, \
        cc.direccion as dir_cliente, \
        cc.localizacion as local_cliente, \
        me.nombre AS modelo_equipo_optico, \
        eo.software_version, \
        sn.nombre AS sub_network, \
        np.nombre AS network_partition, \
        eo.status \
       FROM optical_equipo_optical eo \
         JOIN optical_area_divisional ad ON ad.id = eo.area_div_id \
         JOIN optical_dir_divisional dd ON dd.id = ad.dir_divisional_id \
         LEFT JOIN main_central c ON c.id = eo.central_id \
         LEFT JOIN optical_cliente cc ON cc.id = eo.cliente_id \
         LEFT JOIN main_ciudad cd ON cd.id = c.ciudad_id \
         LEFT JOIN main_estado e ON e.id = cd.estado_id \
         JOIN main_modelo_equipo me ON me.id = eo.modelo_equipo_id \
         JOIN optical_sub_network sn ON sn.id = eo.sub_network_id \
         JOIN optical_network_partition np ON np.id = sn.network_partition_id \
        where eo.id=%s order by eo.ip asc;",[equipo_id])
	for p in equipo.objects.raw("select id,mes,anio,max(mes+anio) from public.optical_inventario_piezas_optica where id_ne = %s group by id order by max asc;",[equipo_id]):
	    context['maximo'] = p.max
	    context['mes'] = p.mes
	    context['anio'] = p.anio
	context['partes'] = equipo.objects.raw("select id,equipment_type,actual_equipment_type,physical_location,hw_part_number,sn,equipment_state,product_id from public.optical_inventario_piezas_optica where id_ne = %s and (mes+anio)= %s order by physical_location;",[equipo_id,p.max])

	return context

class Soporte(TemplateView):
    template_name = 'main/soporte.html'

    def get_context_data(self, *args, **kwargs):
	context = super(Soporte, self).get_context_data(**kwargs)
	context['uno'] = "1"
	context['dos'] = "2"
	return context

class Busqueda_Avanzada_Optica(TemplateView):
    template_name = 'optical/busquedas.html'

    def get_context_data(self, *args, **kwargs):
	context = super(Busqueda_Avanzada_Optica, self).get_context_data(**kwargs)
        context['uno'] = "1"
        return context

class Busqueda_Partes_Optica(TemplateView):
    template_name= None

    def get(self, request):
        parte = self.request.GET.get("term", "")
        result_partes = partes_optica.objects.filter(product_id__icontains=parte)
        results = []
        for s in result_partes:
	  results.append(s.product_id)
        data = json.dumps(results)
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Busqueda_Nodo_Optica(TemplateView):
    template_name= None

    def get(self, request):
	nodo  = self.request.GET.get("term", "")
        result_partes = equipo_optical.objects.filter(ne_id__icontains=nodo)
        results = []
        for s in result_partes:
	  results.append(s.ne_id)
        data = json.dumps(results)
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Resultado_Partes_Optica(TemplateView):
    template_name= None

    def get(self, request):
        parte_id = self.request.GET.get("in_parte", "")
	####
	for p in version_inventario.objects.all():
	    mes = p.mes
	    anio = p.anio

	result = partes_optica.objects.raw("""select po.id,ad.nombre as area_div, \
	e.nombre as estado, \
	c.nombre as ciudad, \
	cc.nombre as central, \
	CAST( CASE when cc.nombre = 'Ambulancia' or cc.nombre = 'Bodega' then 1 else 0 end as bit), \
	ipo.ne as NE, \
	po.product_id as parte_optica \
	from optical_partes_optica po \
	inner join optical_inventario_piezas_optica ipo on (ipo.product_id = po.product_id or ipo.product_id = CONCAT(po.product_id,'=')) \
	inner join optical_equipo_optical eo on eo.id = ipo.id_ne \
	inner join main_central cc on cc.id = eo.central_id \
	inner join main_ciudad c on c.id = cc.ciudad_id \
	inner join main_estado e on e.id = c.estado_id \
	inner join optical_area_divisional ad on ad.id = eo.area_div_id \
	where po.product_id = (%s) and ipo.mes = (%s) and ipo.anio = (%s) order by bit DESC,cc.nombre ASC;""",[parte_id,mes,anio])

	#parte = self.request.POST["in_parte"]
        results = []
	results.append("<table class=\"table table-striped\">")
	results.append("<thead>")
	results.append("<tr><th id=\"col-2\"><a href=\"#\">Estado</a></th><th id=\"col-3\"><a href=\"#\">Ciudad</a></th><th id=\"col-3\"><a href=\"#\">Central</a></th><th id=\"col-2\"><a href=\"#\">NE</a></th><th id=\"col-2\"><a href=\"#\">Parte</a></th></tr>")
	results.append("</thead>")
	results.append("<tbody>")
        for s in result:
	  if s.central == 'Ambulancia':
	     central = "Ambulancia <img src=\"/static/images/ambulance.png\" width=\"18\" height=\"17\">"
	  elif s.central == 'Bodega':
	     central = "Bodega <img src=\"/static/images/depot.png\" width=\"18\" height=\"17\">"
	  else:
	    central = s.central
	  results.append("<tr>")
	  results.append("<td id=\"col-2\">"+s.estado+"</td><td id=\"col-3\">"+s.ciudad+"</td><td id=\"col-3\">"+central+"</td><td id=\"col-2\">"+s.ne+"</td><td id=\"col-2\">"+s.parte_optica+"</td>")
	  results.append("</tr>");
          #results.append(partes_json)
	results.append("</tbody>")
	results.append("</table>")
        #data = json.dumps(results)
        data = results
        #mimetype = 'application/json'
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Resultado_Partes_Optica_SN(TemplateView):
    template_name= None

    def get(self, request):
    #def get_context_data(self, *args, **kwargs):
        serial = self.request.GET.get("in_serial", "")
	context = super(Resultado_Partes_Optica_SN, self).get_context_data()
	for p in version_inventario.objects.all():
	    mes = p.mes
	    anio = p.anio

	result1 = partes_optica.objects.raw("""select po.id,ad.nombre as area_div, \
	e.nombre as estado, \
	c.nombre as ciudad, \
	cc.nombre as central, \
	ipo.ne as NE, \
	po.product_id as parte_optica \
	from optical_partes_optica po \
	inner join optical_inventario_piezas_optica ipo on (ipo.product_id = po.product_id or ipo.product_id = CONCAT(po.product_id,'=')) \
	inner join optical_equipo_optical eo on eo.ne_id = ipo.ne \
	inner join main_central cc on cc.id = eo.central_id \
	inner join main_ciudad c on c.id = cc.ciudad_id \
	inner join main_estado e on e.id = c.estado_id \
	inner join optical_area_divisional ad on ad.id = eo.area_div_id \
	where ipo.sn = (%s) and ipo.mes = (%s) and ipo.anio = (%s);""",[serial,mes,anio])
	
	

	#parte = self.request.POST["in_parte"]
        results1 = []
	results1.append("<table class=\"table table-striped\">")
	results1.append("<tr><th id=\"col-2\">Area Divisional</th><th id=\"col-1\">Estado</th><th id=\"col-2\">Ciudad</th><th id=\"col-2\">Central</th><th id=\"col-1\">NE</th><th id=\"col-2\">Parte</th></tr>")
        for s in result1:
	  results1.append("<tr><td id=\"col-2\">"+s.area_div+"</td><td id=\"col-1\">"+s.estado+"</td><td id=\"col-2\">"+s.ciudad+"</td><td id=\"col-2\">"+s.central+"</td><td id=\"col-1\">"+s.ne+"</td><td id=\"col-2\">"+s.parte_optica+"</td></tr>")
          #results.append(partes_json)
        results1.append("</table>")
        #data = json.dumps(results)

	data =  results1
        #mimetype = 'application/json'
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Resultado_Partes_Optica_nodo(TemplateView):
    template_name= None

    def get(self, request):
	import datetime
	#from datetime import datetime
        nodo = self.request.GET.get("in_nodo", "")

	today = datetime.datetime.now().strftime("%Y-%m-%d")
	#today = datetime.strptime('2019-05-23' , '%Y-%m-%d')
	#today = str(day)	
	#today = datetime.datetime.utcnow()
	#today = datetime.datetime(2019,5,23,0,0,0)
	
	for p in equipo.objects.raw("select id,mes,anio,max(mes+anio) from public.optical_inventario_piezas_optica where ne = %s group by id order by max asc;",[nodo]):
	    maximo = p.max
	    mes = p.mes
	    anio = p.anio
	result = equipo.objects.raw("select ipo.id,ipo.equipment_type,ipo.physical_location,ipo.hw_part_number,ipo.sn,ipo.equipment_state,ipo.product_id,po.end_support \
	from public.optical_inventario_piezas_optica ipo \
	left join public.optical_partes_optica po on po.product_id = ipo.product_id \
	where ipo.ne = %s and (ipo.mes+ipo.anio)= %s \
	order by  ipo.physical_location;",[nodo,p.max])

	resultado = []
	resultado.append("<h3>Partes del nodo</h3>")
	resultado.append("<table class=\"table table-striped\">")
	resultado.append("<thead>")
	resultado.append("<tr><th id=\"col-3\">Localizaci&oacute;n</th><th id=\"col-2\">SN</th><th id=\"col-6\">Estado</th><th id=\"col-3\">Parte</th><th id=\"col-4\">&nbsp;<th></tr>")
	resultado.append("</thead>")
	resultado.append("<tbody>")
	for s in result:
	  day = str(s.end_support)
	  #day = datetime.strptime(day , '%Y-%m-%d')
	  if day < today:
	    color = "red"
	  else:
	    color = "black"
	  if s.product_id != "":
	    resultado.append("<tr><td id=\"col-3\">"+s.physical_location+"</td><td id=\"col-2\">"+s.sn+"</td><td id=\"col-6\">"+s.equipment_state+"</td><td id=\"col-3\" style=\"color:"+color+"\">"+s.product_id+"</td><td id=\"col-4\"><img id=\"parteXnodo\" src=\"/static/images/xmag.png\" width=\"18\" height=\"17\" value=\""+s.product_id+"\"></td></tr>")
	  else:
	    resultado.append("<tr><td id=\"col-3\">"+s.physical_location+"</td><td id=\"col-2\">"+s.sn+"</td><td id=\"col-6\">"+s.equipment_state+"</td><td id=\"col-3\">"+s.product_id+"</td><td id=\"col-4\"></td></tr>")

	resultado.append("</tbody>")
	resultado.append("</table>")
	resultado.append("<label style=\"color:red\">*Fuera de Soporte</label>")

	data = resultado 
        #mimetype = 'application/json'
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Resultado_Partes_Optica_nodo_detalle(TemplateView):
    template_name= None

    def get(self, request):
	nodo = self.request.GET.get("in_nodo", "")
	results = []
	#context = super(DetalleEquipoOptico, self).get_context_data(**kwargs)

	for p in equipo.objects.raw(" SELECT eo.id, eo.clli, eo.ip, eo.ne_id, \
        dd.nombre AS dir_divisional, \
        ad.nombre AS area_divisional, \
        e.nombre AS estado, \
        cd.nombre AS ciudad, \
        c.nombre AS ccentral, \
        c.direccion as dir_central, \
        c.localizacion as local_central, \
        cc.nombre AS cliente, \
        cc.direccion as dir_cliente, \
        cc.localizacion as local_cliente, \
        me.nombre AS modelo_equipo_optico, \
        eo.software_version, \
        sn.nombre AS sub_network, \
        np.nombre AS network_partition, \
        eo.status \
       FROM optical_equipo_optical eo \
         JOIN optical_area_divisional ad ON ad.id = eo.area_div_id \
         JOIN optical_dir_divisional dd ON dd.id = ad.dir_divisional_id \
         LEFT JOIN main_central c ON c.id = eo.central_id \
         LEFT JOIN optical_cliente cc ON cc.id = eo.cliente_id \
         LEFT JOIN main_ciudad cd ON cd.id = c.ciudad_id \
         LEFT JOIN main_estado e ON e.id = cd.estado_id \
         JOIN main_modelo_equipo me ON me.id = eo.modelo_equipo_id \
         JOIN optical_sub_network sn ON sn.id = eo.sub_network_id \
         JOIN optical_network_partition np ON np.id = sn.network_partition_id \
        where eo.ne_id=%s order by eo.ip asc;",[nodo]):
	    dir_div = p.dir_divisional
	    are_div = p.area_divisional
	    estado = p.estado
	    ciudad = p.ciudad
	    central = str(p.ccentral)
	    if central == "None":
		central = ""
	    cliente = str(p.cliente)
	    if cliente == "None":
		cliente = ""
	results.append("<table>");
	results.append("<tr><td id=\"col-2\">Dir Divisional</td><td id=\"col-2\">"+dir_div+"</td><td id=\"col-2\">Area Divisional</td><td id=\"col-2\">"+are_div+"</td></tr>");
	results.append("<tr><td id=\"col-2\">Estado:</td><td id=\"col-2\">"+estado+"</td><td id=\"col-2\">Ciudad</td><td id=\"col-2\">"+ciudad+"</td></tr>");
	results.append("<tr><td id=\"col-2\">Central/Cliente</td><td colspan=\"2\">"+central+cliente+"</td></tr>");
	results.append("</table><br>");
	data = results
        #mimetype = 'application/json'
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Resultado_Partes_Optica_nodo_parte(TemplateView):
    template_name= None

    def get(self, request):
	parte_id = self.request.GET.get("in_parte", "")
	result = partes_optica.objects.raw("""select po.id,ipo.id as po_id,ad.nombre as area_div, \
	e.nombre as estado, \
	c.nombre as ciudad, \
	cc.nombre as central, \
	CAST( CASE when cc.nombre = 'Ambulancia' or cc.nombre = 'Bodega' then 1 else 0 end as bit), \
	ipo.ne as NE, \
	po.product_id as parte_optica \
	from optical_partes_optica po \
	inner join optical_inventario_piezas_optica ipo on (ipo.product_id = po.product_id or ipo.product_id = CONCAT(po.product_id,'=')) \
	inner join optical_equipo_optical eo on eo.id = ipo.id_ne \
	inner join main_central cc on cc.id = eo.central_id \
	inner join main_ciudad c on c.id = cc.ciudad_id \
	inner join main_estado e on e.id = c.estado_id \
	inner join optical_area_divisional ad on ad.id = eo.area_div_id \
	where po.product_id = (%s) order by bit DESC,cc.nombre ASC;""",[parte_id])

	#parte = self.request.POST["in_parte"]
        results = []

	results.append("<h3>Partes/Refacciones disponibles</h3>")
	results.append("<table class=\"table table-striped\">")
	results.append("<thead>")
	results.append("<tr><th id=\"col-3\">Estado</th><th id=\"col-3\">Ciudad</th><th id=\"col-3\">Central</th><th id=\"col-1\">NE</th><th id=\"col-4\">.</th></tr>")
	results.append("</thead>")
	results.append("<tbody>")
        for s in result:
	  if s.central == 'Ambulancia':
	     central = "Ambulancia <img src=\"/static/images/ambulance.png\" width=\"18\" height=\"17\">"
	  elif s.central == 'Bodega':
	     central = "Bodega <img src=\"/static/images/depot.png\" width=\"18\" height=\"17\">"
	  else:
	    central = s.central
	  results.append("<tr><td id=\"col-3\">"+s.estado+"</td><td id=\"col-3\">"+s.ciudad+"</td><td id=\"col-3\">"+central+"</td><td id=\"col-1\">"+s.ne+"</td><td id=\"col-4\"><a class=\"iframe2\" href=\""+str(s.po_id)+"/actualizar_inventario_parte_optica\" data-lightbox-title=\"Actualizar Inventario\" data-lightbox-description=\"xxxxx\" data-lightbox-iframe-scroll=\"true\"><img src=\"/static/images/edit.png\" width=\"18\" height=\"17\"></a></td></tr>")
          #results.append(partes_json)
	results.append("<tbody>")
        results.append("</table>")
        results.append("<script>")
        results.append("$(document).ready(function(){")
        results.append("$(\".iframe2\").colorbox({iframe:true, width:\"50%\", height:\"40%\",onClosed:reloadPage});")
	results.append("function reloadPage() { location.reload(true); }")
        results.append("});")
        results.append("</script>")

        #data = json.dumps(results)
        data = results
        #mimetype = 'application/json'
	mimetype = 'text/plain'
        return HttpResponse(data,mimetype)

class Lista_Refacciones_Optica(TemplateView):
    template_name = 'optical/lista_refacciones_optica.html'

    def get_context_data(self, *args, **kwargs):
	context = super(Lista_Refacciones_Optica, self).get_context_data(**kwargs)
	#context['resumen'] =  equipo.objects.raw("select 1 as id,casos,equipos,round ((equipos*100/total::decimal) ,2) as porc from (select casos, count(casos) as equipos, (select count(*) from inventario_opticos) as total from inventario_opticos group by casos order by equipos)res order by casos desc, equipos desc");
	context['inventario']= partes_optica.objects.raw("""select po.id,ad.nombre as area_div, \
	e.nombre as estado, \
	c.nombre as ciudad, \
	cc.nombre as central, \
	ipo.ne as NE, \
	po.product_id as parte_optica \
	from optical_partes_optica po \
	inner join optical_inventario_piezas_optica ipo on (ipo.product_id = po.product_id or ipo.product_id = CONCAT(po.product_id,'=')) \
	inner join optical_equipo_optical eo on eo.id = ipo.id_ne \
	inner join main_central cc on cc.id = eo.central_id \
	inner join main_ciudad c on c.id = cc.ciudad_id \
	inner join main_estado e on e.id = c.estado_id \
	inner join optical_area_divisional ad on ad.id = eo.area_div_id \
	where cc.nombre in ('Ambulancia','Bodega') order by c.nombre,cc.nombre ASC;""")
	#context['total'] = inventario_opticos.objects.count()
	return context

class Actualizar_Inventario_Parte_Optica(generic.ListView):
    template_name = 'optical/actualizar_parte_optica.html'

    def get_queryset(self):
	parte_id=self.kwargs['pk']
	#return "Hola"

    def get_context_data(self, *args, **kwargs):
	parte_id=self.kwargs['pk']
	context = super(Actualizar_Inventario_Parte_Optica, self).get_context_data(**kwargs)
	context['parte_id'] = parte_id
	return context

class Actualizar_Inventario_Parte_Optica_resultado(TemplateView):
    template_name= None

    def get(self, request):
	mensaje = "Error - Valor no actualizado"
	parte_id = self.request.GET.get("parte_id", "")
	status = self.request.GET.get("status", "")
	if status=='1':
	  mensaje="Actualizado - Disponible"
	elif status =='0':
	  mensaje="Actualizado - No Disponible"
	#t = inventario_piezas_optica.objects.get(id=1)
	#t.status = status
	#t.save(['status'])
	inventario_piezas_optica.objects.filter(id=parte_id).update(status=status)
	mimetype = 'text/plain'
        return HttpResponse(mensaje,mimetype)

  
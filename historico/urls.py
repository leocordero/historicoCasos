from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
#from django.conf.urls import handler404
#from historico.views import mi_error_404

urlpatterns = [
    #url(r'^login/$', auth_views.login, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', auth_views.login, {'template_name': 'main/login.html'}, name='login'),
    url(r'index.html$', views.IndexView.as_view(), name='index'),
    #url(r'byIP$', views.IndexViewFilterbyIP.as_view(), name='indexByIP'),
    #url(r'byHostname$', views.IndexViewFilterbyHostname.as_view(), name='indexByHostname'),
    url(r'^ce/busqueda.*$', views.Busqueda.as_view(), name='busqueda'),
    url(r'^optica/busqueda_optica.*$', views.BusquedaOptical.as_view(), name='busqueda_optical'),
    url(r'^ce/inventario$', views.Inventario.as_view(), name='inventario'),
    url(r'^ce/inventario2$', views.Inventario2.as_view(), name='inventario2'),
    url(r'^optica/inventario_optico$', views.Inventario_Optico.as_view(), name='inventario_optico'),
    url(r'^ce/(?P<pk>[0-9]+)/detalle_equipo/$', views.DetalleEquipo.as_view(), name='detalle_equipo'),
    url(r'^optica/(?P<pk>[0-9]+)/detalle_equipo_optico/$', views.DetalleEquipoOptico.as_view(), name='detalle_equipo_optico'),
    url(r'^ce/(?P<pk>[0-9]+)/historico/$', views.HistoricoCasos.as_view(), name='historico_casos'),
    url(r'^optica/(?P<pk>[0-9]+)/historico/$', views.HistoricoCasosOptica.as_view(), name='historico_casos_optica'),
    url(r'^main/soporte/$', views.Soporte.as_view(), name='soporte'),
    url(r'^optica/busqueda_avanzada_optica$', views.Busqueda_Avanzada_Optica.as_view(), name='busqueda_avanzada_optica'),
    url(r'^optica/busqueda_partes_optica/', views.Busqueda_Partes_Optica.as_view(), name='busqueda_partes_optica'),
    url(r'^optica/busqueda_nodo_optica/', views.Busqueda_Nodo_Optica.as_view(), name='busqueda_nodo_optica'),
    url(r'^optica/resultado_partes_optica/', views.Resultado_Partes_Optica.as_view(), name='resultado_partes_optica'),
    url(r'^optica/resultado_partes_optica_sn/', views.Resultado_Partes_Optica_SN.as_view(), name='resultado_partes_optica_sn'),
    url(r'^optica/resultado_partes_optica_nodo/', views.Resultado_Partes_Optica_nodo.as_view(), name='resultado_partes_optica_nodo'),
    url(r'^optica/resultado_partes_optica_nodo_detalle/', views.Resultado_Partes_Optica_nodo_detalle.as_view(), name='resultado_partes_optica_nodo_detalle'),
    url(r'^optica/resultado_partes_optica_nodo_parte/', views.Resultado_Partes_Optica_nodo_parte.as_view(), name='resultado_partes_optica_nodo_parte'),
    url(r'^optica/lista_refacciones_optica/', views.Lista_Refacciones_Optica.as_view(), name='lista_refacciones_optica'),
    url(r'^optica/(?P<pk>[0-9]+)/actualizar_inventario_parte_optica/', views.Actualizar_Inventario_Parte_Optica.as_view(), name='actualizar_inventario_parte_optica'),
    url(r'^optica/actualizar_inventario_parte_optica_resultado/', views.Actualizar_Inventario_Parte_Optica_resultado.as_view(), name='actualizar_inventario_parte_optica_resultado')
]

#handler404 = mi_error_404
from django.urls import re_path
from webapi.tipo_mascota.view import tipo_mascota_list, tipo_perro_razas_list
from webapi.color.view import color_list, color_detail
from webapi.genero.view import genero_list
from webapi.incapacidad.view import incapacidad_list
from webapi.owner.view import owner_list, owner_detail
from webapi.mascota.view import mascota_list, mascota_detail
from webapi.mascota.view import mascota_colores, mascota_colores_detail
from webapi.mascota.view import mascota_incapacidad, mascota_incapacidad_detail


urlpatterns = [
      re_path(r'^api/tipo_mascotas$', tipo_mascota_list )
    , re_path(r'^api/tipo_mascotas/(?P<id>\d+)/razas$', tipo_perro_razas_list )
    
    , re_path(r'^api/colores$', color_list )
    , re_path(r'^api/colores/(?P<id>\d+)$', color_detail )

    , re_path(r'^api/generos$', genero_list )
    , re_path(r'^api/incapacidades$', incapacidad_list )

    , re_path(r'^api/owners$', owner_list )
    , re_path(r'^api/owners/(?P<id>\d+)$', owner_detail )

    , re_path(r'^api/mascotas$', mascota_list )
    , re_path(r'^api/mascotas/(?P<id>\d+)$', mascota_detail )
    , re_path(r'^api/mascotas/(?P<id>\d+)/colores$', mascota_colores )
    , re_path(r'^api/mascotas/(?P<id>\d+)/colores/(?P<id_color>\d+)$', mascota_colores_detail )
    , re_path(r'^api/mascotas/(?P<id>\d+)/incapacidades$', mascota_incapacidad )
    , re_path(r'^api/mascotas/(?P<id>\d+)/incapacidades/(?P<id_incapacidad>\d+)$', mascota_incapacidad_detail )

]
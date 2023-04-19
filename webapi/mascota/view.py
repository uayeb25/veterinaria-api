from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from webapi.models import Mascota, MascotaColores, Color, MascotaIncapacidad, Incapacidad
from webapi.serializers import MascotaSerializer, MascotaColoresSerializer, ColorSerializer, MascotaIncapacidadSerializer, IncapacidadSerializer

from rest_framework.decorators import api_view
from django.db.utils import IntegrityError

from django.db.models import Count


from pymongo import MongoClient

from webapi.dbclasses.owner import OwnerCollection
from django.db.models import Case, When, Value, IntegerField

import pandas as pd

# Create your views here.
@api_view(['POST'])
def mascota_list(request):
    if request.method == 'POST':
        mascota_data = JSONParser().parse(request)
        mascota_serializer = MascotaSerializer(data=mascota_data)
        if mascota_serializer.is_valid():
            mascota_serializer.save()
            return JsonResponse(mascota_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(mascota_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def mascota_detail(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'GET':
        mascota_serializer = MascotaSerializer(mascota)
        return JsonResponse(mascota_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'PUT':
        mascota_data = JSONParser().parse(request)
        mascota_data["id"] = id
        mascota_serializer = MascotaSerializer(mascota, data=mascota_data)
        if mascota_serializer.is_valid():
            mascota_serializer.save()
            return JsonResponse(mascota_serializer.data)
        return JsonResponse(mascota_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mascota.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def mascota_colores(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    if request.method == 'GET':
        colores = MascotaColores.objects.filter(id_mascota=mascota)
        colores_serializer = MascotaColoresSerializer(colores, many=True)
        return JsonResponse(colores_serializer.data, safe=False)
    
    elif request.method == 'POST':
        colores_data = JSONParser().parse(request)
        colores_data["id_mascota"] = id
        colores_serializer = MascotaColoresSerializer(data=colores_data)
        if colores_serializer.is_valid():
            colores_serializer.save()
            return JsonResponse(colores_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(colores_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def mascota_colores_detail(request, id, id_color):
    if request.method == 'DELETE':
        mascota = get_object_or_404(Mascota, id=id)
        color = get_object_or_404(Color, id=id_color)
        mascota_color = get_object_or_404(MascotaColores, id_color=color, id_mascota=mascota)        
        mascota_color.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
def mascota_incapacidad(request, id):
    
    
    mascota = get_object_or_404(Mascota, id=id)    
    
    if request.method == 'POST':
        incapacidad_data = JSONParser().parse(request)
        incapacidad_data["id_mascota"] = id
        
        incapacidad_id = incapacidad_data["id_incapacidad"]
        incapacidad = Incapacidad.objects.get(id=incapacidad_id)

        mascota_incapacidad = MascotaIncapacidad.objects.filter(id_mascota=mascota, id_incapacidad=incapacidad)
        if len(mascota_incapacidad) > 0:
            return JsonResponse({"error": "Incapacidad ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        incapacidad_serializer = MascotaIncapacidadSerializer(data=incapacidad_data)
        if incapacidad_serializer.is_valid():
            incapacidad_serializer.save()
            return JsonResponse(incapacidad_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(incapacidad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        
        incapacidades = Incapacidad.objects.all().values()
        
        mascota_incapacidades = MascotaIncapacidad.objects.filter(
            id_mascota=mascota
        ).values(
            'id_mascota'
            ,'descripcion'
            ,'id_incapacidad'
        ).distinct()        

        ##pip install pandas
        df_incapacidades = pd.DataFrame(list(incapacidades))
        df_mascota_incapacidades = pd.DataFrame(list(mascota_incapacidades), columns=['id_mascota','descripcion','id_incapacidad'])
        
        df_incapacidades.columns = ['id','incapacidad']
        df_result = df_incapacidades.merge(df_mascota_incapacidades, how='left', left_on='id', right_on='id_incapacidad')      
        
        df_result['has_incapacidad'] = False
        df_result.loc[ df_result['id_mascota'].notnull() , 'has_incapacidad' ] = True
        df_result = df_result.loc[:, ['id','incapacidad','descripcion','has_incapacidad']]       

        #retornamos df_incapacidades
        return JsonResponse(list(df_result.to_dict('records')), safe=False)
        
    
@api_view(['DELETE'])
def mascota_incapacidad_detail(request, id, id_incapacidad):
    if request.method == 'DELETE':
        mascota = get_object_or_404(Mascota, id=id)
        incapacidad = get_object_or_404(Incapacidad, id=id_incapacidad)
        mascota_incapacidad = get_object_or_404(MascotaIncapacidad, id_incapacidad=incapacidad, id_mascota=mascota)        
        mascota_incapacidad.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
    
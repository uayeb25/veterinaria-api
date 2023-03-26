from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.parsers import JSONParser
from rest_framework import status

from webapi.models import TipoMascota, Raza
from webapi.serializers import TipoMascotaSerializer, RazaSerializer
from rest_framework.decorators import api_view

from django.db.models import Count
# Create your views here.

@api_view(['GET', 'POST'])
def tipo_mascota_list(request):
    if request.method == 'GET':
        tipo_mascota = TipoMascota.objects.all()
        tipo_mascota_serializer = TipoMascotaSerializer(tipo_mascota, many=True)
        return JsonResponse(tipo_mascota_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        tipo_mascota_data = JSONParser().parse(request)
        tipo_mascota_serializer = TipoMascotaSerializer(data=tipo_mascota_data)
        if tipo_mascota_serializer.is_valid():
            tipo_mascota_serializer.save()
            return JsonResponse(tipo_mascota_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tipo_mascota_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST'])
def tipo_perro_razas_list(request, id):
    tipo_mascota = get_object_or_404(TipoMascota, id=id)
    if request.method == 'GET':
        raza = Raza.objects.filter(id_tipo_mascota=tipo_mascota)
        raza_serializer = RazaSerializer(raza, many=True)
        return JsonResponse(raza_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        payload = request.data
        
        raza_data = {'descripcion': payload['descripcion'], 'id_tipo_mascota': tipo_mascota.id}
        raza_serializer = RazaSerializer(data=raza_data)
        
        if raza_serializer.is_valid():
            raza_serializer.save()
            return JsonResponse(raza_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(raza_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
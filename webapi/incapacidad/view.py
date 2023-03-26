from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest_framework import status

from webapi.models import Incapacidad
from webapi.serializers import IncapacidadSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def incapacidad_list(request):
    if request.method == 'GET':
        incapacidad = Incapacidad.objects.all()
        incapacidad_serializer = IncapacidadSerializer(incapacidad, many=True)
        return JsonResponse(incapacidad_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        incapacidad_data = JSONParser().parse(request)
        incapacidad_serializer = IncapacidadSerializer(data=incapacidad_data)
        if incapacidad_serializer.is_valid():
            incapacidad_serializer.save()
            return JsonResponse(incapacidad_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(incapacidad_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
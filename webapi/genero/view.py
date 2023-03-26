from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest_framework import status

from webapi.models import Genero
from webapi.serializers import GeneroSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def genero_list(request):
    if request.method == 'GET':
        genero = Genero.objects.all()
        genero_serializer = GeneroSerializer(genero, many=True)
        return JsonResponse(genero_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        genero_data = JSONParser().parse(request)
        genero_serializer = GeneroSerializer(data=genero_data)
        if genero_serializer.is_valid():
            genero_serializer.save()
            return JsonResponse(genero_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(genero_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
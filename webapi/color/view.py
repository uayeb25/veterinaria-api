from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest_framework import status

from webapi.models import Color
from webapi.serializers import ColorSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def color_list(request):
    if request.method == 'GET':
        color = Color.objects.all()
        color_serializer = ColorSerializer(color, many=True)
        return JsonResponse(color_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        color_data = JSONParser().parse(request)
        color_serializer = ColorSerializer(data=color_data)
        if color_serializer.is_valid():
            color_serializer.save()
            return JsonResponse(color_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(color_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def color_detail(request, id):
    try:
        color = Color.objects.get(id=id)
    except Color.DoesNotExist:
        return JsonResponse({'message': 'The color does not exist....'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        color_serializer = ColorSerializer(color)
        return JsonResponse(color_serializer.data)

    elif request.method == 'PUT':
        color_data = JSONParser().parse(request)
        color_serializer = ColorSerializer(color, data=color_data)
        if color_serializer.is_valid():
            color_serializer.save()
            return JsonResponse(color_serializer.data)
        return JsonResponse(color_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        color.delete()
        return JsonResponse({'message': 'Color was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
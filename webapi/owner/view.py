from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from webapi.models import Owner
from webapi.serializers import OwnerSerializer
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError

from django.db.models import Count


from pymongo import MongoClient

from webapi.dbclasses.owner import OwnerCollection


# Create your views here.
@api_view(['POST'])
def owner_list(request):
    if request.method == 'POST':
        owner_data = JSONParser().parse(request)
        owner_serializer = OwnerSerializer(data=owner_data)
        owner = Owner.objects.filter(id_nacional=owner_data['id_nacional'])
        if len(owner) > 0:
            return JsonResponse({ "message": "ID already exist" }, status=status.HTTP_400_BAD_REQUEST)
        
        if owner_serializer.is_valid():
            owner_serializer.save()
            return JsonResponse(owner_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE'])
def owner_detail(request, id):
    owner = get_object_or_404(Owner, id_nacional=id)
    if request.method == 'GET':
        owner_serializer = OwnerSerializer(owner)
        return JsonResponse(owner_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'PUT':
        owner_data = JSONParser().parse(request)        
        owner_serializer = OwnerSerializer(owner, data=owner_data)
        
        owner = Owner.objects.filter(id_nacional=owner_data['id_nacional'])
        if len(owner) > 0 and id != owner_data['id_nacional']:
            return JsonResponse({ "message": "ID already exist" }, status=status.HTTP_400_BAD_REQUEST)
        
        if owner_serializer.is_valid():
            owner_serializer.save()
            return JsonResponse(owner_serializer.data)
        return JsonResponse(owner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        owner.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
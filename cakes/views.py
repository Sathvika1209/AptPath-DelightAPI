from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Cake
from .serializers import CakeSerializer

class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

from django.shortcuts import render
from rest_framework import generics

from .serializers import CreateTenantSerializer
# Create your views here.


class CreateTenantView(generics.CreateAPIView):
    serializer_class = CreateTenantSerializer

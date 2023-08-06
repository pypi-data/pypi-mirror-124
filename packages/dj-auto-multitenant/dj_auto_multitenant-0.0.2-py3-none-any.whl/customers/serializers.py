from rest_framework import serializers
from .models import Client

class CreateTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('name',)
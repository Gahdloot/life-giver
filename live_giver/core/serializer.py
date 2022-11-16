from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'location']

class ClientCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "name",
            "phone_number",
            "email",
            "bvn",
            "password",
            "location",
            "age",
            "weight",
            "blood_group",
   
        ]
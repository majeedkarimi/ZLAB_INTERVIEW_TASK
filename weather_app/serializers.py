from rest_framework import serializers
from .models import WeatherSerializer


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSerializer
        fields = '__all__'






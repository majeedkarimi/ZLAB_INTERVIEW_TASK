from django.db import models
from django.utils.timezone import now

class WeatherSerializer(models.Model):
    """
    Django model representing weather data.

    Attributes:
    - temperature (FloatField): Temperature in Kelvin (default: 0).
    - humidity (IntegerField): Humidity percentage (default: 0).
    - precipitation (FloatField): Precipitation amount in millimeters (default: 0).
    - wind_speed (FloatField): Wind speed in kilometers per hour (default: 0).
    - visibility (FloatField): Visibility in meters (default: 1.0).
    - name (CharField): Name or identifier for the weather data (max length: 120, blank allowed).
    - weather (CharField): Description of the weather conditions (max length: 120, default: '').
    - sunrise (TimeField): Time of sunrise (default: current time).
    - sunset (TimeField): Time of sunset (default: current time).
    - today (DateField): Date for which the weather data is recorded (default: current date).
    """
    temperature = models.FloatField(default=0)
    humidity = models.IntegerField(default=0)
    precipitation = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    visibility= models.FloatField(default=1.0)
    name=models.CharField(max_length=120,blank=True)
    weather=models.CharField(max_length=120,default='')
    sunrise=models.TimeField(default=now)
    sunset=models.TimeField(default=now)
    today=models.DateField(default=now)




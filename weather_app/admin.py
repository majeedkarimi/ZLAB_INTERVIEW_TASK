from django.contrib import admin
from.models import WeatherSerializer

# Register your models here.
class WeatherAdmin(admin.ModelAdmin):
    pass


admin.site.register(WeatherSerializer, WeatherAdmin)

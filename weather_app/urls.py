from django.urls import path
from .views import view_weather,WeatherInfoView,WeatherInfoViewHtml,WeatherInfoViewLoc

urlpatterns = [
    path('',view_weather,name='insert_location'),
    path('weather/', WeatherInfoView.as_view(), name='weather-info'),
    path('weather_html/', WeatherInfoViewHtml.as_view(), name='weather-info-html'),
    path('weather_loc/', WeatherInfoViewLoc.as_view(), name='weather-info-loc'),

] 
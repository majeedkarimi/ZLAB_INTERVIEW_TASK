from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings
from .serializers import WeatherSerializer
from rest_framework.request import Request
from django.shortcuts import render
from datetime import date,datetime
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def view_weather(request):
    """
    View function to render the 'insert_location.html' template for weather information.

    Parameters:
    - request (HttpRequest): The HTTP request object that triggered this view.
    """
    return render(request,'insert_location.html')


class WeatherInfoView(APIView):
    """
    WeatherInfoView is a Django REST Framework API view that retrieves weather information
    for a specified region using the OpenWeatherMap API.

    Endpoint: /weather-info/

    Methods:
    - GET: Retrieves and returns the current weather information for the specified region.

    Parameters:
    - region (query parameter): Required. The name of the region for which weather information is requested.

    Responses:
    - 200 OK: Successful response with weather information in the specified format.
    - 400 Bad Request: Missing or invalid 'region' parameter.
    - 500 Internal Server Error: An error occurred during the API request or data processing.
    """
    
    # create Basic Authentication
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request:Request):
        """
        Handles the GET request to retrieve weather information for a specified region.

        Parameters:
        - request: The HTTP request object containing query parameters.

        Returns:
        - Response: A JSON response containing weather information or an error message.
        """

        # Extract the 'region' parameter from the query parameters.
        region = request.query_params.get('region')

        # Check if the 'region' parameter is missing.
        if not region:
            return Response({'error': 'Region parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the OpenWeatherMap API key from Django settings.
        api_key = settings.WEATHER_API_KEY

        # Build the API URL for the OpenWeatherMap request.
        api_url = f'https://api.openweathermap.org/data/2.5/weather?q={region}&appid={api_key}'

        try:
            # Send a GET request to the OpenWeatherMap API.
            response = requests.get(api_url)
            response.raise_for_status() # Raise an exception for HTTP errors.

            # Parse the JSON response from the OpenWeatherMap API.
            weather_data = response.json()

        except requests.exceptions.HTTPError as http_err:
            return Response({'error': f'HTTP error occurred: {http_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as req_err:
            return Response({'error': f'Request error occurred: {req_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as val_err:
            return Response({'error': f'Failed to parse weather data: {val_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Process and format the retrieved weather data.
        mylist = [date.today()]

        # Create a WeatherSerializer instance for data validation and serialization.
        serializer = WeatherSerializer(data={
            'temperature': round(weather_data['main']['temp']-273.15,2),
            'humidity': weather_data['main']['humidity'],
            'precipitation': weather_data.get('rain', {}).get('1h', 0),
            'wind_speed': weather_data['wind']['speed'],
            'visibility': weather_data['visibility']/1000,
            'name':weather_data['name'],
            'weather':weather_data['weather'][0]['description'],
            'sunrise':datetime.fromtimestamp(int(weather_data['sys']['sunrise'])).strftime('%H:%M:%S'),
            'sunset':datetime.fromtimestamp(int(weather_data['sys']['sunset'])).strftime('%H:%M:%S'),
            'today':mylist[0],
        })

        # Check if the serializer successfully validates the data.
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherInfoViewHtml(APIView):
    """
    WeatherInfoViewHtml - API view class for retrieving weather information.

    This API view class handles GET requests to fetch weather information for a specified region using the OpenWeatherMap API.

    Endpoint: /weather-info-html/

    Methods:
        - get(self, request: Request): Handles GET requests and returns weather information for the specified region.

    """
    def get(self, request:Request):
        """
        Handles GET requests and returns weather information for the specified region.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing weather information for the specified region.

        """

        # Retrieve the 'region' parameter from the query parameters
        region = request.query_params.get('region')

        # Check if the 'region' parameter is provided
        if not region:
            return Response({'error': 'Region parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the OpenWeatherMap API key from Django settings
        api_key = settings.WEATHER_API_KEY

        # Construct the API URL for fetching weather data
        api_url = f'https://api.openweathermap.org/data/2.5/weather?q={region}&appid={api_key}'

        # Make a GET request to the OpenWeatherMap API
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            weather_data = response.json()

        # Handle HTTP errors
        except requests.exceptions.HTTPError as http_err:
            return Response({'error': f'HTTP error occurred: {http_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Handle general request errors
        except requests.exceptions.RequestException as req_err:
            return Response({'error': f'Request error occurred: {req_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Handle JSON parsing errors
        except ValueError as val_err:
            return Response({'error': f'Failed to parse weather data: {val_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Process and format the retrieved weather data.
        mylist = [date.today()]

        # Create a WeatherSerializer instance for data validation and serialization.
        serializer = WeatherSerializer(data={
            'temperature': round(weather_data['main']['temp']-273.15,2),
            'humidity': weather_data['main']['humidity'],
            'precipitation': weather_data.get('rain', {}).get('1h', 0),
            'wind_speed': weather_data['wind']['speed'],
            'visibility': weather_data['visibility']/1000,
            'name':weather_data['name'],
            'weather':weather_data['weather'][0]['description'],
            'sunrise':datetime.fromtimestamp(int(weather_data['sys']['sunrise'])).strftime('%H:%M:%S'),
            'sunset':datetime.fromtimestamp(int(weather_data['sys']['sunset'])).strftime('%H:%M:%S'),
            'today':mylist[0],
        })

        # Check if the serializer is valid
        if serializer.is_valid():
            return render(request,'vw_view.html',{"data":serializer})
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WeatherInfoViewLoc(APIView):
    """
    WeatherInfoViewLoc is a Django Rest Framework APIView that retrieves current weather information based on latitude and longitude.

    Endpoint: /path/to/endpoint/?lat=<latitude>&lon=<longitude>

    Parameters:
        - lat: Latitude of the location (required).
        - lon: Longitude of the location (required).

    Returns:
        - 200 OK: Returns weather information in a serialized format.
        - 400 Bad Request: If lat or lon parameters are missing.
        - 500 Internal Server Error: If there's an issue with the external weather API or data parsing.

    """
    def get(self, request:Request):
        """
        Handles GET requests to retrieve weather information.

        Args:
            request (Request): Django Rest Framework request object.

        Returns:
            Response: Serialized weather information or error response.
        """

        # Extract latitude and longitude from query parameters
        lat = request.query_params.get('lat')
        lon= request.query_params.get('lon')

        # Validate the presence of lat and lon parameters
        if not lat:
            return Response({'error': 'Lat parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not lon:
            return Response({'error': 'Lon parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve API key from Django settings
        api_key = settings.WEATHER_API_KEY

        # Construct the API URL for OpenWeatherMap
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

        try:
            # Make a request to the OpenWeatherMap API
            response = requests.get(api_url)
            response.raise_for_status()
            weather_data = response.json()
        except requests.exceptions.HTTPError as http_err:
            return Response({'error': f'HTTP error occurred: {http_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as req_err:
            return Response({'error': f'Request error occurred: {req_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as val_err:
            return Response({'error': f'Failed to parse weather data: {val_err}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        mylist = [date.today()]
        serializer = WeatherSerializer(data={
            'temperature': round(weather_data['main']['temp']-273.15,2),
            'humidity': weather_data['main']['humidity'],
            'precipitation': weather_data.get('rain', {}).get('1h', 0),
            'wind_speed': weather_data['wind']['speed'],
            'visibility': weather_data['visibility']/1000,
            'name':weather_data['name'],
            'weather':weather_data['weather'][0]['description'],
            'sunrise':datetime.fromtimestamp(int(weather_data['sys']['sunrise'])).strftime('%H:%M:%S'),
            'sunset':datetime.fromtimestamp(int(weather_data['sys']['sunset'])).strftime('%H:%M:%S'),
            'today':mylist[0],
        })


        # Check if the serializer is valid and return the appropriate response
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


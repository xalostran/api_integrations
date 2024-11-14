import requests
import os
from dotenv import load_dotenv

load_dotenv()

class API():
    def get_weather(self, city_weather):
        weather_key = os.getenv("WEATHER_API")
        url_weather = f"http://api.openweathermap.org/data/2.5/weather?q={city_weather}&appid={weather_key}"

        response_weather = requests.get(url_weather, timeout=10)
        weather_data = response_weather.json()

        if response_weather.status_code == 200:
            # Hämta vädret från API-svar
            weather_description = weather_data["weather"][0]["description"]
            temperature_kelvin = weather_data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15  # Omvandla Kelvin till Celsius

            return(f"Vädret i {city_weather} är {weather_description}. " 
                   f"Temperaturen är {temperature_celsius:.2f} grader Celsius.")
        else:
            return{"Det gick inte att hämta vädret för den angivna platsen."}

    def get_location(self, city_location):
        location_key = os.getenv("LOCATION_API")
        url_location = f"https://geocode.maps.co/search?q={city_location}&api_key={location_key}"

        response_location = requests.get(url_location, timeout=10)
        location_data = response_location.json()

        if response_location.status_code == 200:
            latitude = location_data[0]["lat"]
            longitude = location_data[0]["lon"]
            return{f"Latitude: {latitude}, Longitude: {longitude}"}
        else:
            return{"Error: ", response_location.status_code}

        
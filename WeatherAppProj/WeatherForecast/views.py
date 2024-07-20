from django.shortcuts import render, HttpResponse

from geopy.geocoders import Nominatim
import requests
import pandas as pd
import openmeteo_requests


# Create your views here.
def home(request) -> None:
    if request.method == "POST":
        city = request.POST.get("city")
        latitude, longitude = get_coordinates(city)
        print(latitude, longitude)
        data = get_weather_forecast(latitude, longitude, 2)
        print(data)
        if data["weather_code"] == 0:
            return render(request, "today.html",
                          {"image": "static/sunny.png", "city": city, "maxTemp": data['max_temperature'],
                           "wind_speed": int(data["windspeed_10m"]),
                           "pression": int(data['pressure_msl']),
                           "humidity": int(data["humidity_2m"])})
        elif data["weather_code"] == 1:
            return render(request, "today.html",
                          {"image": "static/cloudy.png", "city": city, "maxTemp": data['max_temperature'],
                           "wind_speed": int(data["windspeed_10m"]),
                           "pression": int(data['pressure_msl']),
                           "humidity": int(data["humidity_2m"])})
        elif data["weather_code"] == 3:
            return render(request, "today.html",
                          {"image": "static/rainy.png", "city": city, "maxTemp": data['max_temperature'],
                           "wind_speed": int(data["windspeed_10m"]),
                           "pression": int(data['pressure_msl']),
                           "humidity": int(data["humidity_2m"])})
        else:
            return render(request, "today.html",
                          {"image": "static/sunny.png", "city": city, "maxTemp": data['max_temperature'],
                           "wind_speed": int(data["windspeed_10m"]),
                           "pression": int(data['pressure_msl']),
                           "humidity": int(data["humidity_2m"])})
    else:
        return render(request, "index.html")


def tomorrow(request) -> None:
    if request.method == "POST":
        city = request.POST.get("city")
        latitude, longitude = get_coordinates(city)
        print(latitude, longitude)
        data = get_weather_forecast(latitude, longitude, 2)
        print(data)
        return render(request, "tomorrow.html",
                      {"image": get_weather_image(data["weather_code"]), "city": city, "maxTemp": data['max_temperature'],
                       "wind_speed": int(data["windspeed_10m"]),
                       "pression": int(data['pressure_msl']),
                       "humidity": int(data["humidity_2m"])})
    else:
        return render(request, "index.html")


def three_days(request) -> None:
    if request.method == "POST":
        city = request.POST.get("city")
        latitude, longitude = get_coordinates(city)
        data = get_weather_forecast(latitude, longitude, 3)

        if len(data['temperature_2m']) >= 3:
            return render(request, "three_days.html", {
                "city": city,
                "day1": {
                    "image": get_weather_image(data["weather_code"][0]),
                    "temp": int(data['temperature_2m'][0]),
                    "press": int(data['pressure_msl'][0]),
                    "hum": int(data['humidity_2m'][0])
                },
                "day2": {
                    "image": get_weather_image(data["weather_code"][1]),
                    "temp": int(data['temperature_2m'][1]),
                    "press": int(data['pressure_msl'][1]),
                    "hum": int(data['humidity_2m'][1])
                },
                "day3": {
                    "image": get_weather_image(data["weather_code"][2]),
                    "temp": int(data['temperature_2m'][2]),
                    "press": int(data['pressure_msl'][2]),
                    "hum": int(data['humidity_2m'][2])
                }
            })
    else:
        return render(request, "index.html")


def seven_days(request) -> None:
    if request.method == "POST":
        city = request.POST.get("city")
        latitude, longitude = get_coordinates(city)
        data = get_weather_forecast(latitude, longitude, 7)

        if len(data['temperature_2m']) >= 7:
            return render(request, "seven_days.html", {
                "city": city,
                "day1": {
                    "image": get_weather_image(data["weather_code"][0]),
                    "temp": int(data['temperature_2m'][0]),
                    "press": int(data['pressure_msl'][0]),
                    "hum": int(data['humidity_2m'][0])
                },
                "day2": {
                    "image": get_weather_image(data["weather_code"][1]),
                    "temp": int(data['temperature_2m'][1]),
                    "press": int(data['pressure_msl'][1]),
                    "hum": int(data['humidity_2m'][1])
                },
                "day3": {
                    "image": get_weather_image(data["weather_code"][2]),
                    "temp": int(data['temperature_2m'][2]),
                    "press": int(data['pressure_msl'][2]),
                    "hum": int(data['humidity_2m'][2])
                },
                "day4": {
                    "image": get_weather_image(data["weather_code"][3]),
                    "temp": int(data['temperature_2m'][3]),
                    "press": int(data['pressure_msl'][3]),
                    "hum": int(data['humidity_2m'][3])
                },
                "day5": {
                    "image": get_weather_image(data["weather_code"][4]),
                    "temp": int(data['temperature_2m'][4]),
                    "press": int(data['pressure_msl'][4]),
                    "hum": int(data['humidity_2m'][4])
                },
                "day6": {
                    "image": get_weather_image(data["weather_code"][5]),
                    "temp": int(data['temperature_2m'][5]),
                    "press": int(data['pressure_msl'][5]),
                    "hum": int(data['humidity_2m'][5])
                },
                "day7": {
                    "image": get_weather_image(data["weather_code"][6]),
                    "temp": int(data['temperature_2m'][6]),
                    "press": int(data['pressure_msl'][6]),
                    "hum": int(data['humidity_2m'][6])
                }
            })
    else:
        return render(request, "index.html")


def get_coordinates(city: str):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(city)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def get_weather_forecast(latitude, longitude, days):
    if days == 2:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,windspeed_10m,pressure_msl,relativehumidity_2m,weathercode&timezone=Europe%2FBerlin&past_days=0&forecast_days=1"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            temperature_2m = data['hourly']['temperature_2m']
            windspeed_10m = data['hourly']['windspeed_10m']
            pressure_msl = data['hourly']['pressure_msl']
            humidity_2m = data['hourly']['relativehumidity_2m']
            weather_code = data['hourly']['weathercode']

            # Проверяем длину списка
            if len(temperature_2m) >= 24:
                # Интерполяция для 25 часов
                temperature_25h = (temperature_2m[23] + temperature_2m[0]) / 2
                windspeed_25h = (windspeed_10m[23] + windspeed_10m[0]) / 2
                pressure_25h = (pressure_msl[23] + pressure_msl[0]) / 2
                humidity_25h = (humidity_2m[23] + humidity_2m[0]) / 2
                weather_code_25h = (weather_code[23] + weather_code[0]) // 2

                max_temperature = max(temperature_2m)

                forecast = {
                    'temperature_2m': temperature_25h,
                    'windspeed_10m': windspeed_25h,
                    'pressure_msl': pressure_25h,
                    'humidity_2m': humidity_25h,
                    'max_temperature': max_temperature,
                    'weather_code': weather_code_25h
                }

                return forecast
            else:
                return None
        else:
            return None
    elif days >= 3:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,windspeed_10m,pressure_msl,relativehumidity_2m,weathercode&timezone=Europe%2FBerlin&past_days=0&forecast_days={days}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            temperature_2m = data['hourly']['temperature_2m']
            windspeed_10m = data['hourly']['windspeed_10m']
            pressure_msl = data['hourly']['pressure_msl']
            humidity_2m = data['hourly']['relativehumidity_2m']
            weather_code = data['hourly']['weathercode']

            daily_temperature_2m = [sum(temperature_2m[i:i + 24]) / 24 for i in range(0, len(temperature_2m), 24)]
            daily_windspeed_10m = [sum(windspeed_10m[i:i + 24]) / 24 for i in range(0, len(windspeed_10m), 24)]
            daily_pressure_msl = [sum(pressure_msl[i:i + 24]) / 24 for i in range(0, len(pressure_msl), 24)]
            daily_humidity_2m = [sum(humidity_2m[i:i + 24]) / 24 for i in range(0, len(humidity_2m), 24)]
            daily_weather_code = [weather_code[i] for i in range(0, len(weather_code), 24)]

            forecast = {
                'temperature_2m': daily_temperature_2m,
                'windspeed_10m': daily_windspeed_10m,
                'pressure_msl': daily_pressure_msl,
                'humidity_2m': daily_humidity_2m,
                'weather_code': daily_weather_code
            }

            return forecast
        else:
            return None


def get_weather_image(number: int) -> str:
    if number == 0:
        return "static/sunny.png"
    elif number == 1:
        return "static/cloudy.png"
    else:
        return "static/rainy.png"

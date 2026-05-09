import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def weather_agent(query: str):

    print("Weather agent called")

    # -----------------------------
    # 🌍 DEFAULT LOCATION (change if needed)
    # -----------------------------
    city = "Hyderabad"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
    except:
        return "Unable to fetch weather data."

    if data.get("cod") != 200:
        return "Weather data not available."

    # -----------------------------
    # 📊 EXTRACT DATA
    # -----------------------------
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind = data["wind"]["speed"]

    # -----------------------------
    # 🌱 FARMER FRIENDLY OUTPUT
    # -----------------------------
    return f"""
Weather in {city}:
Temperature: {temp}°C
Humidity: {humidity}%
Condition: {weather}
Wind Speed: {wind} m/s

Advice:
Avoid spraying if rain or high wind is expected.
"""
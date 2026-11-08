"""
LuntiAI — Weather Service
===========================
Fetches real-time weather data from OpenWeatherMap API
with fallback to hard-coded monthly climate presets for the classroom demo.

Author: LuntiAI Team
"""

import os
import requests

# Monthly classroom presets for Tagum City / Davao del Norte
# Original attribution: PAGASA 1991-2020, Davao; exact table not independently verified.
# Monthly averages — used as fallback when API is unavailable
TAGUM_CLIMATE_NORMALS = {
    1:  {"temp": 27.0, "humidity": 82, "rainfall": 130, "description": "Warm, moderate rain"},
    2:  {"temp": 27.2, "humidity": 80, "rainfall": 105, "description": "Warm, less rain"},
    3:  {"temp": 27.8, "humidity": 78, "rainfall": 100, "description": "Warmest, drier"},
    4:  {"temp": 28.2, "humidity": 78, "rainfall": 120, "description": "Hot, transition"},
    5:  {"temp": 27.8, "humidity": 80, "rainfall": 175, "description": "Warm, wet season starts"},
    6:  {"temp": 27.2, "humidity": 82, "rainfall": 195, "description": "Wet season"},
    7:  {"temp": 27.0, "humidity": 82, "rainfall": 180, "description": "Wet season peak"},
    8:  {"temp": 27.0, "humidity": 82, "rainfall": 165, "description": "Wet season"},
    9:  {"temp": 27.2, "humidity": 82, "rainfall": 175, "description": "Wet season"},
    10: {"temp": 27.4, "humidity": 82, "rainfall": 190, "description": "Wet, typhoon season"},
    11: {"temp": 27.4, "humidity": 82, "rainfall": 170, "description": "Wet, transitioning"},
    12: {"temp": 27.2, "humidity": 82, "rainfall": 145, "description": "Moderate rain"},
}


def get_weather_data(lat: float, lon: float, api_key: str = None) -> dict:
    """
    Fetch current weather data for given coordinates.

    Tries OpenWeatherMap API first, falls back to monthly presets.

    Returns:
        dict with keys: temp, humidity, rainfall_estimate, description, source
    """
    if api_key:
        try:
            return _fetch_openweather(lat, lon, api_key)
        except Exception as e:
            print(f"Weather API unavailable ({type(e).__name__}); using monthly presets.")
            return _get_pagasa_fallback()
    else:
        return _get_pagasa_fallback()


def _fetch_openweather(lat: float, lon: float, api_key: str) -> dict:
    """Fetch from OpenWeatherMap Current Weather API."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Extract relevant fields
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    # Rainfall: check if rain data is available
    rain_1h = 0
    if "rain" in data:
        rain_1h = data["rain"].get("1h", 0)

    # Estimate monthly rainfall from current conditions
    # Use climate normals as base, adjust with current rain indicator
    import datetime
    month = datetime.datetime.now().month
    normal = TAGUM_CLIMATE_NORMALS.get(month, TAGUM_CLIMATE_NORMALS[1])
    rainfall_estimate = normal["rainfall"]

    # Weather description
    description = ""
    if data.get("weather"):
        description = data["weather"][0].get("description", "")

    return {
        "temp": round(temp, 1),
        "humidity": humidity,
        "rainfall_estimate": rainfall_estimate,
        "current_rain_1h_mm": round(rain_1h, 1),
        "description": description,
        "source": "OpenWeatherMap (current temperature and humidity)",
        "rainfall_source": "Monthly climate preset",
        "is_live": True,
        "icon": data["weather"][0].get("icon", "01d") if data.get("weather") else "01d",
    }


def _get_pagasa_fallback() -> dict:
    """Return monthly climate presets for current month."""
    import datetime
    month = datetime.datetime.now().month
    normal = TAGUM_CLIMATE_NORMALS.get(month, TAGUM_CLIMATE_NORMALS[1])

    return {
        "temp": normal["temp"],
        "humidity": normal["humidity"],
        "rainfall_estimate": normal["rainfall"],
        "current_rain_1h_mm": 0,
        "description": normal["description"],
        "source": "Monthly climate preset (offline)",
        "rainfall_source": "Monthly climate preset",
        "is_live": False,
        "icon": "02d",
    }

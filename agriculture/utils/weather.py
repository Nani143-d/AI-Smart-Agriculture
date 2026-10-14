import requests


def get_weather(city):
    try:
        # Find the city's geographical coordinates.
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        locations = geo_data.get("results", [])

        if not locations:
            return {
                "error": "City not found. Please enter a valid city name."
            }

        location = locations[0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        # Retrieve current weather.
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = requests.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,precipitation,"
                    "weather_code,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )

        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]

        # Convert weather codes into readable descriptions.
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snowfall",
            73: "Moderate snowfall",
            75: "Heavy snowfall",
            80: "Rain showers",
            81: "Moderate rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with heavy hail",
        }

        return {
            "city": location["name"],
            "country": location.get("country", ""),
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "description": weather_codes.get(
                current["weather_code"],
                "Weather conditions unavailable",
            ),
            "wind_speed": current["wind_speed_10m"],
            "precipitation": current["precipitation"],
            "time": current["time"],
        }

    except requests.exceptions.Timeout:
        return {
            "error": "The weather service timed out. Please try again."
        }

    except requests.exceptions.RequestException:
        return {
            "error": "Unable to connect to the weather service."
        }

    except (KeyError, ValueError, TypeError):
        return {
            "error": "Unable to process the weather information."
        }
import requests

BASE_API = "https://www.tmd.go.th/api/weather/aws/province/"

def get_weather_data(province_slug):
    url = BASE_API + province_slug

    try:
        response = requests.get(url)
        data = response.json()

        weather_info = {
            "temperature": str(data.get("temperature", "N/A")),
            "totalraintoday": str(data.get("rain_24h", "0")),
            "humidity": str(data.get("humidity", "N/A"))
        }

        return weather_info

    except Exception as e:
        return {
            "temperature": "N/A",
            "totalraintoday": "0",
            "humidity": "N/A"
        }

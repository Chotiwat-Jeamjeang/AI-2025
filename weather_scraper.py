import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tmd.go.th/weather/province/"

def get_weather_data(province_slug):
    url = BASE_URL + province_slug
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    weather_info = {}

    try:
        weather_info["temperature"] = soup.find("label", id="lblAwsTemperature").text.strip()
    except:
        weather_info["temperature"] = "N/A"

    try:
        weather_info["totalraintoday"] = soup.find("label", id="lblAwsRainFrom7AM").text.strip()
    except:
        weather_info["totalraintoday"] = "N/A"

    try:
        weather_info["humidity"] = soup.find("label", id="lblAwsHumidity").text.strip()
    except:
        weather_info["humidity"] = "N/A"

    return weather_info

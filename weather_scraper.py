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
        weather_info["temperature"] = soup.find("span", class_="temp").text.strip()
    except:
        weather_info["temperature"] = "N/A"

    try:
        weather_info["rainfall"] = soup.find("span", class_="rain").text.strip()
    except:
        weather_info["rainfall"] = "N/A"

    try:
        weather_info["description"] = soup.find("div", class_="weather-desc").text.strip()
    except:
        weather_info["description"] = "N/A"

    return weather_info

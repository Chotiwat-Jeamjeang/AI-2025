import requests
import streamlit as st

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

def get_weather_data(lat, lon):

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={API_KEY}"
        "&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    weather_info = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "totalraintoday": data.get("rain", {}).get("1h", 0)
    }

    return weather_info

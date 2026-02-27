import streamlit as st
import requests
import json
from ai_analyzer import analyze_weather

st.set_page_config(page_title="AI Weather Risk", layout="centered")

st.title("🌦️ AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

# โหลดจังหวัดจาก JSON
with open("provinces.json", "r", encoding="utf-8") as f:
    provinces = json.load(f)

province_names = list(provinces.keys())

# Dropdown เลือกจังหวัด
selected_province = st.selectbox("เลือกจังหวัด", province_names)

if st.button("วิเคราะห์สภาพอากาศ"):

    lat = provinces[selected_province]["lat"]
    lon = provinces[selected_province]["lon"]

    API_KEY = st.secrets["OPENWEATHER_API_KEY"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    weather_info = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rain": data.get("rain", {}).get("1h", 0)
    }

    st.subheader("📊 ข้อมูลปัจจุบัน")
    st.write(f"🌡️ อุณหภูมิ: {weather_info['temperature']} °C")
    st.write(f"💧 ความชื้น: {weather_info['humidity']} %")
    st.write(f"🌧️ ฝน 1 ชม.: {weather_info['rain']} mm")

    st.subheader("📈 ผลการวิเคราะห์ AI")
    result = analyze_weather(weather_info)
    st.write(result)

import streamlit as st
from weather_scraper import get_weather_data
from ai_analyzer import analyze_weather

st.set_page_config(
    page_title="AI Weather Risk",
    page_icon="🌧️",
    layout="centered"
)

st.title("🌦️ AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

# ตัวอย่างกรุงเทพ
lat = 13.7563
lon = 100.5018

if st.button("วิเคราะห์สภาพอากาศ"):

    weather_info = get_weather_data(lat, lon)

    st.subheader("ข้อมูลปัจจุบัน")
    st.write(f"🌡️ อุณหภูมิ: {weather_info['temperature']} °C")
    st.write(f"💧 ความชื้น: {weather_info['humidity']} %")
    st.write(f"🌧️ ฝน 1 ชม.: {weather_info['totalraintoday']} mm")

    result = analyze_weather(weather_info)

    st.subheader("📊 ผลการวิเคราะห์ AI")
    st.write(result)

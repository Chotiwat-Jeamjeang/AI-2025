import streamlit as st
import json
from weather_scraper import get_weather_data
from ai_analyzer import analyze_weather

st.set_page_config(
    page_title="AI Weather Risk",
    layout="centered"
)

st.title("🌧️ AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

with open("provinces.json") as f:
    provinces = json.load(f)

province = st.selectbox("เลือกจังหวัด", list(provinces.keys()))

if st.button("วิเคราะห์"):
    slug = provinces[province]

    with st.spinner("กำลังดึงข้อมูล..."):
        data = get_weather_data(slug)

    st.write("ข้อมูลล่าสุด:", data)

    with st.spinner("AI กำลังวิเคราะห์..."):
        result = analyze_weather(data)

    st.markdown("### ผลวิเคราะห์")
    st.write(result)

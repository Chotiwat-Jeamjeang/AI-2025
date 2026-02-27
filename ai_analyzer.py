from google import genai
import streamlit as st

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:
    อุณหภูมิ: {weather_info.get('temperature')}
    ฝนสะสมวันนี้: {weather_info.get('totalraintoday')}
    ความชื้น: {weather_info.get('humidity')}

    ประเมินความเสี่ยงและให้คำแนะนำสั้น ๆ
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )

    return response.text

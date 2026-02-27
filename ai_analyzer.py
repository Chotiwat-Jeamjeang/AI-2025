import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-flash")

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:
    อุณหภูมิ: {weather_info.get('temperature')}
    ฝนสะสมวันนี้: {weather_info.get('totalraintoday')}
    ความชื้น: {weather_info.get('humidity')}

    ประเมินความเสี่ยงและให้คำแนะนำสั้น ๆ
    """

    response = model.generate_content(prompt)

    return response.text

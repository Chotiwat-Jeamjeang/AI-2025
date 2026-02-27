import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์:
    Temp {weather_info.get('temperature')}
    Rain {weather_info.get('totalraintoday')}
    Humidity {weather_info.get('humidity')}
    ให้คำแนะนำสั้น ๆ
    """

    response = model.generate_content(prompt)

    return response.text

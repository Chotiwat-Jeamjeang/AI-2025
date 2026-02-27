import requests
import streamlit as st

HF_API_KEY = st.secrets["HF_API_KEY"]

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def analyze_weather(weather_info):

    prompt = f"""
คุณเป็นผู้เชี่ยวชาญด้านอุตุนิยมวิทยา

ข้อมูลสภาพอากาศ:
- อุณหภูมิ: {weather_info['temperature']} °C
- ปริมาณฝน 1 วัน: {weather_info['totalraintoday']} mm
- ความชื้น: {weather_info['humidity']} %

กรุณา:
1. ประเมินระดับความเสี่ยง (ต่ำ / ปานกลาง / สูง)
2. อธิบายเหตุผล
3. ให้คำแนะนำประชาชน

ตอบเป็นภาษาไทย
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.3
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        return f"เกิดข้อผิดพลาด: {response.text}"

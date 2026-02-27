import requests
import streamlit as st

HF_API_KEY = st.secrets["HF_API_KEY"]

API_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:
    อุณหภูมิ : {weather_info['temperature']}
    ฝนสะสมวันนี้ : {weather_info['totalraintoday']}
    ความชื้นสัมพัทธ์ : {weather_info['humidity']}

    ประเมินความเสี่ยงและให้คำแนะนำ
    """

    payload = {
        "inputs": prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response
er`

    result = response.json()
    return result[0]["generated_text"]

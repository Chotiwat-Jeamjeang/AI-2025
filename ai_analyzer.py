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
    วิเคราะห์ข้อมูล:
    อุณหภูมิ: {weather_info['temperature']}
    ฝนสะสมวันนี้: {weather_info['totalraintoday']}
    ความชื้น: {weather_info['humidity']}

    ประเมินความเสี่ยงและให้คำแนะนำ
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]

    return "ไม่สามารถวิเคราะห์ได้"

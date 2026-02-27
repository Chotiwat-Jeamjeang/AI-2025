import requests
import streamlit as st

API_URL = "https://router.huggingface.co"
headers = {
    "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
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
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.4
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"เกิดข้อผิดพลาด: {response.text}"

    result = response.json()
    return result[0]["generated_text"]

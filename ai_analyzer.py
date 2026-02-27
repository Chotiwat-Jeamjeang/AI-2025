from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:
    อุณหภูมิ : {weather_info['temperature']}
    ฝนสะสมวันนี้ : {weather_info['totalraintoday']}
    ความชื้นสัมพัทธ์ : {weather_info['humidity']}

    ประเมินความเสี่ยงและให้คำแนะนำ
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "คุณเป็นผู้เชี่ยวชาญด้านอุตุนิยมวิทยา"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

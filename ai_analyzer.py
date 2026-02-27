from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def analyze_weather(weather_info):

    prompt = f"""
    ข้อมูลสภาพอากาศปัจจุบัน:

    - อุณหภูมิ: {weather_info['temperature']} °C
    - ปริมาณฝน 1 ชั่วโมง: {weather_info['totalraintoday']} mm
    - ความชื้นสัมพัทธ์: {weather_info['humidity']} %

    กรุณา:
    1. ประเมินระดับความเสี่ยงเป็น 3 ระดับ (ต่ำ / ปานกลาง / สูง)
    2. อธิบายเหตุผลสั้น ๆ
    3. ให้คำแนะนำประชาชน

    ตอบเป็นภาษาไทย
    จัดรูปแบบให้อ่านง่าย
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "คุณเป็นผู้เชี่ยวชาญด้านอุตุนิยมวิทยาและการประเมินความเสี่ยงภัยธรรมชาติ"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

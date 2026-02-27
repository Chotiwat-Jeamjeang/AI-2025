from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def analyze_weather(weather_data):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:
    อุณหภูมิ: {weather_data['temperature']}
    ปริมาณฝน: {weather_data['rainfall']}
    รายละเอียด: {weather_data['description']}

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

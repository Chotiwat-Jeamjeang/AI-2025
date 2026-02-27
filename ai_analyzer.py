from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def analyze_weather(weather_info):

    prompt = f"""
    วิเคราะห์ข้อมูลสภาพอากาศ:

    อุณหภูมิ : {weather_info.get('temperature', 'ไม่มีข้อมูล')}
    ฝนสะสมวันนี้ : {weather_info.get('totalraintoday', 'ไม่มีข้อมูล')}
    ความชื้นสัมพัทธ์ : {weather_info.get('humidity', 'ไม่มีข้อมูล')}

    โปรด:
    1. ประเมินระดับความเสี่ยง (ต่ำ / ปานกลาง / สูง)
    2. อธิบายสาเหตุ
    3. ให้คำแนะนำที่ประชาชนควรปฏิบัติ
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "คุณเป็นผู้เชี่ยวชาญด้านอุตุนิยมวิทยา"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"เกิดข้อผิดพลาดในการวิเคราะห์: {e}"

import streamlit as st
import requests

# =========================
# 🔐 OpenWeather API KEY
# =========================
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# =========================
# 🌍 จังหวัด
# =========================
PROVINCES = {
    "กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
    "เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
    "ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
    "ภูเก็ต": {"lat": 7.8804, "lon": 98.3923},
    "ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
}

# =========================
# 🌤 ดึงข้อมูลอากาศ
# =========================
def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
        f"&lang=th"
    )

    response = requests.get(url)
    data = response.json()

    # เช็ค error จาก API
    if response.status_code != 200:
        return None, data

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rain": data.get("rain", {}).get("1h", 0)
    }

    return weather, None


# =========================
# 🎨 UI
# =========================
st.set_page_config(page_title="Weather App")
st.title("🌦 แสดงข้อมูลสภาพอากาศ")

province = st.selectbox("เลือกจังหวัด", list(PROVINCES.keys()))

if st.button("ดึงข้อมูลอากาศ"):

    lat = PROVINCES[province]["lat"]
    lon = PROVINCES[province]["lon"]

    weather, error = get_weather(lat, lon)

    if error:
        st.error(f"❌ เกิดข้อผิดพลาด: {error}")
    else:
        st.subheader("📊 ข้อมูลปัจจุบัน")
        st.write(f"🌡 อุณหภูมิ: {weather['temperature']} °C")
        st.write(f"💧 ความชื้น: {weather['humidity']} %")
        st.write(f"🌧 ฝน 1 ชม.: {weather['rain']} mm")

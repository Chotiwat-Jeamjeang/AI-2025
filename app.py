import streamlit as st
import requests

# =========================
# 🔐 OpenWeather API KEY
# =========================
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# =========================
# 🌍 จังหวัด (ตัวอย่างหลัก ๆ)
# =========================
PROVINCES = {
    "กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
    "เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
    "ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
    "ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
    "ภูเก็ต": {"lat": 7.8804, "lon": 98.3923},
    "นครราชสีมา": {"lat": 14.9799, "lon": 102.0977},
    "สงขลา": {"lat": 7.1898, "lon": 100.5951},
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

    if response.status_code != 200:
        return None, response.text

    data = response.json()

    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "rain": data.get("rain", {}).get("1h", 0),
    }

    return weather, None


# =========================
# 🧠 Risk Engine (ฉลาดขึ้น)
# =========================
def analyze_weather(weather):
    score = 0
    reasons = []

    temp = weather["temperature"]
    feels = weather["feels_like"]
    humidity = weather["humidity"]
    rain = weather["rain"]
    wind = weather["wind"]

    # 🔥 อากาศร้อน
    if feels >= 40:
        score += 3
        reasons.append("อากาศร้อนจัดมาก")
    elif feels >= 35:
        score += 2
        reasons.append("อากาศร้อนและอบอ้าว")
    elif feels >= 32:
        score += 1
        reasons.append("เริ่มร้อน")

    # 💧 ความชื้นสูง
    if humidity >= 85:
        score += 2
        reasons.append("ความชื้นสูงมาก")
    elif humidity >= 75:
        score += 1
        reasons.append("ความชื้นค่อนข้างสูง")

    # 🌧 ฝน
    if rain >= 20:
        score += 3
        reasons.append("ฝนตกหนัก")
    elif rain >= 5:
        score += 1
        reasons.append("มีฝนตก")

    # 💨 ลมแรง
    if wind >= 10:
        score += 1
        reasons.append("ลมค่อนข้างแรง")

    # 🎯 สรุประดับความเสี่ยง
    if score >= 6:
        level = "🔴 ความเสี่ยงสูง"
        advice = "ควรหลีกเลี่ยงกิจกรรมกลางแจ้ง ดื่มน้ำมาก ๆ และติดตามข่าวอากาศ"
    elif score >= 3:
        level = "🟠 ความเสี่ยงปานกลาง"
        advice = "ควรเตรียมร่มและพักผ่อนให้เพียงพอ"
    else:
        level = "🟢 ความเสี่ยงต่ำ"
        advice = "สภาพอากาศปกติ สามารถทำกิจกรรมได้ตามปกติ"

    return level, advice, reasons


# =========================
# 🎨 UI
# =========================
st.set_page_config(page_title="AI วิเคราะห์ความเสี่ยงสภาพอากาศ")
st.title("🌦 AI วิเคราะห์ความเสี่ยงสภาพอากาศ (ไม่ใช้ AI API)")

province = st.selectbox("เลือกจังหวัด", list(PROVINCES.keys()))

if st.button("วิเคราะห์สภาพอากาศ"):

    lat = PROVINCES[province]["lat"]
    lon = PROVINCES[province]["lon"]

    weather, error = get_weather(lat, lon)

    if error:
        st.error(f"❌ ไม่สามารถดึงข้อมูลได้: {error}")
    else:
        st.subheader("📊 ข้อมูลปัจจุบัน")

        st.write(f"📍 เมือง: {weather['city']}")
        st.write(f"🌡 อุณหภูมิ: {weather['temperature']} °C")
        st.write(f"🤒 รู้สึกเหมือน: {weather['feels_like']} °C")
        st.write(f"💧 ความชื้น: {weather['humidity']} %")
        st.write(f"🌧 ฝน 1 ชม.: {weather['rain']} mm")
        st.write(f"💨 ลม: {weather['wind']} m/s")
        st.write(f"☁️ สภาพอากาศ: {weather['description']}")

        level, advice, reasons = analyze_weather(weather)

        st.subheader("📈 ผลการวิเคราะห์ความเสี่ยง")
        st.write(level)

        if reasons:
            st.write("🔎 ปัจจัยที่มีผล:")
            for r in reasons:
                st.write(f"- {r}")

        st.info(advice)

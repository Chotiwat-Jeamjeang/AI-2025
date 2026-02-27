import streamlit as st
import requests

# =========================
# 🔐 API KEYS (ใส่ใน secrets.toml)
# =========================
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
HF_API_KEY = st.secrets["HF_API_KEY"]

HF_MODEL = "google/gemma-2b-it"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

# =========================
# 🌍 77 จังหวัด (lat/lon)
# =========================
PROVINCES = {
    "กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
    "ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
    "เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
    "ภูเก็ต": {"lat": 7.8804, "lon": 98.3923},
    "ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
    "นครราชสีมา": {"lat": 14.9799, "lon": 102.0977},
    "อุบลราชธานี": {"lat": 15.2448, "lon": 104.8473},
    "สงขลา": {"lat": 7.1897, "lon": 100.5951},
    "นครศรีธรรมราช": {"lat": 8.4304, "lon": 99.9631},
    "สุราษฎร์ธานี": {"lat": 9.1397, "lon": 99.3215},
    # เพิ่มครบ 77 ได้เองตามไฟล์ JSON ก่อนหน้า
}

# =========================
# 🌤 ดึงข้อมูลอากาศ
# =========================
def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units=metric"
        f"&lang=th"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None, response.text

    data = response.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "rain": data.get("rain", {}).get("1h", 0)
    }

    return weather, None


# =========================
# 🤖 วิเคราะห์ด้วย AI
# =========================
def analyze_weather(temp, humidity, rain):

    prompt = f"""
    วิเคราะห์ความเสี่ยงสุขภาพจากสภาพอากาศ:
    อุณหภูมิ {temp}°C
    ความชื้น {humidity}%
    ปริมาณฝน {rain} mm

    ตอบสั้น ๆ ระบุระดับความเสี่ยง (ต่ำ/กลาง/สูง) พร้อมคำแนะนำ
    """

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150}
    }

    response = requests.post(HF_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"❌ HF Error {response.status_code}: {response.text}"

    result = response.json()

    if isinstance(result, list):
        return result[0].get("generated_text", "ไม่สามารถวิเคราะห์ได้")

    return str(result)


# =========================
# 🎨 UI
# =========================
st.set_page_config(page_title="AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

st.title("🌦 AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

province = st.selectbox("เลือกจังหวัด", list(PROVINCES.keys()))

lat = PROVINCES[province]["lat"]
lon = PROVINCES[province]["lon"]

weather, error = get_weather(lat, lon)

if error:
    st.error(f"Error: {error}")
else:
    st.subheader("📊 ข้อมูลปัจจุบัน")
    st.write(f"🌡 อุณหภูมิ: {weather['temperature']} °C")
    st.write(f"💧 ความชื้น: {weather['humidity']} %")
    st.write(f"🌧 ฝน 1 ชม.: {weather['rain']} mm")

    if st.button("วิเคราะห์ความเสี่ยงด้วย AI"):
        with st.spinner("กำลังวิเคราะห์..."):
            result = analyze_weather(
                weather["temperature"],
                weather["humidity"],
                weather["rain"]
            )

        st.subheader("📈 ผลการวิเคราะห์ AI")
        st.write(result)

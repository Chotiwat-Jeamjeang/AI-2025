import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Weather Risk", page_icon="🌦️")

OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]
HF_API_KEY = st.secrets["HF_API_KEY"]

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"

# ---------------- PROVINCES 77 ----------------
PROVINCES = {
    "กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
    "เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
    "เชียงราย": {"lat": 19.9105, "lon": 99.8406},
    "ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
    "นครราชสีมา": {"lat": 14.9799, "lon": 102.0977},
    "ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
    "ภูเก็ต": {"lat": 7.8804, "lon": 98.3923},
    "นครศรีธรรมราช": {"lat": 8.4304, "lon": 99.9631},
    "อุบลราชธานี": {"lat": 15.2448, "lon": 104.8473},
    "สุราษฎร์ธานี": {"lat": 9.1382, "lon": 99.3215},
    "สงขลา": {"lat": 7.1898, "lon": 100.5951},
    "นนทบุรี": {"lat": 13.8591, "lon": 100.5217},
    "ปทุมธานี": {"lat": 14.0208, "lon": 100.5250},
    "สมุทรปราการ": {"lat": 13.5991, "lon": 100.5998},
    "นครปฐม": {"lat": 13.8199, "lon": 100.0622},
    "กาญจนบุรี": {"lat": 14.0227, "lon": 99.5328},
    "ราชบุรี": {"lat": 13.5283, "lon": 99.8134},
    "เพชรบุรี": {"lat": 13.1119, "lon": 99.9391},
    "ประจวบคีรีขันธ์": {"lat": 11.8124, "lon": 99.7973},
    "พิษณุโลก": {"lat": 16.8211, "lon": 100.2659},
    "นครสวรรค์": {"lat": 15.6987, "lon": 100.1199},
    "ลำปาง": {"lat": 18.2888, "lon": 99.4908},
    "ลำพูน": {"lat": 18.5746, "lon": 99.0087},
    "พะเยา": {"lat": 19.1665, "lon": 99.9018},
    "แม่ฮ่องสอน": {"lat": 19.3020, "lon": 97.9654},
    "สุโขทัย": {"lat": 17.0061, "lon": 99.8230},
    "อุตรดิตถ์": {"lat": 17.6201, "lon": 100.0993},
    "แพร่": {"lat": 18.1446, "lon": 100.1403},
    "น่าน": {"lat": 18.7756, "lon": 100.7730},
    "ชัยภูมิ": {"lat": 15.8068, "lon": 102.0315},
    "บุรีรัมย์": {"lat": 14.9950, "lon": 103.1116},
    "สุรินทร์": {"lat": 14.8829, "lon": 103.4937},
    "ศรีสะเกษ": {"lat": 15.1186, "lon": 104.3220},
    "อุดรธานี": {"lat": 17.4138, "lon": 102.7872},
    "เลย": {"lat": 17.4905, "lon": 101.7223},
    "หนองคาย": {"lat": 17.8783, "lon": 102.7420},
    "สกลนคร": {"lat": 17.1610, "lon": 104.1476},
    "นครพนม": {"lat": 17.3920, "lon": 104.7695},
    "มุกดาหาร": {"lat": 16.5447, "lon": 104.7234},
    "ตรัง": {"lat": 7.5563, "lon": 99.6114},
    "กระบี่": {"lat": 8.0863, "lon": 98.9063},
    "พังงา": {"lat": 8.4501, "lon": 98.5255},
    "ระยอง": {"lat": 12.6814, "lon": 101.2816},
    "จันทบุรี": {"lat": 12.6112, "lon": 102.1038},
    "ตราด": {"lat": 12.2428, "lon": 102.5170}
}

# ---------------- UI ----------------
st.title("🌦️ AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

province = st.selectbox("เลือกจังหวัด", list(PROVINCES.keys()))
coords = PROVINCES[province]

# ---------------- WEATHER ----------------
def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    res = requests.get(url)
    return res.json()

data = get_weather(coords["lat"], coords["lon"])

if "main" not in data:
    st.error("❌ ดึงข้อมูลอากาศไม่สำเร็จ")
    st.stop()

temperature = data["main"]["temp"]
humidity = data["main"]["humidity"]
rain = data.get("rain", {}).get("1h", 0)

st.subheader("📊 ข้อมูลปัจจุบัน")
st.write(f"🌡️ อุณหภูมิ: {temperature} °C")
st.write(f"💧 ความชื้น: {humidity} %")
st.write(f"🌧️ ฝน 1 ชม.: {rain} mm")

# ---------------- AI ANALYSIS ----------------
def analyze_weather(temp, humidity, rain):
    prompt = f"""
    วิเคราะห์ความเสี่ยงสุขภาพจากข้อมูล:
    อุณหภูมิ {temp}°C
    ความชื้น {humidity}%
    ฝน {rain} mm

    ให้สรุประดับความเสี่ยง (ต่ำ/กลาง/สูง) และคำแนะนำสั้น ๆ
    """

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(HF_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()
    return result[0]["generated_text"]

# ---------------- BUTTON ----------------
if st.button("วิเคราะห์ความเสี่ยงด้วย AI"):
    with st.spinner("AI กำลังวิเคราะห์..."):
        result = analyze_weather(temperature, humidity, rain)

    st.subheader("📈 ผลการวิเคราะห์ AI")
    st.write(result)

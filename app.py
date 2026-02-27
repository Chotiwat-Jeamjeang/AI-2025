import streamlit as st
import requests

# =========================
# 🔐 OpenWeather API KEY (ใส่ใน secrets.toml)
# =========================
OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# =========================
# 🌍 จังหวัด (ตัวอย่างหลัก ๆ เพิ่มได้เอง)
# =========================
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
# 🤖 AI จำลอง (Rule-based Risk Engine)
# =========================
def analyze_weather(temp, humidity, rain):

    score = 0

    # อุณหภูมิ
    if temp > 35:
        score += 2
    elif temp > 32:
        score += 1

    # ความชื้น
    if humidity > 85:
        score += 2
    elif humidity > 75:
        score += 1

    # ปริมาณฝน
    if rain > 20:
        score += 3
    elif rain > 5:
        score += 1

    # แปลงคะแนนเป็นระดับความเสี่ยง
    if score >= 5:
        level = "🔴 ความเสี่ยงสูง"
        advice = "ควรหลีกเลี่ยงกิจกรรมกลางแจ้ง ระวังน้ำท่วม และดูแลสุขภาพ"
    elif score >= 3:
        level = "🟠 ความเสี่ยงปานกลาง"
        advice = "ควรเตรียมร่ม ดื่มน้ำมาก ๆ และติดตามพยากรณ์อากาศ"
    else:
        level = "🟢 ความเสี่ยงต่ำ"
        advice = "สภาพอากาศปกติ สามารถทำกิจกรรมได้ตามปกติ"

    return level, advice


# =========================
# 🎨 UI
# =========================
st.set_page_config(page_title="AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

st.title("🌦 AI วิเคราะห์ความเสี่ยงสภาพอากาศ (ไม่ใช้ API AI)")

province = st.selectbox("เลือกจังหวัด", list(PROVINCES.keys()))

if st.button("วิเคราะห์สภาพอากาศ"):

    lat = PROVINCES[province]["lat"]
    lon = PROVINCES[province]["lon"]

    weather, error = get_weather(lat, lon)

    if error:
        st.error(f"❌ ไม่สามารถดึงข้อมูลสภาพอากาศได้: {error}")
    else:
        st.subheader("📊 ข้อมูลปัจจุบัน")
        st.write(f"🌡 อุณหภูมิ: {weather['temperature']} °C")
        st.write(f"💧 ความชื้น: {weather['humidity']} %")
        st.write(f"🌧 ฝน 1 ชม.: {weather['rain']} mm")

        level, advice = analyze_weather(
            weather["temperature"],
            weather["humidity"],
            weather["rain"]
        )

        st.subheader("📈 ผลการวิเคราะห์ความเสี่ยง")
        st.write(level)
        st.info(advice)

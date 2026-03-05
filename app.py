import streamlit as st
import requests

# =========================
# 🔐 OpenWeather API KEY
# =========================
API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# =========================
# 🌍 จังหวัด (ตัวอย่างหลัก ๆ)
# =========================
PROVINCES = PROVINCES = {
"กรุงเทพมหานคร": {"lat": 13.7563, "lon": 100.5018},
"กระบี่": {"lat": 8.0863, "lon": 98.9063},
"กาญจนบุรี": {"lat": 14.0228, "lon": 99.5328},
"กาฬสินธุ์": {"lat": 16.4314, "lon": 103.5059},
"กำแพงเพชร": {"lat": 16.4834, "lon": 99.5227},
"ขอนแก่น": {"lat": 16.4322, "lon": 102.8236},
"จันทบุรี": {"lat": 12.6113, "lon": 102.1038},
"ฉะเชิงเทรา": {"lat": 13.6904, "lon": 101.0779},
"ชลบุรี": {"lat": 13.3611, "lon": 100.9847},
"ชัยนาท": {"lat": 15.1852, "lon": 100.1251},
"ชัยภูมิ": {"lat": 15.8068, "lon": 102.0315},
"ชุมพร": {"lat": 10.4930, "lon": 99.1800},
"เชียงราย": {"lat": 19.9105, "lon": 99.8406},
"เชียงใหม่": {"lat": 18.7883, "lon": 98.9853},
"ตรัง": {"lat": 7.5563, "lon": 99.6114},
"ตราด": {"lat": 12.2436, "lon": 102.5175},
"ตาก": {"lat": 16.8697, "lon": 99.1286},
"นครนายก": {"lat": 14.2069, "lon": 101.2130},
"นครปฐม": {"lat": 13.8199, "lon": 100.0622},
"นครพนม": {"lat": 17.3920, "lon": 104.7695},
"นครราชสีมา": {"lat": 14.9799, "lon": 102.0977},
"นครศรีธรรมราช": {"lat": 8.4304, "lon": 99.9631},
"นครสวรรค์": {"lat": 15.7047, "lon": 100.1372},
"นนทบุรี": {"lat": 13.8621, "lon": 100.5144},
"นราธิวาส": {"lat": 6.4255, "lon": 101.8253},
"น่าน": {"lat": 18.7756, "lon": 100.7789},
"บึงกาฬ": {"lat": 18.3609, "lon": 103.6464},
"บุรีรัมย์": {"lat": 14.9930, "lon": 103.1029},
"ปทุมธานี": {"lat": 14.0208, "lon": 100.5250},
"ประจวบคีรีขันธ์": {"lat": 11.8124, "lon": 99.7973},
"ปราจีนบุรี": {"lat": 14.0509, "lon": 101.3686},
"ปัตตานี": {"lat": 6.8695, "lon": 101.2505},
"พระนครศรีอยุธยา": {"lat": 14.3532, "lon": 100.5689},
"พะเยา": {"lat": 19.1667, "lon": 99.9000},
"พังงา": {"lat": 8.4501, "lon": 98.5255},
"พัทลุง": {"lat": 7.6167, "lon": 100.0833},
"พิจิตร": {"lat": 16.4419, "lon": 100.3488},
"พิษณุโลก": {"lat": 16.8211, "lon": 100.2659},
"เพชรบุรี": {"lat": 13.1119, "lon": 99.9391},
"เพชรบูรณ์": {"lat": 16.4189, "lon": 101.1550},
"แพร่": {"lat": 18.1446, "lon": 100.1403},
"ภูเก็ต": {"lat": 7.8804, "lon": 98.3923},
"มหาสารคาม": {"lat": 16.1843, "lon": 103.3026},
"มุกดาหาร": {"lat": 16.5436, "lon": 104.7209},
"แม่ฮ่องสอน": {"lat": 19.3020, "lon": 97.9654},
"ยโสธร": {"lat": 15.7941, "lon": 104.1451},
"ยะลา": {"lat": 6.5411, "lon": 101.2804},
"ร้อยเอ็ด": {"lat": 16.0538, "lon": 103.6520},
"ระนอง": {"lat": 9.9529, "lon": 98.6085},
"ระยอง": {"lat": 12.6814, "lon": 101.2810},
"ราชบุรี": {"lat": 13.5283, "lon": 99.8134},
"ลพบุรี": {"lat": 14.7995, "lon": 100.6534},
"ลำปาง": {"lat": 18.2923, "lon": 99.4928},
"ลำพูน": {"lat": 18.5746, "lon": 99.0087},
"เลย": {"lat": 17.4905, "lon": 101.7223},
"ศรีสะเกษ": {"lat": 15.1186, "lon": 104.3294},
"สกลนคร": {"lat": 17.1611, "lon": 104.1476},
"สงขลา": {"lat": 7.1898, "lon": 100.5951},
"สตูล": {"lat": 6.6238, "lon": 100.0674},
"สมุทรปราการ": {"lat": 13.5991, "lon": 100.5998},
"สมุทรสงคราม": {"lat": 13.4146, "lon": 100.0023},
"สมุทรสาคร": {"lat": 13.5475, "lon": 100.2740},
"สระแก้ว": {"lat": 13.8240, "lon": 102.0646},
"สระบุรี": {"lat": 14.5289, "lon": 100.9101},
"สิงห์บุรี": {"lat": 14.8936, "lon": 100.3967},
"สุโขทัย": {"lat": 17.0068, "lon": 99.8230},
"สุพรรณบุรี": {"lat": 14.4745, "lon": 100.1177},
"สุราษฎร์ธานี": {"lat": 9.1397, "lon": 99.3215},
"สุรินทร์": {"lat": 14.8829, "lon": 103.4937},
"หนองคาย": {"lat": 17.8783, "lon": 102.7413},
"หนองบัวลำภู": {"lat": 17.2040, "lon": 102.4260},
"อ่างทอง": {"lat": 14.5896, "lon": 100.4551},
"อำนาจเจริญ": {"lat": 15.8657, "lon": 104.6258},
"อุดรธานี": {"lat": 17.4138, "lon": 102.7872},
"อุตรดิตถ์": {"lat": 17.6201, "lon": 100.0993},
"อุทัยธานี": {"lat": 15.3835, "lon": 100.0246},
"อุบลราชธานี": {"lat": 15.2448, "lon": 104.8473}
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
st.title("🌦 AI วิเคราะห์ความเสี่ยงสภาพอากาศ")

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

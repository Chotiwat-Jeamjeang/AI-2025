def analyze_weather(weather):

    temp = float(weather["temperature"])
    humidity = float(weather["humidity"])
    rain = float(weather["rain"])

    risk_score = 0

    # ประเมินอุณหภูมิ
    if temp >= 38:
        risk_score += 3
    elif temp >= 35:
        risk_score += 2
    elif temp >= 32:
        risk_score += 1

    # ประเมินความชื้น
    if humidity >= 85:
        risk_score += 2
    elif humidity >= 70:
        risk_score += 1

    # ประเมินฝน
    if rain >= 50:
        risk_score += 3
    elif rain >= 20:
        risk_score += 2
    elif rain > 0:
        risk_score += 1

    # สรุประดับความเสี่ยง
    if risk_score >= 6:
        level = "🔴 ความเสี่ยงสูง"
        advice = "ควรหลีกเลี่ยงกิจกรรมกลางแจ้ง และติดตามประกาศเตือนภัย"
    elif risk_score >= 3:
        level = "🟡 ความเสี่ยงปานกลาง"
        advice = "ควรเตรียมอุปกรณ์กันฝนและดูแลสุขภาพ"
    else:
        level = "🟢 ความเสี่ยงต่ำ"
        advice = "สภาพอากาศปกติ สามารถทำกิจกรรมได้"

    return f"""
### 📊 ระดับความเสี่ยง: {level}

🌡 อุณหภูมิ: {temp} °C  
💧 ความชื้น: {humidity} %  
🌧 ปริมาณฝน: {rain} mm  

💡 คำแนะนำ: {advice}
"""

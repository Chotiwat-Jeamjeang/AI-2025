async function getWeather(){

let city=document.getElementById("city").value

let api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=dcf3065ebffb68296e7a61c6d278c3a0&units=metric"

let res=await fetch(api)

let data=await res.json()

let temp=data.main.temp
let humidity=data.main.humidity

let risk="ต่ำ"

if(temp>35 || humidity>80){
risk="สูง"
}

document.getElementById("result").innerHTML=

`
อุณหภูมิ : ${temp} °C<br>
ความชื้น : ${humidity}%<br>
ความเสี่ยง : ${risk}
`

}

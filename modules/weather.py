import requests
from config import OPENWEATHER_API_KEY

def get_weather(city="Pune"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res["cod"] != 200:
            return f"Couldn't get weather for {city}."
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}."
    except Exception as e:
        print("❌ Weather Error:", e)
        return "Unable to fetch weather information right now."

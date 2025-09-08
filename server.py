from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
from random import randint
app = FastAPI()

@app.get("/my-ip")
async def get_ip(request: Request):
    return {"ip": request.client.host}

############################################

# that's the api key in the "https://home.openweathermap.org/"
# We nead that key to have access to data collection
API_KEY = "49dc213648657bf08fe94b7682ed4c0b"

class Location(BaseModel):
    location : str
@app.post("/weather")
def get_weather(data: Location):
    try:
        city = data.location
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        res = requests.get(url)

        if res.status_code != 200:
            print(0)
            return {"error": f"OpenWeather error: {res.status_code}", "details": res.text}

        res = res.json()

        return {
            "temperature": res["main"]["temp"],
            "humidity": res["main"]["humidity"],
        }
    except:
        print(1)
        return {"error": "Invalid location"}

####################################

quotes = [
    "Believe you can and you're halfway there.",
    "Do one thing every day that scares you.",
    "Your limitation—it’s only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It’s going to be hard, but hard does not mean impossible.",
    "Don’t wait for opportunity. Create it.",
    "Sometimes we’re tested not to show our weaknesses, but to discover our strengths.",
    "The key to success is to focus on goals, not obstacles.",
    "Dream it. Believe it. Build it.",
    "Doubt kills more dreams than failure ever will.",
    "Act as if what you do makes a difference. It does."
]


@app.get("/quote")
def get_quote():
    index = randint(0, len(quotes) - 1)
    return {"quote": quotes[index]}
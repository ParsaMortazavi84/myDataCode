from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
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

@app.get("/quote")
def get_quote():

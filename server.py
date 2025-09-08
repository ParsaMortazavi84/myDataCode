from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import requests
from random import randint
import time
import json

from starlette.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.time()
    log_data = {
        "ip": request.client.host,
        "method": request.method,
        "url" :  str(request.url),
    }

    response = await call_next(request)

    log_data["status_code"] = response.status_code
    log_data["duration"] = round(time.time() - start_time, 4)

    with open("requests_log.json", "a") as f:
        f.write(json.dumps(log_data) + "\n")

    return response


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

    city = data.location
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    res = requests.get(url)

    if res.status_code != 200:
        return {"error": f"OpenWeather error: {res.status_code}", "details": res.text}

    res = res.json()

    return {
        "location": city,
        "temperature": res["main"]["temp"],
        "humidity": res["main"]["humidity"],
    }

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

@app.add_exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )
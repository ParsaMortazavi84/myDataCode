from inspirational_quotes import quote
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import BaseModel
import requests
from random import randint
import time
import json
from starlette.responses import JSONResponse
from requests import RequestException

logger.add(""
           "logs/server.log",
           rotation="10MB",
           retention="7 days",
           compression="zip",

)


app = FastAPI()

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = time.time()
    ## log request
    logger.info(f"Request: {request.method} {request.url}")

    ##log response
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.url} {response.status_code} {duration:.2f}s")
        return response

    except HTTPException as exc:
        logger.error(f"HTTPException: {exc.detail}")

    except RequestValidationError as exc:
        logger.error(f"RequestException: {exc.errors()}")

    except RequestException as exc:
        logger.error(f"Unexpected exception")



    return response

############################################

@app.get("/my-ip")
async def get_ip(request: Request):
    return {"ip": request.client.host}

############################################

# that's the api key in the "https://home.openweathermap.org/"
# We nead that key to have access to data collection
file = open("myApiKey.txt", "r")
API_KEY = file.read()

class Location(BaseModel):
    location : str
@app.post("/weather")
def get_weather(data: Location):

    city = data.location
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    # when we want to send sequest to a another server
    res = requests.get(url)
    res = res.json()
    response = {
        "location": city,
        "temperature": res["main"]["temp"],
        "humidity": res["main"]["humidity"],
    }
    return response

############################################


@app.get("/quote")
def get_quote():
    ins_quote = quote()
    return ins_quote


############################################



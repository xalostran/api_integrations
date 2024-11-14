from smart_api import autentication, apis, commands
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

"""klass konvertering"""
app = FastAPI()
autent = autentication.Autent()
api = apis.API()
cmd = commands.Commands()

"""funktions konvertering"""
location_list = cmd.location_cmd()
lock_list = cmd.locks_cmd()
lamp_list = cmd. lamps_cmd()


"""klasser med variabler för att användaren ska skicka data i request body"""
class UserCred(BaseModel):
    username: str
    password: str

class GetValues(BaseModel):
    place: str
    key: str 

class TempValue(BaseModel):
    temp: str


class LockStatus(str, Enum):
    """klass av typen enum för att användaren endast ska kunna sätta låsen till open/closed"""
    open = "open"
    closed = "closed"

class LockValue(BaseModel):
    locks: LockStatus


class LampStatus(str, Enum):
    """klass av typen enum för att användaren endast ska kunna sätta lamporna till on/off"""
    off = "off"
    on = "on"

class LampValue(BaseModel):
    lamps_: LampStatus



@app.post('/login')
async def postapi(credentials: UserCred):
    """logga in för att få api nyckel"""

    username = credentials.username
    password = credentials.password
    api_key = autent.get_key(username, password)
    if api_key:
        return {"Your API key": api_key}
        
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")
    

@app.post('/location')
async def locate(credentials: GetValues):
    """hitta koordinater för användarens hus"""

    key = credentials.key
    place = credentials.place
    location_api = api.get_location(place)
    print(key)
    print(autent.api_key)
    if key == autent.api_key:
        if place.capitalize() in location_list.keys():
                return{"location": location_api}
        else:
            return{"Error": "Invalid or non-accessible area"}
    else:
        return{"Error": "Invalid api"}


@app.post('/temp/get')
async def get_temperature(credentials: GetValues):
    """ta reda på temperatur data"""

    key = credentials.key
    place = credentials.place
    weather_api = api.get_weather(place)

    if key == autent.api_key:
        if place.capitalize() in location_list.keys():
            temp = location_list[place.capitalize()]
            return{
                "Status": weather_api,
                "Temperature indoor": temp
                } 
        else:
            return{"Error": "Invalid or non-accessible city"}
    else:
        return{"Error": "Invalid Key"}

  
@app.put('/temp/set')
async def set_temperature(credentials: GetValues, temp: TempValue):
    """ställ om temperaturen""" 

    key = credentials.key
    place = credentials.place
    #pylint: disable=global-statement

    if key == autent.api_key:
        if place.capitalize() in location_list.keys():
            location_list[place.capitalize()] = temp
            return{"Status": f"Temperature in your home at {place} is set to {temp}"}
        else:
            return{"Error": "Invalid or non-accessible area"}  
    else:
        return{"Error": "Invalid Key"}


@app.post('/locks/get')
async def get_locks(credentials: GetValues):
    """ta reda på låsens status"""

    key = credentials.key
    place = credentials.place

    if key == autent.api_key:
        if place.lower().capitalize() in location_list.keys():
            lock = lock_list[place.capitalize()]
            return{"Status": f"locks are {lock} in {place}"}
        else:
            return{"Status": "No such city"}
    else:
        return{"Error": "Invalid Key"}


@app.post('/locks/set')
async def set_locks(credentials: GetValues, set_lock: LockValue):
    """uppdatera låsens status"""

    key = credentials.key
    place = credentials.place
    
    if key == autent.api_key:
        if place.lower().capitalize() in location_list.keys():
            lock_list[place.capitalize()] = set_lock.locks.value
            return{"Status": f"locks are {set_lock.locks.value} in {place}"}
        else:
            return{"Error": "Invalid or non-accessible city"}
    else:
        return{"Error": "Invalid Key"}
    

@app.post('/lamps/get')
async def get_lamps(credentials:GetValues):
    """ta reda på lampornas status"""

    key = credentials.key
    place = credentials.place

    if key == autent.api_key:
        if place.lower().capitalize() in location_list.keys():
            lamp = lamp_list[place.capitalize()]
            return{"Status": f"lamps are {lamp} in {place}"}
        else:
            return{"Error": "Invalid or non-accessible city"}
    else:
        return{"Error": "Invalid Key"}
    

@app.put('/lamps/set')
async def set_lamps(credentials: GetValues, set_lamp: LampValue):
    """ställ om lampornas status"""

    key = credentials.key
    place = credentials.place

    if key == autent.api_key:
        if place.lower().capitalize() in location_list.keys():
            lamp_list[place.capitalize()] = set_lamp.lamps_.value
            return{"Status": f"lamps are {set_lamp.lamps_.value} in {place}"}
        else:
            return{"Error": "Invalid or non-accessible city"}
    else:
        return{"Error": "Invalid Key"}



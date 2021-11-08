from typing import Any, Optional, Literal
import typing

from fastapi import FastAPI
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dnacentersdk import DNACenterAPI



dnac = DNACenterAPI(base_url='https://10.9.11.226',
                            username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")
import create_site
print(dnac)
print(type(dnac))


# def create_area(area):
#     return area
class ChildArea(BaseModel):
    name: str
    parentName: str

class Area(BaseModel):
    area: ChildArea

class ChildBuilding(BaseModel):
    name: str
    parentName: str
    address: str

class Building(BaseModel):
    building: ChildBuilding

class ChildFloor(BaseModel):
    name: str
    parentName: str
    rfModel: str
    width: int
    length: int
    height: int

class Floor(BaseModel):
    floor: ChildFloor




class WebhookJsonModel(BaseModel):
    event: str
    timestamp: str
    model: str
    username: str
    request_id: str
    data: Obj
    snapshots: Obj

class WebhookResponseModel(BaseModel):
    message: Literal["Received site webhook from Netbox"]
    data: WebhookJsonModel

app = FastAPI()

# base test endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# #sites endpoint
# @app.post("/sites/", response_model=WebhookResponseModel)
# def sites(site_data: WebhookJsonModel):
#     create_area(site_data.data)
#     return {
#         "message": "Received site webhook from Netbox",
#         "data": site_data
#     }

@app.post("/area", status_code=201)
def create_area(area: Area):
    return create_site.create_area(dnac, area)

@app.post("/building", status_code=201)
def create_building(building: Building):
    return create_site.create_building(dnac, building)

@app.post("/floor", status_code=201)
def create_area(floor: Floor):
    return create_site.create_floor(dnac, floor)

@app.delete("/area", status_code=202)
def delete_area():
    return {"message": "deleting area"}
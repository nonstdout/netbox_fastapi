from typing import Any, Optional, Literal, List
from enum import Enum
import json

from fastapi import FastAPI
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dnacentersdk import DNACenterAPI



dnac = DNACenterAPI(base_url='https://10.9.11.226',
                            username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")
import create_site
import ip_pool


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

class GlobalPool(BaseModel):
    pool_name: str
    dhcp_servers: List[str]
    dns_servers: List[str]
    supernet: str

class PoolTypes(str, Enum):
    generic: "generic"
    LAN: "LAN"

class SubPool(BaseModel):
    site_id: str
    global_pool_name: str
    name: str
    type_: str
    ipv6AddressSpace: bool
    ipv4GlobalPool: str
    ipv4Prefix: bool
    ipv4PrefixLength: int
    ipv4Subnet: str
    ipv4GateWay: str
    ipv4DhcpServers: List[str]
    ipv4DnsServers: List[str]

class SiteID(BaseModel):
    site_id: str

class PoolName(BaseModel):
    pool_name: str

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

# future, delete single area
# @app.delete("/area", status_code=202)
# def delete_area():
#     return {"message": "deleting area"}

@app.post("/pool/global", status_code=201)
def create_global_pool(global_pool: GlobalPool):
    # convert object to dict so it can be unpacked
    global_pool = global_pool.dict()
    return ip_pool.create_global_pool(dnac, **global_pool)

@app.post("/pool/subpool", status_code=201)
def reserve_subpool(subpool: SubPool):
    # convert object to dict so it can be unpacked
    subpool = subpool.dict()
    return ip_pool.reserve_subpool(dnac, **subpool)

@app.delete("/pool/subpool", status_code=202)
def release_subpool(site_id: SiteID):
    # convert to dict to select key
    site_id = site_id.dict()
    return ip_pool.release_subpool(dnac, site_id['site_id'])

@app.delete("/pool/global", status_code=202)
def release_subpool(pool_name: PoolName):
    pool_name = pool_name.dict()
    return ip_pool.delete_global_pool(dnac, pool_name['pool_name'])
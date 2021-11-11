from typing import Any, Optional, Literal, List, Dict
from enum import Enum
import json
import os

from fastapi import FastAPI
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dnacentersdk import DNACenterAPI



dnac = DNACenterAPI(base_url='https://10.9.11.226',
                                username=os.getenv("username"),password=os.getenv("password"), verify=False, version="2.2.2.3")
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
@app.post("/dnac", response_model=WebhookResponseModel)
def sites(site_data: WebhookJsonModel):
    
    return {
        "message": "Received site webhook from Netbox",
        "data": site_data
    }

@app.post("/info", status_code=201)
def display_webhook_data(request: Dict[Any, Any]):
        print(json.dumps(request, indent=2))


@app.post("/area", status_code=201)
def create_area(area: Area):
    return create_site.create_area(dnac, area)

@app.post("/building", status_code=201)
def create_building(building: Building):
    return create_site.create_building(dnac, building)

@app.post("/floor", status_code=201)
def create_floor(floor: Floor):
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
def delete_global_pool(pool_name: PoolName):
    pool_name = pool_name.dict()
    return ip_pool.delete_global_pool(dnac, pool_name['pool_name'])

@app.post("/netbox/webhooks", status_code=200)
def webhook_received(webhook: Dict[Any, Any]):
    print(webhook)
    if webhook['model'] == "prefix":
        prefix_data = webhook['data']
        if prefix_data['custom_fields']['DNAC Global']:
            global_pool_obj = {
                "pool_name": prefix_data['custom_fields']['DNAC Pool Name'],
                "dhcp_servers": [], #not required
                "dns_servers": [], # not required
                "supernet": prefix_data['prefix']
            }  
            return ip_pool.create_global_pool(dnac, **global_pool_obj)
        else:
            sites = dnac.sites.get_site().response
            for site in sites:
                if site.name.lower() == prefix_data['site']['slug'].lower():
                    site_heirarchy = site['siteNameHierarchy']
                    site_id = dnac.sites.get_site(name=site_heirarchy).response[0].id
            subpool_obj = {
                "site_id": site_id,
                "global_pool_name": prefix_data['custom_fields']['dnac_global_pool'].upper(),
                "name": prefix_data['custom_fields']['DNAC Pool Name'],
                "type_": prefix_data['custom_fields']['dnac_pool_type'],
                "ipv6AddressSpace": False,
                "ipv4GlobalPool": "192.168.1.0/24", # not needed in legacy API which this is
                "ipv4Prefix": True,
                "ipv4PrefixLength": prefix_data['prefix'].split("/")[1],
                "ipv4Subnet": prefix_data['prefix'].split("/")[0],
                "ipv4GateWay": prefix_data['custom_fields']['gateway'],
                "ipv4DhcpServers": prefix_data['custom_fields']['dhcp_servers'],
                "ipv4DnsServers":  prefix_data['custom_fields']['dns_servers']
            }
            return ip_pool.reserve_subpool(dnac, **subpool_obj)
    if webhook['model'] == 'region':
        region_data = webhook["data"]
        area = {
            "area": {
                "name": region_data['slug'],
                "parentName": region_data['parent']['slug'],
                }
            }
        return create_site.create_area(dnac, area)

    if webhook['model'] == 'site':
        site_data = webhook['data']
        sites = dnac.sites.get_site().response
        for site in sites:
            if site.name.lower() == site_data['region']['slug'].lower():
                site_heirarchy = site['siteNameHierarchy']
        building = {
            "building": {
                "name": site_data['slug'],
                "parentName": site_heirarchy,
                "address": site_data['physical_address']
            }
        }
        return create_site.create_building(dnac, building)

    if webhook['model'] == 'location':
        location_data = webhook['data']
        sites = dnac.sites.get_site().response
        for site in sites:
            if site.name.lower() == location_data['site']['slug'].lower():
                site_heirarchy = site['siteNameHierarchy']
        floor = {
            "floor": {
                "name": location_data['slug'],
                "parentName": site_heirarchy,
                "rfModel": "Cubes And Walled Offices",
                "width": 5,
                "length": 5,
                "height": 5
            }
        }
        return create_site.create_floor(dnac, floor)
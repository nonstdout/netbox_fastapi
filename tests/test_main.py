import json
from typing import Literal, Optional
from fastapi.testclient import TestClient
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj
from dnacentersdk import DNACenterAPI
dnac = DNACenterAPI(base_url='https://10.9.11.226',
                                username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")

from main import app
import create_site

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_area():
    site = {
        "area": {
        "name": "testarea",
        "parentName": "Global",
        }
    }     
    response = client.post("/area", json=site)
    assert response.status_code == 201
    assert response.json()['status'] == "SUCCESS"

def test_create_building():
    site = {
            "building": {
            "name": "testbuilding",
            "parentName": "Global/testarea",
            "address": "unknown",
            }
        }    
    response = client.post("/building", json=site)
    assert response.status_code == 201
    assert response.json()['status'] == "SUCCESS"

def test_create_floor():
    site = {
            "floor": {
            "name": "testfloor",
            "parentName": "Global/testarea/testbuilding",
            "rfModel": "Cubes And Walled Offices",
            "width": 5,
            "length": 5,
            "height": 5,
            }
        }     
    response = client.post("/floor", json=site)
    assert response.status_code == 201
    assert response.json()['status'] == "SUCCESS"

# clean up created sites after tests
def test_delete_sites():
    response = create_site.delete_sites(dnac)
    assert json.loads(response)['status'] == "SUCCESS"





# def test_respond_to_sites_webhooks():
#     test_data = {
#         "event": 'created',
#         "timestamp": '2021-07-19 15:39:01.828640+00:00',
#         "model": 'region',
#         "username": 'admin',
#         "request_id": '3a66bcb7-dbb3-45d0-9f69-7e8d070935de',
#         "data": {"john": "site"},
#         "snapshots": {}
#     }
#     response = client.post(
#         "/sites/",
#         json=test_data
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "Received site webhook from Netbox",
#         "data": test_data
#         }

# dnac_url = "/dnac/" 

# class DnacTaskModel(BaseModel):
#     executionId: str
#     executionStatusUrl: str
#     message: str

# class DnacAreaModel(BaseModel):
#     name: str
#     parentName: str

# class DnacSiteTypeModel(BaseModel):
#     area: DnacAreaModel

# class DnacSitesModel(BaseModel):
#     type: str
#     site: Optional[DnacSiteTypeModel]



# def test_create_area():
#     area_data = {
#         "type": "area",
#         "site": {
#             "area": {
#                 "name": "testsite01",
#                 "parentName": "Global"
#             }
#         }
#     }

#     url = dnac_url + "/area"
#     headers = {
#         "Content-Type": "application/json",
#         "X-Auth-Token": "testToken123"
#     }
#     response = client.post(url, area_data, headers)
#     assert response.status_code == 200
#     assert response.json() == {
#         DnacTaskModel
#     }


# def test_dnac_auth():
#     DNACenterAPI(base_url='https://10.9.11.226',
#                             username='***REMOVED***',password='***REMOVED***', verify=False)

# def test_create_site():
#     dnac = DNACenterAPI(base_url='https://10.9.11.226',
#                             username='***REMOVED***',password='***REMOVED***', verify=False)

#     site = {
#         "site": {
#             "building": {
#                 "name": "bob",
#                 "parentName": "Global"
#             }
#         }
#     }      
#     site_type = "area"   
#     print(dnac.sites.create_site(site, site_type, active_validation=False))

# def test_task_status():
#     response = client.post(
#         "/tasks",
#         data=json.dumps({"type": 1})
#     )
#     content = response.json()
#     task_id = content["task_id"]
#     assert task_id

#     response = client.get(f"tasks/{task_id}")
#     content = response.json()
#     assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
#     assert response.status_code == 200

#     while content["task_status"] == "PENDING":
#         response = client.get(f"tasks/{task_id}")
#         content = response.json()
#     assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}
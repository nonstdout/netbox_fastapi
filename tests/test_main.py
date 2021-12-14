import json
from typing import Literal, Optional
from fastapi.testclient import TestClient
from pydantic import BaseModel, Json, ValidationError
from pydantic.utils import Obj
from dnacentersdk import DNACenterAPI
import os
dnac = DNACenterAPI(base_url=os.getenv("DNAC_ADDRESS"),
                                username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"), verify=os.getenv("DNAC_VERIFY"), version=os.getenv("DNAC_VERSION"))

from main import app
import create_site
import ip_pool

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# def test_create_area():
#     site = {
#         "area": {
#         "name": "testarea",
#         "parentName": "Global",
#         }
#     }     
#     response = client.post("/area", json=site)
#     assert response.status_code == 201
#     assert response.json()['status'] == "SUCCESS"



# def test_create_building():
#     site = {
#             "building": {
#             "name": "testbuilding",
#             "parentName": "Global/testarea",
#             "address": "unknown",
#             }
#         }    
#     response = client.post("/building", json=site)
#     assert response.status_code == 201
#     assert response.json()['status'] == "SUCCESS"

# def test_create_floor():
#     site = {
#             "floor": {
#             "name": "testfloor",
#             "parentName": "Global/testarea/testbuilding",
#             "rfModel": "Cubes And Walled Offices",
#             "width": 5,
#             "length": 5,
#             "height": 5,
#             }
#         }     
#     response = client.post("/floor", json=site)
#     assert response.status_code == 201
#     assert response.json()['status'] == "SUCCESS"

# def test_create_global_pool():
#     global_pool_obj = {
#         "pool_name": "test_global_pool",
#         "dhcp_servers": ["1.1.1.1"],
#         "dns_servers": ["2.2.2.2"],
#         "supernet": "192.168.1.0/24"
#     }   

#     response = client.post("/pool/global", json=global_pool_obj)
#     assert response.status_code == 201
#     assert response.json()['status'] == "SUCCESS"

# def test_reserve_subpool():
#     site_id = dnac.sites.get_site(name="Global/testarea").response[0].id
#     subpool_obj = {
#         "site_id": site_id,
#         "global_pool_name": "test_global_pool",
#         "name": "testsubpool",
#         "type_": "generic",
#         "ipv6AddressSpace": False,
#         "ipv4GlobalPool": "192.168.1.0/24",
#         "ipv4Prefix": True,
#         "ipv4PrefixLength": 25,
#         "ipv4Subnet": "192.168.1.0",
#         "ipv4GateWay": "192.168.1.1",
#         "ipv4DhcpServers": [
#             "1.2.3.4",
#             "1.2.3.5"
#         ],
#         "ipv4DnsServers": [
#             "1.2.3.4",
#             "1.2.3.5"
#         ]
#     }
    

#     response = client.post("/pool/subpool", json=subpool_obj)
#     assert response.status_code == 201
#     assert response.json()['status'] == "SUCCESS"

# def test_release_subpool():
#     site_id = dnac.sites.get_site(name="Global/testarea").response[0].id
#     site_id = {
#         "site_id": site_id
#     }

#     print(site_id)

#     response = client.delete("/pool/subpool", json=site_id)
#     assert response.status_code == 202
#     assert response.json()['status'] == "SUCCESS"

# def test_delete_global_pool():
#     pool_name = {
#         "pool_name": "test_global_pool"
#     }

#     response = client.delete("/pool/global", json=pool_name)
#     assert response.status_code == 202
#     assert response.json()['status'] == "SUCCESS"




def test_create_area_webhook():
    webhook = {
        'data': {
            '_depth': 1,
            'created': '2021-11-10',
            'custom_fields': {},
            'description': '',
            'display': 'testarea',
            'id': 88,
            'last_updated': '2021-11-10T17:24:36.431958Z',
            'name': 'testarea',
            'parent': {
                '_depth': 0,
                'display': 'Global',
                'id': 2,
                'name': 'Global',
                'slug': 'global',
                'url': '/api/dcim/regions/2/'
                },
            'slug': 'testarea',
            'url': '/api/dcim/regions/88/'
            },
        'event': 'created',
        'model': 'region',
        'request_id': '5054c422-ec46-426b-affe-7e09c3be4aff',
        'snapshots': {
            'postchange': {
                'created': '2021-11-10',
                'custom_fields': {},
                'description': '',
                'last_updated': '2021-11-10T17:24:36.431Z',
                'name': 'testarea',
                'parent': 2,
                'slug': 'testarea'
                },
            'prechange': None
            },
        'timestamp': '2021-11-10 17:24:36.457868+00:00',
        'username': 'admin'
        }
    
  
    response = client.post("/netbox/webhooks", json=webhook)
    assert response.status_code == 200
    assert response.json()['status'] == "SUCCESS"

def test_create_building_webhook():
    webhook = {
        "event": "created",
        "timestamp": "2021-11-10 18:08:08.801325+00:00",
        "model": "site",
        "username": "admin",
        "request_id": "4656a3c9-36f7-4da0-8a66-ee956532f2c6",
        "data": {
            "id": 8,
            "url": "/api/dcim/sites/8/",
            "display": "testbuilding",
            "name": "testbuilding",
            "slug": "testbuilding",
            "status": {
            "value": "active",
            "label": "Active"
            },
            "region": {
                "id": 86,
                "url": "/api/dcim/regions/86/",
                "display": "testarea",
                "name": "testarea",
                "slug": "testarea",
                "_depth": 1
            },
            "group": None,
            "tenant": None,
            "facility": "",
            "asn": None,
            "time_zone": None,
            "description": "",
            "physical_address": "somewhere",
            "shipping_address": "",
            "latitude": None,
            "longitude": None,
            "contact_name": "",
            "contact_phone": "",
            "contact_email": "",
            "comments": "",
            "tags": [],
            "custom_fields": {
            "dnac_site_id": None
            },
            "created": "2021-11-10",
            "last_updated": "2021-11-10T18:08:08.775134Z"
        },
        "snapshots": {
            "prechange": None,
            "postchange": {
            "created": "2021-11-10",
            "last_updated": "2021-11-10T18:08:08.775Z",
            "name": "testbuilding",
            "slug": "testbuilding",
            "status": "active",
            "region": 86,
            "group": None,
            "tenant": None,
            "facility": "",
            "asn": None,
            "time_zone": None,
            "description": "",
            "physical_address": "somewhere",
            "shipping_address": "",
            "latitude": None,
            "longitude": None,
            "contact_name": "",
            "contact_phone": "",
            "contact_email": "",
            "comments": "",
            "custom_fields": {
                "dnac_site_id": None
            },
            "tags": []
            }
        }
    }
  
    response = client.post("/netbox/webhooks", json=webhook)
    assert response.status_code == 200
    assert response.json()['status'] == "SUCCESS"


def test_create_floor_webhook():
    webhook = {
        "event": "updated",
        "timestamp": "2021-11-10 18:39:11.642038+00:00",
        "model": "location",
        "username": "admin",
        "request_id": "d52fbb0d-7451-4a8e-9bc7-b92a42c87ab0",
        "data": {
            "id": 1,
            "url": "/api/dcim/locations/1/",
            "display": "testfloor",
            "name": "testfloor",
            "slug": "testfloor",
            "site": {
            "id": 6,
            "url": "/api/dcim/sites/6/",
            "display": "testbuilding",
            "name": "testbuilding",
            "slug": "testbuilding"
            },
            "parent": None,
            "description": "",
            "custom_fields": {},
            "created": "2021-11-09",
            "last_updated": "2021-11-10T18:39:11.623452Z",
            "_depth": 0
        },
        "snapshots": {
            "prechange": {
            "created": "2021-11-09",
            "last_updated": "2021-11-09T14:39:31.450Z",
            "name": "testfloor",
            "slug": "testfloor",
            "site": 6,
            "parent": None,
            "description": "",
            "custom_fields": {}
            },
            "postchange": {
            "created": "2021-11-09",
            "last_updated": "2021-11-10T18:39:11.623Z",
            "name": "testfloor",
            "slug": "testfloor",
            "site": 6,
            "parent": None,
            "description": "",
            "custom_fields": {}
            }
        }
        }   
    response = client.post("/netbox/webhooks", json=webhook)
    assert response.status_code == 200
    assert response.json()['status'] == "SUCCESS"



def test_create_global_pool_webhook():
    # webhook data with custom_field DNAC Global = True
    # should create global pool in dnac
    data = {
        'id': 3,
        'url': '/api/ipam/prefixes/3/',
        'display': '192.168.0.0/24',
        'family': {'value': 4, 'label': 'IPv4'},
        'prefix': '192.168.0.0/24',
        'site': {
            'id': 6,
            'url': '/api/dcim/sites/6/',
            'display': 'testbuilding',
            'name': 'testbuilding',
            'slug': 'testbuilding'
            },
        'vrf': None, 
        'tenant': None,
        'vlan': None, 
        'status': {
            'value': 'active', 
            'label': 'Active'
            }, 
        'role': None, 
        'is_pool': True, 
        'mark_utilized': False, 
        'description': 'j', 
        'tags': [], 
        'custom_fields': {
            'DNAC Global': True, 
            'DNAC Pool Name': 'TESTBUILDING_POOL'
            }, 
            'created': '2021-11-09', 
            'last_updated': '2021-11-09T15:45:02.907116Z', 
            'children': 0, 
            '_depth': 0
        }
    if data['custom_fields']['DNAC Global']:
        global_pool_obj = {
            "pool_name": data['custom_fields']['DNAC Pool Name'],
            "dhcp_servers": [],
            "dns_servers": [],
            "supernet": data['prefix']
        }  
        assert ip_pool.create_global_pool(dnac, **global_pool_obj)['status'] == "SUCCESS"

def test_reserve_subpool_webhook():
    # webhook data with custom_field DNAC Global = False
    # should reserve subpool in dnac
    data =  {
        "id": 4,
        "url": "/api/ipam/prefixes/4/",
        "display": "192.168.0.0/25",
        "family": {
        "value": 4,
        "label": "IPv4"
        },
        "prefix": "192.168.0.0/25",
        "site": {
        "id": 6,
        "url": "/api/dcim/sites/6/",
        "display": "testbuilding",
        "name": "testbuilding",
        "slug": "testbuilding"
        },
        "vrf": None,
        "tenant": None,
        "vlan": None,
        "status": {
        "value": "active",
        "label": "Active"
        },
        "role": None,
        "is_pool": True,
        "mark_utilized": False,
        "description": "",
        "tags": [],
        "custom_fields": {
        "DNAC Global": False,
        "DNAC Pool Name": "AP_POOL",
        "dnac_pool_type": "Generic",
        "dnac_global_pool": "MRBUILDING2_POOL",
        "dhcp_servers": None,
        "dns_servers": None,
        "gateway": "192.168.0.1"
        },
        "created": "2021-11-10",
        "last_updated": "2021-11-10T14:47:32.101078Z",
        "children": 0,
        "_depth": 1
    }

    if not data['custom_fields']['DNAC Global']:
        sites = dnac.sites.get_site().response
        for site in sites:
            if site.name.lower() == data['site']['slug'].lower():
                site_heirarchy = site['siteNameHierarchy']
                site_id = dnac.sites.get_site(name=site_heirarchy).response[0].id
        subpool_obj = {
            "site_id": site_id,
            "global_pool_name": f"{data['site']['slug']}_pool".upper(),
            "name": data['custom_fields']['DNAC Pool Name'],
            "type_": data['custom_fields']['dnac_pool_type'],
            "ipv6AddressSpace": False,
            "ipv4GlobalPool": "192.168.1.0/24", # not needed in legacy API which this is
            "ipv4Prefix": True,
            "ipv4PrefixLength": data['prefix'].split("/")[1],
            "ipv4Subnet": data['prefix'].split("/")[0],
            "ipv4GateWay": data['custom_fields']['gateway'],
            "ipv4DhcpServers": data['custom_fields']['dhcp_servers'],
            "ipv4DnsServers":  data['custom_fields']['dns_servers']
        }
    assert ip_pool.reserve_subpool(dnac, **subpool_obj)['status'] == "SUCCESS"


def test_release_subpool():
    site_id = dnac.sites.get_site(name="Global/testarea/testbuilding").response[0].id
    site_id = {
        "site_id": site_id
    }

    print(site_id)

    response = client.delete("/pool/subpool", json=site_id)
    assert response.status_code == 202
    assert response.json()['status'] == "SUCCESS"

def test_delete_global_pool():
    pool_name = {
        "pool_name": "TESTBUILDING_POOL"
    }

    response = client.delete("/pool/global", json=pool_name)
    assert response.status_code == 202
    assert response.json()['status'] == "SUCCESS"



# # # clean up created sites after tests
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
#     dnac = DNACenterAPI(base_url=os.getenv("DNAC_ADDRESS"),
 #                               username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"), verify=os.getenv("DNAC_VERIFY"), version=os.getenv("DNAC_VERSION"))
# def test_create_site():
#     dnac = DNACenterAPI(base_url=os.getenv("DNAC_ADDRESS"),
#                                username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"), verify=os.getenv("DNAC_VERIFY"), version=os.getenv("DNAC_VERSION"))

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
import json

def get_execution_status(dnac, execution_id):
    return dnac.custom_caller.call_api('GET',
                            f'/dna/platform/management/business-api/v1/execution-status/{execution_id}')

def check_task_completion(dnac, execution_id):
    """Check status of task."""
    import time
    while True:
        response = get_execution_status(dnac, execution_id)
        if response.endTime == None:
            print('Task not completed yet, retrying...')
            time.sleep(1)
        elif response.status == 'SUCCESS':
            print(f'TASK {response.status}!')
            task_info = response
            return task_info

        else:
            print(f'TASK {response.status}! Error: {response.bapiError}')
            return None

def create_area(dnac, site):

    site = {
            "area": {
            "name": "testarea",
            "parentName": "Global",
            }
        }     
    site_type = "area" 
    execution_id = dnac.sites.create_site(site=site, type=site_type)["executionId"]
    task_status = check_task_completion(dnac, execution_id)
    return task_status

def create_building(dnac, site):

    site = {
            "building": {
            "name": "testbuilding",
            "parentName": "Global/testarea",
            "address": "unknown",
            }
        }     
    site_type = "building" 
    execution_id = dnac.sites.create_site(site=site, type=site_type)["executionId"]
    task_status = check_task_completion(dnac, execution_id)
    return task_status

def create_floor(dnac, site):

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
    site_type = "floor" 
    execution_id = dnac.sites.create_site(site=site, type=site_type)["executionId"]
    task_status = check_task_completion(dnac, execution_id)
    return task_status

def delete_site(dnac, site_id):
    execution_id = dnac.sites.delete_site(site_id)["executionId"]
    task_status = check_task_completion(dnac, execution_id)
    return task_status

def delete_sites(dnac):
    # To check names of sites being deleted by id
    # check_names = [
    #     dnac.sites.get_site(name="Global/testarea/testbuilding/testfloor").response[0].name,
    #     dnac.sites.get_site(name="Global/testarea/testbuilding").response[0].name,
    #     dnac.sites.get_site(name="Global/testarea").response[0].name,
    # ]
    # print(check_names)

    # list of sites to be deleted
    # dnac returns 500 if site with name not found
    created_sites = []
    try:
        created_sites.append(dnac.sites.get_site(name="Global/testarea/testbuilding/testfloor").response[0].id)
    except Exception as e:
        None
    
    try:
        created_sites.append(dnac.sites.get_site(name="Global/testarea/testbuilding").response[0].id)
    except Exception as e:
        None
    
    try:
        created_sites.append(dnac.sites.get_site(name="Global/testarea").response[0].id)
    except Exception as e:
        None

    # delete test sites to cleanup after tests
    print(created_sites)
    for site in created_sites:
            print(delete_site(dnac, site))
    return json.dumps({"status": "SUCCESS"})


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    from dnacentersdk import DNACenterAPI



    dnac = DNACenterAPI(base_url='https://10.9.11.226',
                                username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")
    # print(create_area(dnac))
    # print(create_building(dnac))
    # print(create_floor(dnac))

    # cleans up all created sites
    # delete_sites(dnac)

if __name__ == "__main__":
    main()
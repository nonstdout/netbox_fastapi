


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


def create_global_pool(dnac, pool_type='generic', **kwargs):
    payload = {
        "ipPoolName": kwargs['pool_name'],
        "dhcpServerIps": kwargs['dhcp_servers'],
        "dnsServerIps": kwargs['dns_servers'],
        "ipPoolCidr": kwargs['supernet'],
        "context": [
            {
                "contextKey": "type",
                "contextValue": pool_type,
                "owner": "DNAC"
            }
        ]
    }

    global_pool = dnac.custom_caller.call_api('POST','/api/v2/ippool/', json=payload)
    task_global_pool = dnac.task.get_task_by_id(task_id=global_pool.response.taskId)

    if not task_global_pool.response.isError:
        # Retrieve created pool
        all_pools = dnac.network_settings.get_global_pool().response
        for pool in all_pools:
            if pool['ipPoolName'] == kwargs['pool_name']:
                created_global_pool = pool['ipPoolName']
                print(created_global_pool)
                return {"status": "SUCCESS"}

    else:
        # Get task error details
        print('Unfortunately ', task_global_pool.response.progress)
        print('Reason: ', task_global_pool.response.failureReason)

def delete_global_pool(dnac, pool_name):
    # get pool id
    all_pools = dnac.network_settings.get_global_pool().response
    for pool in all_pools:
        if pool['ipPoolName'] == pool_name:
            global_pool_id = pool['id']
            pool_name = pool['name']
            print(pool_name, global_pool_id)
    execution_id = dnac.network_settings.delete_global_ip_pool(global_pool_id)['executionId']
    task_status = check_task_completion(dnac, execution_id)
    return task_status


# new api is broken
# TASK FAILURE! Error: c0cc95e2-9028-4768-aac7-7230de999066 | 09fa06a0-22a8-421e-a78f-21e08f236c62 | 429f-aa81-4d3b-960a : ScriptProcessor
#  Execution Failed with error: ReferenceError: "iinput_json_detail" is not defined in <eval>  at line number : 237 
# def reserve_subpool(dnac, site_id, **kwargs):
#     payload = {
#         "name": kwargs['name'],
#         "type": kwargs['type'],
#         "ipv6AddressSpace": kwargs['ipv6AddressSpace'],
#         "ipv4GlobalPool": kwargs['ipv4GlobalPool'],
#         "ipv4Prefix": kwargs['ipv4Prefix'],
#         "ipv4PrefixLength": kwargs['ipv4PrefixLength'],
#         "ipv4Subnet": kwargs['ipv4Subnet'],
#         "ipv4GateWay": kwargs['ipv4GateWay'],
#         "ipv4DhcpServers": kwargs['ipv4DhcpServers'],
#         "ipv4DnsServers": kwargs['ipv4DnsServers']
#     }
#     import json
#     print(json.dumps(payload, indent=2))
#     execution_id = dnac.network_settings.reserve_ip_subpool(site_id, **payload)['executionId']
#     task_status = check_task_completion(dnac, execution_id)
#     return task_status


def get_parent_pool_id_dna(dnac, pool_name):
    """Query name and return parent_pool id."""
    # Query DNAC for pool name by site name.
    pool = dnac.custom_caller.call_api('GET',f'/api/v2/ippool?ipPoolName={pool_name}')

    return pool.response[0].id

# Implementation of non-public API as public API is broken
def reserve_subpool(dnac, **kwargs):
    payload = {
        "groupName": kwargs['name'],
        "groupOwner": "DNAC",
        "type": kwargs['type_'],
        "siteId": kwargs['site_id'],
        "ipPools": [
            {
                "parentUuid": get_parent_pool_id_dna(dnac, kwargs['global_pool_name']),
                "dhcpServerIps": kwargs['ipv4DhcpServers'],
                "dnsServerIps": kwargs['ipv4DnsServers'],
                "ipPoolOwner": "DNAC",
                "shared": True,
                "gateways": [kwargs['ipv4GateWay']],
                "ipPoolCidr": f"{kwargs['ipv4Subnet']}/{kwargs['ipv4PrefixLength']}"
            }
        ]
    }

    # #for testing to see payload
    # import json
    # print(json.dumps(payload))

 
    subpool = dnac.custom_caller.call_api('POST','/api/v2/ippool/group/', json=payload)
    task_subpool = dnac.task.get_task_by_id(task_id=subpool.response.taskId)

    # completed tasks have an endtime attribute
    import time
    while not task_subpool.response.endTime:
        # print(task_subpool.response.progress)
        time.sleep(1)
        # check task has completed, reassign variable
        task_subpool = dnac.task.get_task_by_id(task_id=subpool.response.taskId)
    if not task_subpool.response.isError:
        print(f"Subpool Created Sucessfully")
        # print(task_subpool)
        return {"status": "SUCCESS"}

    else:
        # Get task error details
        print('Unfortunately ', task_subpool.response.progress)
        print('Reason: ', task_subpool.response.failureReason)

def release_subpool(dnac, site_id):
    subpool_id = dnac.network_settings.get_reserve_ip_subpool(site_id=site_id).response[0].id
    execution_id = dnac.network_settings.release_reserve_ip_subpool(subpool_id)['executionId']
    task_status = check_task_completion(dnac, execution_id)
    return task_status








def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    from dnacentersdk import DNACenterAPI



    dnac = DNACenterAPI(base_url='https://10.9.11.226',
                                username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")
        ## setup site for testing, get id
    import create_site
    create_site.create_area(dnac)

    global_pool_obj = {
        "pool_name": "test_global_pool",
        "dhcp_servers": ["1.1.1.1"],
        "dns_servers": ["2.2.2.2"],
        "supernet": "192.168.1.0/24"
    }

    create_global_pool(dnac, **global_pool_obj)

    subpool_obj = {
        "global_pool_name": "test_global_pool",
        "name": "testsubpool",
        "_type": "generic",
        "ipv6AddressSpace": False,
        "ipv4GlobalPool": "192.168.1.0/24",
        "ipv4Prefix": True,
        "ipv4PrefixLength": 25,
        "ipv4Subnet": "192.168.1.0",
        "ipv4GateWay": "192.168.1.1",
        "ipv4DhcpServers": [
            "1.2.3.4",
            "1.2.3.5"
        ],
        "ipv4DnsServers": [
            "1.2.3.4",
            "1.2.3.5"
        ]
    }

    site_id = dnac.sites.get_site(name="Global/testarea").response[0].id
    reserve_subpool(dnac, site_id, **subpool_obj)

    # cleanup
    # release subpool
    release_subpool(dnac, site_id)
    # delete global pool
    delete_global_pool(dnac, 'test_global_pool')
    # cleanup created site
    create_site.delete_sites(dnac)


if __name__ == "__main__":
    main()



import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from dnacentersdk import DNACenterAPI
import time


dnac = DNACenterAPI(base_url='https://10.9.11.226',
                            username='***REMOVED***',password='***REMOVED***', verify=False, version="2.2.2.3")

def get_execution_status(dnac, execution_id):
    return dnac.custom_caller.call_api('GET',
                            f'/dna/platform/management/business-api/v1/execution-status/{execution_id}')

def check_task_completion(dnac, execution_id):
    """Check status of task."""
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


global_pool_obj = {
    "pool_name": "test_global_pool",
    "dhcp_servers": ["1.1.1.1"],
    "dns_servers": ["2.2.2.2"],
    "supernet": "192.168.1.0/24"
}
# create_global_pool(dnac, **global_pool_obj)
delete_global_pool(dnac, 'test_global_pool')

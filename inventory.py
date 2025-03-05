#!/usr/bin/python3

import requests as r
import json as j
import os

api_url = "https://compute.api.cloud.yandex.net/compute/v1/instances"
api_token = os.environ['YC_TOKEN']
group_label = "ansible.group"
folder_id = os.environ['YC_FOLDER_ID']
k3s_token = os.environ['K3S_TOKEN']


def get_hosts(data_json):
    inventory = {
            '_meta': { 'hostvars': {} },
            'k3s_cluster': {
            'children': ['server', 'agent'],
            'vars': {
                'token': k3s_token
            }
        }
    }

    if data_json == {}:
        return {}

    for instance in data_json['instances']:
        group = instance['labels'][group_label]

        address = instance['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']

        if group not in inventory:
            inventory[group] = {'hosts': [], 'vars': {}, 'children': []}

        inventory[group]['hosts'].append(address)
        inventory['_meta']['hostvars'][address] = {
            'ansible_local_ip': instance['networkInterfaces'][0]['primaryV4Address']['address']
        }

    return j.dumps(inventory, indent=2)


def main():
    payload = {"folderId": f"{folder_id}"}
    headers = {"Authorization": f"Bearer {api_token}"}

    res = r.get(api_url, params=payload, headers=headers)
    hosts_formatted = get_hosts(j.loads(res.text))

    print(hosts_formatted)


if __name__ == '__main__':
    main()

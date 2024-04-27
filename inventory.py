#!/usr/bin/python3

import requests as r
import json as j

api_url = "https://compute.api.cloud.yandex.net/compute/v1/instances"
api_token = "t1.<token>"
group_label = "ansible.group"

def get_hosts(data_json):
    host_groups = dict()

    if data_json == {}:
        return {}

    for instance in data_json['instances']:
        group = instance['labels'][group_label]
        address = instance['networkInterfaces'][0]['primaryV4Address']['oneToOneNat']['address']

        if group not in host_groups:
            host_groups[group] = {'hosts': [], 'vars': {}, 'children': []}
        host_groups[group]['hosts'].append(address)
    return j.dumps(host_groups, indent=2)


def main():
    payload = {"folderId": "<folder_id>"}
    headers = {"Authorization": f"Bearer {api_token}"}

    res = r.get(api_url, params=payload, headers=headers)
    hosts_formatted = get_hosts(j.loads(res.text))

    print(hosts_formatted)

if __name__ == '__main__':
    main()

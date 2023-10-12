import http.client
import json

connection = http.client.HTTPConnection('localhost','8080',timeout=10)

def create(connection) : 

    header = { 
    'Content-Type': 'application/json;ty=1',
    'Accept': 'application/json',
    'X-M2M-Origin': 'CAdmin',
    'X-M2M-RI': 'lus89mknqcd',
    'X-M2M-RVI': '3'
    }

    payload = {
    "m2m:acp": {
        "pv": {
            "acr": [ 

            {
                "acop": 1,
                "acor": ["CSensor*"]
            }
            ]
        },
        "pvs": {
            "acr": [{
                "acop": 63,
                "acor": [
                    "CAdmin"
                ]
            }
            ]
        },
        "rn": "SensorACPRoom2"
    }
    }
    json_data = json.dumps(payload)
    connection.request('POST', 'id-in', json_data, header)

def put(connection):
    header = { 
    'Content-Type': 'application/json;ty=1',
    'Accept': 'application/json',
    'X-M2M-Origin': 'CAdmin',
    'X-M2M-RI': 'pfgk5cslxc',
    'X-M2M-RVI': '3'
    }
    payload = {
        "m2m:acp":{
            "pv": {
                "acr": [ 
                {
                    "acop": 1,
                    "acor": ["CSensor*"]
                }
                ]
            }
        }
    }
    json_data = json.dumps(payload)
    connection.request('PUT', 'acp8798785459841813212', json_data, header)

create(connection)
response = connection.getresponse()
print(response.read().decode())
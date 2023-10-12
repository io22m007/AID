import requests

resourceTypes = { # TS0004 6.3.4.2.1
    "AccessControlPolicy" : "ty=1"
}

def CreateAccessControlPolicy(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    print(url)
    print(headers)
    print(primitiveContent)
    return requests.post(url, headers=headers, json=primitiveContent)

def UpdateAccessControlPolicy(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    print(url)
    print(headers)
    print(primitiveContent)
    return requests.put(url, headers=headers, json=primitiveContent)

def HeaderFields(originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str) -> dict:
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json;' + resourceType,
        'Accept': 'application/json',
    }
    return headers

def CreateAccessControlPolicyPrimitiveContent(resourceName:str, accessControlOperations:str, accessControlOriginators:list, accessControlOperationsSelfPrivileges:str, accessControlOriginatorsSelfPrivileges:list) -> dict:
    data = {
        "m2m:acp": {
            "rn": resourceName,
            "pv": {
                "acr": [
                    {
                        "acop": accessControlOperations,
                        "acor": accessControlOriginators
                    }
                ]
            },
            "pvs": {
                "acr": [
                    {
                        "acop": accessControlOperationsSelfPrivileges,
                        "acor": accessControlOriginatorsSelfPrivileges
                    }
                ]
            }
        }
    }
    return data

def UpdateAccessControlOperationsPrimitiveContent( accessControlOperations:str, accessControlOriginators:list) -> dict:
    data = {
        "m2m:acp":{
            "pv": {
                "acr": [ 
                    {
                        "acop": accessControlOperations,
                        "acor": accessControlOriginators
                    }
                ]
            }
        }
    }
    return data

def CheckResponse(response:requests.models.Response):
    if response.request.method == "POST":
        if response.status_code == 201:
            print("POST request successful")
            print(response.text)
            print()
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print(response.text)
            print()
    elif response.request.method == "PUT":
        if response.status_code == 200:
            print("POST request successful")
            print(response.text)
            print()
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print(response.text)
            print()


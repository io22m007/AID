import requests

resourceTypes = {
    "Subscription" : "ty=23"
}

def SubscribeResource(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    return requests.post(url, headers=headers, json=primitiveContent)

def HeaderFields(originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str) -> dict:
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json;' + resourceType,
        'Accept': 'application/json'
    }
    return headers

def SubscriptionPrimitiveContent(resourceName:str, notificationURL, notificationContentType:int, notificationEventType) -> dict:
    data = {
        "m2m:sub": {
            "rn": resourceName,
            "nu": notificationURL,
            "nct": notificationContentType,
            "enc": {
                "net": notificationEventType
            }
        }
    }
    return data

def CheckResponse(response:requests.models.Response):
    if response.status_code == 201:
        print("POST request successful")
        print("Response Content:")
        print(response.text)
        print()
    else:
        print(f"POST request failed with status code: {response.status_code}")
        print("Response Content:")
        print(response.text)
        print()

url = "http://localhost:8080/cse-in/StreetLight-AE-2/Light-Container-2"  # URL includes AE and Container names

cse = "http://acme-regal-1:8080/cse-asn" + "/"  # URL includes AE and resource names
ae = "Regal-AE" + "/"
box = "Box-1" + "/"
user = "CAIDAdmin"

CheckResponse(SubscribeResource(cse + ae + box + "DeviceLight/binarySwitch", HeaderFields(user, "0011", "4", resourceTypes["Subscription"]), SubscriptionPrimitiveContent("Subscription1", ["http://192.168.1.108:1880"], 2, [1])))
CheckResponse(SubscribeResource(cse + ae + box + "DeviceLight/colour", HeaderFields(user, "0012", "4", resourceTypes["Subscription"]), SubscriptionPrimitiveContent("Subscription2", ["http://192.168.1.108:1880"], 2, [1])))
CheckResponse(SubscribeResource(cse + ae + box + "DeviceScale/weight", HeaderFields(user, "0013", "4", resourceTypes["Subscription"]), SubscriptionPrimitiveContent("Subscription3", ["http://192.168.1.108:1880"], 2, [1])))
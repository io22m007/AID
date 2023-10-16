import requests

def UpdateResource(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    return requests.put(url, headers=headers, json=primitiveContent)

def HeaderFields(originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers

def RegalBoxDeviceScaleWeightUpdatePrimitiveContent(weight:float) -> dict:
    data = {
        "cod:weigt": {
            "weigt": weight
        }
    }
    return data

def RegalBoxDeviceLightBinarySwitchUpdatePrimitiveContent(status:bool) -> dict:
    data = {
        "cod:binSh": {
            "powSe": status
        }
    }
    return data

def RegalBoxDeviceLightColourUpdatePrimitiveContent(red:int, green:int, blue:int) -> dict:
    data = {
        "cod:color": {
            "red": red,
            "green": green,
            "blue": blue,
        }
    }
    return data

def CheckResponse(response:requests.models.Response):
    if response.status_code == 200:
        print("PUT request successful")
        print("Response Content:")
        print(response.text)
        print()
    else:
        print(f"PUT request failed with status code: {response.status_code}")
        print("Response Content:")
        print(response.text)
        print()

cse = "http://192.168.32.189:8080/cse-asn"  # URL includes AE and resource names
ae = "/Regal-AE"
box = "/Box-1"
user = "CAIDAdmin"

CheckResponse(UpdateResource(cse + ae + box + "/DeviceLight/binarySwitch", HeaderFields(user, "0101", "4"), RegalBoxDeviceLightBinarySwitchUpdatePrimitiveContent(True)))
CheckResponse(UpdateResource(cse + ae + box + "/DeviceLight/colour", HeaderFields(user, "0102", "4"), RegalBoxDeviceLightColourUpdatePrimitiveContent(11,22,33)))
CheckResponse(UpdateResource(cse + ae + box + "/DeviceScale/weight", HeaderFields(user, "0103", "4"), RegalBoxDeviceScaleWeightUpdatePrimitiveContent(0.125)))


import requests

resourceTypes = { # TS0004 6.3.4.2.1
    "ApplicationEntity" : "ty=2",
    "Container" : "ty=3",
    "ContentInstance" : "ty=4",
    "FlexContainer" : "ty=28",
    "ApplicationEntityAnnouced" : "ty=10002",
    "ContainerAnnouced" : "ty=10003",
    "ContentInstanceAnnouced" : "ty=10004",
    "FlexContainerAnnouced" : "ty=10028"

}

def CreateResource(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    print(url)
    print(headers)
    print(primitiveContent)
    return requests.post(url, headers=headers, json=primitiveContent)

def HeaderFields(originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str, announceTo:str, announceSyncType:str) -> dict:
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json;' + resourceType,
        'Accept': 'application/json',
        "at": announceTo,
        "ast": announceSyncType
    }
    return headers

#ApplicationEntity
def ApplicationEntityPrimitiveContent(resourceName:str, App_ID:str, requestReachability:str, supportedReleaseVersions:dict) -> dict:
    data = {
        "m2m:ae": {
            "rn": resourceName,
            "api": App_ID,
            "rr": requestReachability,
            "srv": supportedReleaseVersions
        }
    }
    return data

#ApplicationEntityAnnouced
def ApplicationEntityAnnoucedPrimitiveContent(resourceName:str, App_ID:str, requestReachability:str, supportedReleaseVersions:dict) -> dict:
    data = {
        "m2m:aeA": {
            "rn": resourceName,
            "api": App_ID,
            "rr": requestReachability,
            "srv": supportedReleaseVersions
        }
    }
    return data

#Container
def ContainerPrimitiveContent(resourceName:str) -> dict:
    data = {
        "m2m:cnt": {
            "rn": resourceName
        }
    }
    return data

#ContainerAnnouced
def ContainerAnnoucedPrimitiveContent(resourceName:str) -> dict:
    data = {
        "m2m:cntA": {
            "rn": resourceName
        }
    }
    return data

#ContentInstance
def ContentInstancePrimitiveContent(content:str) -> dict:
    data = {
        "m2m:cin": {
            "cnf": "text/plain:0",
            "con": content
        }
    }
    return data

#ContentInstanceAnnouced
def ContentInstanceAnnoucedPrimitiveContent(content:str) -> dict:
    data = {
        "m2m:cinA": {
            "cnf": "text/plain:0",
            "con": content
        }
    }
    return data

#FlexContainerWeight
def FlexContainerWeightPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:weigt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.weight", #TS23 5.3.1.99
            "weigt": 0
        }
    }
    return data

#FlexContainerColor
def FlexContainerColorPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:color": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.colour",
            "red": 0,
            "green": 0,
            "blue": 0
        }
    }
    return data

#FlexContainerBinarySwitch
def FlexContainerBinarySwitchPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:binSh": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.binarySwitch",
            "powSe": False
        }
    }
    return data

def DeviceModelDeviceLightPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:devLt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.device.deviceLight"
        }
    }
    return data

def DeviceModelDeviceScalePrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:devSca": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.device.mioDeviceScale"
        }
    }
    return data

def CheckResponse(response:requests.models.Response):
    if response.status_code == 201:
        print("POST request successful")
        print(response.text)
        print()
    else:
        print(f"POST request failed with status code: {response.status_code}")
        print(response.text)
        print()

#Application Entity
#CheckResponse(Create("http://localhost:8080/cse-in", "CAIDAdmin", "0001", "3", resourceTypes["ApplicationEntity"], ApplicationEntityPrimitiveContent("Notebook-AE", "NnotebookAE", True, ["3"])))
#Container
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE", "CAIDAdmin", "0002", "3", resourceTypes["Container"], ContainerPrimitiveContent("Container")))
#ContentInstance
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE/Container", "CAIDAdmin", "0003", "3", resourceTypes["ContentInstance"], ContentInstancePrimitiveContent("Hello, World!")))

url = "http://192.168.1.106:8080/cse-asn"

#Application Entity
CheckResponse(CreateResource(url, HeaderFields("CAIDAdmin", "0001", "4", resourceTypes["ApplicationEntity"], "id-in", "2"), ApplicationEntityPrimitiveContent("Regal-AE", "NRegalAE", True, ["4"])))
#Container
CheckResponse(CreateResource(url + "/Regal-AE", HeaderFields("CAIDAdmin", "0002", "4", resourceTypes["Container"], "id-in", "2"), ContainerPrimitiveContent("Box-1")))
#Device Model DeviceScale
CheckResponse(CreateResource(url + "/Regal-AE/Box-1", HeaderFields("CAIDAdmin", "0004", "4", resourceTypes["FlexContainer"], "id-in", "2"), DeviceModelDeviceScalePrimitiveContent("DeviceScale")))
#FlexContainer Weight
CheckResponse(CreateResource(url + "/Regal-AE/Box-1/DeviceScale", HeaderFields("CAIDAdmin", "0003", "4", resourceTypes["FlexContainer"], "id-in", "2"), FlexContainerWeightPrimitiveContent("weight")))
#Device Model DeviceLight
CheckResponse(CreateResource(url + "/Regal-AE/Box-1", HeaderFields("CAIDAdmin", "0004", "4", resourceTypes["FlexContainer"], "id-in", "2"), DeviceModelDeviceLightPrimitiveContent("DeviceLight")))
#FlexContainer binarySwitch
CheckResponse(CreateResource(url + "/Regal-AE/Box-1/DeviceLight", HeaderFields("CAIDAdmin", "0005", "4", resourceTypes["FlexContainer"], "id-in", "2"), FlexContainerBinarySwitchPrimitiveContent("binarySwitch")))
#FlexContainer colour
CheckResponse(CreateResource(url + "/Regal-AE/Box-1/DeviceLight", HeaderFields("CAIDAdmin", "0006", "4", resourceTypes["FlexContainer"], "id-in", "2"), FlexContainerColorPrimitiveContent("colour")))
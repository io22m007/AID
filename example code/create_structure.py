import requests

class RequestCounterClass:
    def __init__(self):
        self.count = 0  # Initialize the instance variable

    def increment(self):
        self.count += 1
        return f"{self.count:03}" # return with at least three numbers

resourceTypes = { # TS0004 6.3.4.2.1
    "ApplicationEntity" : "ty=2",
    "Container" : "ty=3",
    "ContentInstance" : "ty=4",
    "FlexContainer" : "ty=28"
}

def CreateResource(url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
    print(url)
    print(headers)
    print(primitiveContent)
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

#Container
def ContainerPrimitiveContent(resourceName:str) -> dict:
    data = {
        "m2m:cnt": {
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

#FlexContainer weight
def FlexContainerWeightPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:weigt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.weight", #TS23 5.3.1.99
            "weigt": 0
        }
    }
    return data

#FlexContainer colour
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

#FlexContainer binarySwitch
def FlexContainerBinarySwitchPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:binSh": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.binarySwitch",
            "powSe": False
        }
    }
    return data

#FlexContainer deviceLight
def FlexContainerDeviceLightPrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:devLt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.device.deviceLight"
        }
    }
    return data

#FlexContainer mioDeviceScale
def FlexContainerDeviceScalePrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:devSca": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.device.mioDeviceScale"
        }
    }
    return data

#Print response of POST request
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
#CheckResponse(Create("http://localhost:8080/cse-in", CMyself, "0001", "3", resourceTypes["ApplicationEntity"], ApplicationEntityPrimitiveContent("Notebook-AE", "NnotebookAE", True, ["3"])))
#Container
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE", CMyself, "0002", "3", resourceTypes["Container"], ContainerPrimitiveContent("Container")))
#ContentInstance
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE/Container", CMyself, "0003", "3", resourceTypes["ContentInstance"], ContentInstancePrimitiveContent("Hello, World!")))

cse = "http://acme-regal-1:8080/cse-asn" # URL includes AE and resource names
ae =  "Regal-1-AE"
app_id = "NRegal1AE"
box_count = 2

user = "CAdmin"
request_counter = RequestCounterClass()
releaseVersionIndicator = "3"


#Application Entity
CheckResponse(CreateResource(cse, HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["ApplicationEntity"]), ApplicationEntityPrimitiveContent(ae, app_id, True, ["3"])))

for box_counter in range(1, box_count+1):
    #Container
    CheckResponse(CreateResource(cse + "/" + ae, HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["Container"]), ContainerPrimitiveContent("Box-" + str(box_counter))))
    #Device Model DeviceScale
    CheckResponse(CreateResource(cse + "/" + ae + "/Box-" + str(box_counter) , HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["FlexContainer"]), FlexContainerDeviceScalePrimitiveContent("DeviceScale")))
    #FlexContainer Weight
    CheckResponse(CreateResource(cse + "/" + ae + "/Box-" + str(box_counter) + "/DeviceScale", HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["FlexContainer"]), FlexContainerWeightPrimitiveContent("weight")))
    #Device Model DeviceLight
    CheckResponse(CreateResource(cse + "/" + ae + "/Box-" + str(box_counter) , HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["FlexContainer"]), FlexContainerDeviceLightPrimitiveContent("DeviceLight")))
    #FlexContainer binarySwitch
    CheckResponse(CreateResource(cse + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["FlexContainer"]), FlexContainerBinarySwitchPrimitiveContent("binarySwitch")))
    #FlexContainer colour
    CheckResponse(CreateResource(cse + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", HeaderFields(user, app_id + request_counter.increment(), releaseVersionIndicator, resourceTypes["FlexContainer"]), FlexContainerColorPrimitiveContent("colour")))
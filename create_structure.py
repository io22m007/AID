import requests

resourceTypes = {
    "ApplicationEntity" : "ty=2",
    "Container" : "ty=3",
    "ContentInstance" : "ty=4",
    "FlexContainer" : "ty=28"
}

def Create(url:str, originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str, primitiveContent):
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json;' + resourceType,
        'Accept': 'application/json'
    }
    print(url)
    print(headers)
    print(primitiveContent)
    return requests.post(url, headers=headers, json=primitiveContent)

def ApplicationEntityPrimitiveContent(resourceName:str, App_ID:str, requestReachability:str, supportedReleaseVersions:dict):
    data = {
        "m2m:ae": {
            "rn": resourceName,
            "api": App_ID,
            "rr": requestReachability,
            "srv": supportedReleaseVersions
        }
    }
    return data

def ContainerPrimitiveContent(resourceName:str):
    data = {
        "m2m:cnt": {
            "rn": resourceName
        }
    }
    return data

def ContentInstancePrimitiveContent(content:str):
    data = {
        "m2m:cin": {
            "cnf": "text/plain:0",
            "con": content
        }
    }
    return data

def FlexContainerWeightPrimitiveContent(resourceName:str):
    data = {
        "cod:weigt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.weight", #TS23 5.3.1.99
            "weigt": 0
        }
    }
    return data

def FlexContainerColorPrimitiveContent(resourceName:str):
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

def FlexContainerBinarySwitchPrimitiveContent(resourceName:str):
    data = {
        "cod:binSh": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.binarySwitch",
            "powSe": False
        }
    }
    return data

def DeviceModelDeviceLightPrimitiveContent(resourceName:str):
    data = {
        "cod:devLt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.device.deviceLight"
        }
    }
    return data

def DeviceModelDeviceScalePrimitiveContent(resourceName:str):
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
#CheckResponse(Create("http://localhost:8080/cse-in", "Cmyself", "0001", "3", resourceTypes["ApplicationEntity"], ApplicationEntityPrimitiveContent("Notebook-AE", "NnotebookAE", True, ["3"])))
#Container
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE", "Cmyself", "0002", "3", resourceTypes["Container"], ContainerPrimitiveContent("Container")))
#ContentInstance
#CheckResponse(Create("http://localhost:8080/cse-in/Notebook-AE/Container", "Cmyself", "0003", "3", resourceTypes["ContentInstance"], ContentInstancePrimitiveContent("Hello, World!")))

#Application Entity
CheckResponse(Create("http://192.168.1.108:8080/cse-in", "Cmyself", "0001", "4", resourceTypes["ApplicationEntity"], ApplicationEntityPrimitiveContent("Regal-AE", "NRegalAE", True, ["4"])))
#Container
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE", "Cmyself", "0002", "4", resourceTypes["Container"], ContainerPrimitiveContent("Box-1")))
#Device Model DeviceScale
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE/Box-1", "Cmyself", "0004", "4", resourceTypes["FlexContainer"], DeviceModelDeviceScalePrimitiveContent("DeviceScale")))
#FlexContainer Weight
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE/Box-1/DeviceScale", "Cmyself", "0003", "4", resourceTypes["FlexContainer"], FlexContainerWeightPrimitiveContent("weight")))
#Device Model DeviceLight
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE/Box-1", "Cmyself", "0004", "4", resourceTypes["FlexContainer"], DeviceModelDeviceLightPrimitiveContent("DeviceLight")))
#FlexContainer binarySwitch
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE/Box-1/DeviceLight", "Cmyself", "0005", "4", resourceTypes["FlexContainer"], FlexContainerBinarySwitchPrimitiveContent("binarySwitch")))
#FlexContainer colour
CheckResponse(Create("http://192.168.1.108:8080/cse-in/Regal-AE/Box-1/DeviceLight", "Cmyself", "0006", "4", resourceTypes["FlexContainer"], FlexContainerColorPrimitiveContent("colour")))


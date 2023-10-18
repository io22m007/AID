import requests

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

#FlexContainer amountPiecesInBox
def FlexContainerAmountPiecesInBoxPrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:amPIB": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.moduleclass.amountPiecesInBox",
            "pices": 0
        }
    }
    return data

#FlexContainer minimumPiecesInBox
def FlexContainerMinimumPiecesInBoxPrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:miPIB": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.moduleclass.minimumPiecesInBox",
            "pices": 0
        }
    }
    return data

#FlexContainer weightPerPiece
def FlexContainerWeightPerPiecePrimitiveContent(resourceName:str) -> dict:
    data = {
        "cod:weigt": {
            "rn": resourceName,
            "cnd": "org.onem2m.common.moduleclass.weight", #TS23 5.3.1.99
            "weigt": 0
        }
    }
    return data

#FlexContainer orderstatusBox
def FlexContainerOrderstatusBoxPrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:osBox": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.moduleclass.orderstatusBox",
            "orsta": 0
        }
    }
    return data

#FlexContainer deviceVariables
def FlexContainerDeviceVariablesPrimitiveContent(resourceName:str) -> dict:
    data = {
        "mio:devVar": {
            "rn": resourceName,
            "cnd": "org.fhtwmio.common.device.mioDeviceVariables"
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

cse = "http://acme-in:8080/cse-in" # URL includes AE and resource names
ae =  "Regal-NodeRed-AE"
box = "Box-1"
user = "CAdmin"

#Application Entity
CheckResponse(CreateResource(cse, HeaderFields(user, "0001", "3", resourceTypes["ApplicationEntity"]), ApplicationEntityPrimitiveContent(ae, "NRegalNodeRedAE", True, ["3"])))
#Container
CheckResponse(CreateResource(cse + "/" + ae, HeaderFields(user, "0002", "3", resourceTypes["Container"]), ContainerPrimitiveContent(box)))
#FlexContainer DeviceVariables
CheckResponse(CreateResource(cse + "/" + ae + "/" + box , HeaderFields(user, "0004", "3", resourceTypes["FlexContainer"]), FlexContainerDeviceVariablesPrimitiveContent("DeviceVariables")))
#FlexContainer amountPiecesInBox
CheckResponse(CreateResource(cse + "/" + ae + "/" + box + "/DeviceVariables", HeaderFields(user, "0003", "3", resourceTypes["FlexContainer"]), FlexContainerAmountPiecesInBoxPrimitiveContent("amountPiecesInBox")))
#FlexContainer minimumPiecesInBox
CheckResponse(CreateResource(cse + "/" + ae + "/" + box + "/DeviceVariables", HeaderFields(user, "0003", "3", resourceTypes["FlexContainer"]), FlexContainerMinimumPiecesInBoxPrimitiveContent("minimumPiecesInBox")))
#FlexContainer weightPerPiece
CheckResponse(CreateResource(cse + "/" + ae + "/" + box + "/DeviceVariables", HeaderFields(user, "0003", "3", resourceTypes["FlexContainer"]), FlexContainerWeightPerPiecePrimitiveContent("weightPerPiece")))
#FlexContainer orderstatusBox
CheckResponse(CreateResource(cse + "/" + ae + "/" + box + "/DeviceVariables", HeaderFields(user, "0003", "3", resourceTypes["FlexContainer"]), FlexContainerOrderstatusBoxPrimitiveContent("orderstatusBox")))
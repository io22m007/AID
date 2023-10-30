import requests
import time

class AE_Creation:
    resourceTypes = { # TS0004 6.3.4.2.1
        "ApplicationEntity" : "ty=2",
        "Container" : "ty=3",
        "ContentInstance" : "ty=4",
        "Subscription" : "ty=23",
        "FlexContainer" : "ty=28"
    }

    def CreateResource(self, url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
        return requests.post(url, headers=headers, json=primitiveContent, verify=False)

    def SubscribeResource(self, url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
        return requests.post(url, headers=headers, json=primitiveContent, verify=False)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str) -> dict:
        headers = {
            'X-M2M-Origin': originator,
            'X-M2M-RI': requestIdentifier,
            'X-M2M-RVI': releaseVersionIndicator,
            'Content-Type': 'application/json;' + resourceType,
            'Accept': 'application/json'
        }
        return headers

    #ApplicationEntity
    def ApplicationEntityPrimitiveContent(self, resourceName:str, App_ID:str, requestReachability:str, supportedReleaseVersions:dict) -> dict:
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
    def ContainerPrimitiveContent(self, resourceName:str) -> dict:
        data = {
            "m2m:cnt": {
                "rn": resourceName
            }
        }
        return data

    #ContentInstance
    def ContentInstancePrimitiveContent(self, content:str) -> dict:
        data = {
            "m2m:cin": {
                "cnf": "text/plain:0",
                "con": content
            }
        }
        return data

    #FlexContainer weight
    def FlexContainerWeightPrimitiveContent(self, resourceName:str) -> dict:
        data = {
            "cod:weigt": {
                "rn": resourceName,
                "cnd": "org.onem2m.common.moduleclass.weight", #TS23 5.3.1.99
                "weigt": 0
            }
        }
        return data

    #FlexContainer colour
    def FlexContainerColorPrimitiveContent(self, resourceName:str) -> dict:
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
    def FlexContainerBinarySwitchPrimitiveContent(self, resourceName:str) -> dict:
        data = {
            "cod:binSh": {
                "rn": resourceName,
                "cnd": "org.onem2m.common.moduleclass.binarySwitch",
                "powSe": False
            }
        }
        return data

    #FlexContainer deviceLight
    def FlexContainerDeviceLightPrimitiveContent(self, resourceName:str) -> dict:
        data = {
            "cod:devLt": {
                "rn": resourceName,
                "cnd": "org.onem2m.common.device.deviceLight"
            }
        }
        return data

    #FlexContainer mioDeviceScale
    def FlexContainerDeviceScalePrimitiveContent(self, resourceName:str) -> dict:
        data = {
            "mio:devSca": {
                "rn": resourceName,
                "cnd": "org.fhtwmio.common.device.mioDeviceScale"
            }
        }
        return data

    def SubscriptionPrimitiveContent(self, resourceName:str, notificationURL, notificationContentType:int, notificationEventType) -> dict:
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

    def CheckResponse(self, response:requests.models.Response) -> str:
        return_value = ""
        if response.status_code == 201:
            print("POST request successful")
            print("Response Content:")
            print(response.text)
            print()
            return_value = response.text
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            print()
            return_value = "request failed"
        return return_value

    def __init__(self, cse:str, cse_rn:str, ae:str, app_id:str, box_count:int, user:str, releaseVersionIndicator:str, notificationURLRegal:str, notificationURLNodeRed:str):
        #Application Entity
        self.CheckResponse(self.CreateResource(cse + "/" + cse_rn, self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["ApplicationEntity"]), self.ApplicationEntityPrimitiveContent(ae, app_id, True, ["3"])))

        for box_counter in range(1, box_count+1):
            #Container
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae, self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Container"]), self.ContainerPrimitiveContent("Box-" + str(box_counter))))
            #Device Model DeviceScale
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) , self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), self.FlexContainerDeviceScalePrimitiveContent("DeviceScale")))
            #FlexContainer Weight
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceScale", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), self.FlexContainerWeightPrimitiveContent("weight")))
            #Device Model DeviceLight
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) , self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), self.FlexContainerDeviceLightPrimitiveContent("DeviceLight")))
            #FlexContainer binarySwitch
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), self.FlexContainerBinarySwitchPrimitiveContent("binarySwitch")))
            #FlexContainer colour
            self.CheckResponse(self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), self.FlexContainerColorPrimitiveContent("colour")))

            #Subscribe LED Status
            self.CheckResponse(self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceLight/binarySwitch", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceLightBinarySwitch", [notificationURLRegal], 2, [1])))
            #Subscribe LED Color
            self.CheckResponse(self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceLight/colour", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceLightColour", [notificationURLRegal], 2, [1])))
            #Subscribe Weight
            #self.CheckResponse(self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceScale/weight", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceScaleWeight", [notificationURLNodeRed], 2, [1])))

import requests
import time

class AE_Creation:
    # Dictonary with select one M2M Resource Types from TS0004 6.3.4.2.1
    resourceTypes = {
        "ApplicationEntity" : "ty=2",
        "Container" : "ty=3",
        "ContentInstance" : "ty=4",
        "Subscription" : "ty=23",
        "FlexContainer" : "ty=28"
    }

    def CreateResource(self, url:str, headers:dict, primitiveContent:dict, certificateAuthority:str) -> requests.models.Response:
        """
        Used to create a new resource.
        Returns the response from the HTTP REST API POST request to the ASN CSE ACME.

        Parameters:
            self (the class)
            url (full path incl. protocol, ip/hostname, port, path): str
            headers (headers created with HeaderFields method) : dict
            primitiveContent (the content of the POST request which is created by one of many methods) : dict
            certificateAuthority (path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME): str
        Returns:
            response (response from the request) : requests.models.Response
        """
        return requests.post(url, headers=headers, json=primitiveContent, verify=certificateAuthority)

    def SubscribeResource(self, url:str, headers:dict, primitiveContent:dict, certificateAuthority:str) -> requests.models.Response:
        """
        Used to create a new subscription.
        Returns the response from the HTTP REST API POST request to the ASN CSE ACME.
        
        Parameters:
            self (the class)
            url (full path incl. protocol, ip/hostname, port, path): str
            headers (headers created with HeaderFields method) : dict
            primitiveContent (the content of the POST request which is created by one of two methods) : dict
            certificateAuthority (path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME): str
        Returns:
            response (response from the request) : requests.models.Response
        """
        return requests.post(url, headers=headers, json=primitiveContent, verify=certificateAuthority)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str, resourceType:str) -> dict:
        """
        Returns the HTTP REST API header for communication with the ASN CSE ACME as a dictionary.
        The dict contains the given parameters and that json is the content exchange format.

        Parameters:
            self (the class)
            originator (user that is sending the request) : str
            requestIdentifier (app id + timestamp) : str
            releaseVersionIndicator (version of oneM2M) : str
            resourceType (type of ressource which will be created from resourceTypes dictionary): str
        Returns:
            headers : dict
        """
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
        """
        Returns the primitive content for an application entity as a dictionary.
        The dict contains the given parameters.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
            App_ID (identifier of the application entity) : str
            requestReachability : str
            supportedReleaseVersions (version of oneM2M) : dict
        Returns:
            dict : dict
        """
        data = {
            "m2m:ae": {
                "rn": resourceName,
                "api": App_ID,
                "rr": requestReachability,
                "srv": supportedReleaseVersions,
                "acpi": ["acpCreateACPs"]
            }
        }
        return data

    #Container
    def ContainerPrimitiveContent(self, resourceName:str) -> dict:
        """
        Returns the primitive content for a container as a dictionary.
        The dict contains the given parameters.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
        data = {
            "m2m:cnt": {
                "rn": resourceName
            }
        }
        return data

    #FlexContainer weight
    def FlexContainerWeightPrimitiveContent(self, resourceName:str) -> dict:
        """
        Returns the primitive content for a weight flex container as a dictionary.
        The dict contains the given parameters and the moduleclass path.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
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
        """
        Returns the primitive content for a color flex container as a dictionary.
        The dict contains the given parameters, the moduleclass path and the inital value for the colors red, green and blue.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
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
        """
        Returns the primitive content for a binary switch flex container as a dictionary.
        The dict contains the given parameters, the moduleclass path and the inital value for the powerState.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
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
        """
        Returns the primitive content for a device light flex container as a dictionary.
        The dict contains the given parameters and the moduleclass path.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
        data = {
            "cod:devLt": {
                "rn": resourceName,
                "cnd": "org.onem2m.common.device.deviceLight"
            }
        }
        return data

    #FlexContainer mioDeviceScale
    def FlexContainerDeviceScalePrimitiveContent(self, resourceName:str) -> dict:
        """
        Returns the primitive content for a device scale container as a dictionary.
        The dict contains the given parameters and the moduleclass path.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
        Returns:
            data : dict
        """
        data = {
            "mio:devSca": {
                "rn": resourceName,
                "cnd": "org.fhtwmio.common.device.mioDeviceScale"
            }
        }
        return data

    def SubscriptionPrimitiveContent(self, resourceName:str, notificationURL:list, notificationContentType:int, notificationEventType:list) -> dict:
        """
        Returns the primitive content for subscription as a dictionary.
        The dict contains the given parameters.

        Parameters:
            self (the class)
            resourceName (name of the resource) : str
            notificationURL (where the notification should be sent to, protocol + ip/hostname + port) : list
            notificationContentType (which data should be send as a notification) : str
            notificationEventType (the types of events notifications shoud be send about) : list
        Returns:
            data : dict
        """
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
        """
        Check if a HTTP REST API request was successful. Prints a few lines to the console.
            self (the class)
            response (the repsonse from the HTTP REST API request to ASN CSE ACME) : requests.models.Response
        Returns:
            response_text (response text) : str
        """
        response_text = ""
        # When respone is of HTTP status code 201 (created) 
        if response.status_code == 201:
            print("POST request successful")
            print("Response Content:")
            print(response.text)
            print()
            response_text = response.text
        else:
            print(f"POST request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            print()
            response_text = "request failed"
        return response_text

    def __init__(self, cse:str, cse_rn:str, ae:str, app_id:str, box_count:int, user:str, releaseVersionIndicator:str, notificationURLRegal:str, notificationURLNodeRed:str, certificateAuthority:str):
        """
        Application to create the complete application entity on the ASN CSE ACME.
        
        Parameters:
            self (the class)
            cse (protocol http/https, ip or hostname, colon and port of the ASN CSE ACME) : str
            cse_rn (the resourcename of the ASN CSE ACME) : str
            ae (the name of the application entity which will be created) : str
            app_id (the ID of the application entity which will be created - this information will also form part of the request identifier) : str
            box_count (the number of boxes on the Raspi) : int
            user (the user which will create the AE on the ASN CSE ACME) : str
            releaseVersionIndicator (the version of oneM2M) : str
            notificationURLRegal (protocol http/https, ip or hostname, colon and port of the notification server of this application) : str
            notificationURLNodeRed (protocol http/https, ip or hostname, colon and port of the notification server of the remote NodeRed application) : str
            certificateAuthority (the path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME) : str
        """
        
        #Application Entity
        self.CheckResponse(
            self.CreateResource(cse + "/" + cse_rn, 
                                self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["ApplicationEntity"]), 
                                self.ApplicationEntityPrimitiveContent(ae, app_id, True, ["3"]), 
                                certificateAuthority))

        for box_counter in range(1, box_count+1):
            #Container
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae, 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Container"]), 
                                    self.ContainerPrimitiveContent("Box-" + str(box_counter)), 
                                    certificateAuthority))
            #Device Model DeviceScale
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter), 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), 
                                    self.FlexContainerDeviceScalePrimitiveContent("DeviceScale"), 
                                    certificateAuthority))
            #FlexContainer Weight
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceScale", 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), 
                                    self.FlexContainerWeightPrimitiveContent("weight"), 
                                    certificateAuthority))
            #Device Model DeviceLight
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) , 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), 
                                    self.FlexContainerDeviceLightPrimitiveContent("DeviceLight"), 
                                    certificateAuthority))
            #FlexContainer binarySwitch
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), 
                                    self.FlexContainerBinarySwitchPrimitiveContent("binarySwitch"), 
                                    certificateAuthority))
            #FlexContainer colour
            self.CheckResponse(
                self.CreateResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter)  + "/DeviceLight", 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["FlexContainer"]), 
                                    self.FlexContainerColorPrimitiveContent("colour"), 
                                    certificateAuthority))

            #Subscribe LED Status notifications - only modified attributes (2) and only resource update events
            self.CheckResponse(
                self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceLight/binarySwitch", 
                                       self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), 
                                       self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceLightBinarySwitch", [notificationURLRegal], 2, [1]), 
                                       certificateAuthority))
            #Subscribe LED Color - only modified attributes (2) and only resource update events
            self.CheckResponse(
                self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceLight/colour", 
                                       self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), 
                                       self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceLightColour", [notificationURLRegal], 2, [1]), 
                                       certificateAuthority))
            #Subscribe Weight - only modified attributes (2) and only resource update events
            self.CheckResponse(
                self.SubscribeResource(cse + "/" + cse_rn + "/" + ae + "/Box-" + str(box_counter) + "/DeviceScale/weight", 
                                       self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["Subscription"]), 
                                       self.SubscriptionPrimitiveContent("Box" + str(box_counter) + "SubscriptionDeviceScaleWeight", [notificationURLNodeRed], 2, [1]), 
                                       certificateAuthority))

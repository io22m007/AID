import requests
import time

class AccessControlEdit:
    # Dictonary with select one M2M Resource Types from TS0004 6.3.4.2.1
    resourceTypes = {
        "AccessControlPolicy" : "ty=1"
    }

    def UpdateAccessControlPolicy(self, url:str, headers:dict, primitiveContent:dict, certificateAuthority:str) -> requests.models.Response:
        return requests.put(url, headers=headers, json=primitiveContent, verify=certificateAuthority)

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


    
    def UpdateAccessControlOperationsPrimitiveContent(self, accessControlRessources:list) -> dict:
        acr = []

        for accessControlRessource in accessControlRessources:
            acr.append(
                {
                    "acop": accessControlRessource[0],
                    "acor": [accessControlRessource[1]]
                }
            )
        
        data = {
            "m2m:acp":{
                "pv": {
                    "acr": acr
                }
            }
        }
        return data

    def CheckResponse(self, response:requests.models.Response) -> str:
        """
        Check if a HTTP REST API request was successful. Prints a few lines to the console.

        Parameters:
            self (the class)
            response (the repsonse from the HTTP REST API request to ASN CSE ACME) : requests.models.Response
        Returns:
            response_text (response text) : str
        """
        return_value = ""
        #When respone is of HTTP status code 200 (ok) 
        if response.status_code == 200:
            print("PUT request successful")
            print("Response Content:")
            print(response.text)
            print()
            return_value = response.text
        else:
            print(f"PUT request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            print()
            return_value = "request failed"
        return return_value

    def __init__(self, cse:str, cse_rn:str, app_id:str, user:str, acp:str, acr:list, releaseVersionIndicator:str, certificateAuthority:str):
        self.CheckResponse(
            self.UpdateAccessControlPolicy(cse + "/" + cse_rn + "/" + acp, 
                                    self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator, self.resourceTypes["AccessControlPolicy"]), 
                                    self.UpdateAccessControlOperationsPrimitiveContent(acr),
                                    certificateAuthority))

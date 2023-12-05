import requests
import time

class CheckOnline:
    def GetResource(self, url:str, headers:dict, certificateAuthority:str) -> requests.models.Response:
        return requests.get(url, headers=headers, verify=certificateAuthority)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
        headers = {
            'X-M2M-Origin': originator,
            'X-M2M-RI': requestIdentifier,
            'X-M2M-RVI': releaseVersionIndicator,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def __init__(self, cse:str, app_id:str, user:str, releaseVersionIndicator:str, certificateAuthority:str):
        connected = False

        while not connected:
            time.sleep(10)
            try:
                self.GetResource(cse + "/test", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator), certificateAuthority)
                connected = True
                print("acme online")
            except requests.exceptions.ConnectionError as e:
                print("acme not online, retrying")
                print(str(e))

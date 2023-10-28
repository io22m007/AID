import requests
import time

class CheckOnline:
    def GetResource(self, url:str, headers:dict) -> requests.models.Response:
        return requests.get(url, headers=headers)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
        headers = {
            'X-M2M-Origin': originator,
            'X-M2M-RI': requestIdentifier,
            'X-M2M-RVI': releaseVersionIndicator,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def __init__(self, cse:str, cse_id:str, app_id:str, user:str, releaseVersionIndicator:str):
        connected = False

        while not connected:
            try:
                self.GetResource(cse + "/" + cse_id, self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator))
                connected = True
            except requests.exceptions.ConnectionError:
                print("acme not online, retrying")
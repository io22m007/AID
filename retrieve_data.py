import requests

def GetResource(url:str, headers:dict) -> requests.models.Response:
    return requests.get(url, headers=headers)

def HeaderFields(originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
    headers = {
        'X-M2M-Origin': originator,
        'X-M2M-RI': requestIdentifier,
        'X-M2M-RVI': releaseVersionIndicator,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    return headers

def CheckResponse(response:requests.models.Response):
    if response.status_code == 200:
        print("GET request successful")
        print("Response Content:")
        print(response.text)
        print()
    else:
        print(f"GET request failed with status code: {response.status_code}")
        print("Response Content:")
        print(response.text)
        print()


cse = "http://acme-in:8080/cse-in/cse-asn" # URL includes AE and resource names
ae = "/Regal-AE"
box = "/Box-1"

CheckResponse(GetResource(cse + ae + box + "/DeviceScale/weight", HeaderFields("CAIDAdmin", "0501", "3")))
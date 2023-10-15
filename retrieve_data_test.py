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


# Achtung bei der Abfrage der Ressourcen! Hier ist ei Beispiel mit Testdaten
cse = "http://192.168.8.196:8080/~/" # URL includes cse-in
csr = "id-asn/cse-asn" # Replace with id-asn/cse-asn
ressource = "/Regal-AE/Box-1/DeviceLight/colour"
user = "CAIDAdmin"

CheckResponse(GetResource(cse + csr + ressource, HeaderFields(user, "0501", "3")))
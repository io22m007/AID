import requests
import time

class CheckOnline:
    
    def GetResource(self, url:str, headers:dict, certificateAuthority:str) -> requests.models.Response:
        """
        Returns the response from the HTTP REST API request to the ASN CSE ACME.
        Parameters:
            self (the class)
            url (full path incl. protocol, ip/hostname, port, path): str
            headers (headers created with HeaderFields method) : dict
            certificateAuthority (path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME): str
        Returns:
            request-response : requests.models.Response
        """
        return requests.get(url, headers=headers, verify=certificateAuthority)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
        """
        Returns the HTTP REST API header for communication with the ASN CSE ACME as a dictionary.
        The dict contains the given parameters and that json is the content exchange format.

        Parameters:
            self (the class)
            originator (user that is sending the request) : str
            requestIdentifier (app id + timestamp) : str
            releaseVersionIndicator (version of oneM2M) : str
        Returns:
            headers : dict
        """
        headers = {
            'X-M2M-Origin': originator,
            'X-M2M-RI': requestIdentifier,
            'X-M2M-RVI': releaseVersionIndicator,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def __init__(self, cse:str, app_id:str, user:str, releaseVersionIndicator:str, certificateAuthority:str):
        """
        Application to check if the ASN CSE ACME is already online.

        Parameters:
            self (the class)
            cse (protocol http/https, ip or hostname, colon and port of the ASN CSE ACME) : str
            app_id (the ID of the application entity which will be created - this information will form part of the request identifier) : str
            user (the user that will be used for the communication with the ASN CSE ACME) : str
            releaseVersionIndicator (the version of one M2M) : str
            certificateAuthority (the path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME) : str
        """
        #Boolean variable to save if a connection to ASN CSE ACME was successfully established with an initial  value of False
        connected = False

        #Do the following while a connection to ASN CSE ACME was not successfully established yet
        while not connected:
            #Wait for ten seconds
            time.sleep(10)
            #Try to connect to the ASN CSE ACME
            try:
                #Try to connect to the ASN CSE ACME with the GetResource method - /test directory does not exit but when the ASN CSE ACME is reachable it will still send a response
                self.GetResource(cse + "/test", self.HeaderFields(user, app_id + "-" + str(time.time()), releaseVersionIndicator), certificateAuthority)
                #When the request was successful  set the connected variable to True
                connected = True
                #Print that the ASN CSE ACME is now online
                print("acme online")
            #When the connection to the ASN CSE ACME was not possible to following exception will be triggered
            except requests.exceptions.ConnectionError as e:
                #Print that the ASN CSE ACME is not online yet
                print("acme not online, retrying")
                #Print the exception data
                print(str(e))

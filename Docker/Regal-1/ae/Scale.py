from hx711 import HX711
import threading
import requests
import time

class Scale(threading.Thread):
    def __init__(self, exit_event:threading.Event, cse:str, cse_rn:str, ae:str, app_id:str, box_count:int, user:str, releaseVersionIndicator:str, scales:list, certificateAuthority:str):
        super().__init__()
        self.exit_event = exit_event
        self.cse = cse
        self.cse_rn = cse_rn
        self.ae = ae
        self.app_id = app_id
        self.box_count = box_count
        self.user = user
        self.releaseVersionIndicator = releaseVersionIndicator
        self.scales = scales
        self.certificateAuthority = certificateAuthority

    def UpdateResource(self, url:str, headers:dict, primitiveContent:dict, certificateAuthority:str) -> requests.models.Response:
        """
        Used to get a resource.
        Returns the response from the HTTP REST API PUT request to the ASN CSE ACME.
        
        Parameters:
            self (the class)
            url (full path incl. protocol, ip/hostname, port, path): str
            headers (headers created with HeaderFields method) : dict
            primitiveContent (the content of the PUT request which is created by the RegalBoxDeviceScaleWeightUpdatePrimitiveContent method) : dict
            certificateAuthority (path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME): str
        Returns:
            response (response from the request) : requests.models.Response
        """
        return requests.put(url, headers=headers, json=primitiveContent, verify=certificateAuthority)

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

    def RegalBoxDeviceScaleWeightUpdatePrimitiveContent(self, weight:float) -> dict:
        """
        Returns the primitive content to update a weight flex container as a dictionary.
        The dict contains the given parameter.

        Parameters:
            self (the class)
            weight (the new weight in kilograms) : float
        Returns:
            data : dict
        """
        data = {
            "cod:weigt": {
                "weigt": weight
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
        # When respone is of HTTP status code 200 (ok) 
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

    def SetupScale(self, scales:list) -> list:
        """
        Configure an instance of the HX711 library for each scale.

        Parameters:
            self (the class)
            scales (list of scales, each entry in the list is a list with the two pins dt and sck, the inital offset and the ration) : list
        Returns:
            scale_list (list of configured scales) : list
        """
        scale_list = []

        #For each entry in the scale list
        for scale_data in scales:
            #Create an instance of the HX711 library with the dt and sck pins
            hx = HX711(dout_pin=scale_data[0], pd_sck_pin=scale_data[1])
            #Set the offset
            hx.set_offset(scale_data[2], channel=hx.get_current_channel(), gain_A=hx.get_current_gain_A())
            #Set the ration
            hx.set_scale_ratio(scale_data[3])
            scale_list.append(hx)

        return scale_list

    def run(self):
        """
        Thread start
        """
        #Initial scale configuration
        scale_list = self.SetupScale(self.scales)
        #List to save three recent values per scale
        recent_values = []
        #
        for box_counter in range(1, self.box_count + 1):
            recent_values.append([0,0,0])
            
        print("scale setup done, run scale thread in endless loop")
        value_counter = 0
        while not self.exit_event.is_set():
            start = time.time()
            for box_counter in range(1, self.box_count + 1):
                print(str(box_counter))
                #Get a scale reading by averaging of 10 values
                reading = scale_list[box_counter - 1].get_weight_mean(10)
                if reading:
                    #Save the current reading in the list for the current scale and the current value_counter position (0-2)
                    recent_values[box_counter - 1][value_counter] = reading
                    #When the three values have been read
                    if value_counter == 2:
                        #Check if the three recent values for a particular scale are within 3% of each other
                        if abs(
                            (recent_values[box_counter - 1][0] - recent_values[box_counter - 1][1]) / recent_values[box_counter - 1][0]) <= 0.03 and abs(
                                (recent_values[box_counter - 1][1] - recent_values[box_counter - 1][2]) / recent_values[box_counter - 1][1]) <= 0.03 and abs(
                                    (recent_values[box_counter - 1][0] - recent_values[box_counter - 1][2]) / recent_values[box_counter - 1][0]) <= 0.03:
                            #When the three recent values for a particular scale are within 3% of each other send the latest value
                            self.CheckResponse(
                                self.UpdateResource(self.cse + "/" + self.cse_rn + "/" + self.ae + "/Box-" + str(box_counter) + "/DeviceScale/weight", 
                                                    self.HeaderFields(self.user, self.app_id + "-" + str(time.time()), self.releaseVersionIndicator), 
                                                    self.RegalBoxDeviceScaleWeightUpdatePrimitiveContent(reading/1000), self.certificateAuthority))
                        else:
                            print("scale values don't agree")
                print(recent_values)

            if value_counter == 2:
                value_counter = 0
            else:
                value_counter = value_counter + 1

            try:
                #A cycle should last at least three seconds.
                #If the cycle is shorter than three seconds then sleep for the remaining time
                #If the cycle is already longer than three seconds then an error will occure (can't sleep negative time) which is why the try-except is in place
                time.sleep(time.time() - start - 3)
            except:
                pass

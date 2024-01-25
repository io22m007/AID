import threading
import queue
import requests
import time
import json
import RPi.GPIO

class LedPwm(threading.Thread):
    def __init__(self, exit_event:threading.Event, data_queue:queue.Queue, cse:str, app_id:str, user:str, releaseVersionIndicator:str, leds:list, GPIO:RPi.GPIO, certificateAuthority:str):
        super().__init__()
        self.exit_event = exit_event
        self.data_queue = data_queue
        self.cse = cse
        self.app_id = app_id
        self.user = user
        self.releaseVersionIndicator = releaseVersionIndicator
        self.leds = leds
        self.GPIO = GPIO
        self.certificateAuthority = certificateAuthority

    def GetResource(self, url:str, headers:dict, certificateAuthority:str) -> requests.models.Response:
        """
        Used to get a resource.
        Returns the response from the HTTP REST API GET request to the ASN CSE ACME.
        
        Parameters:
            self (the class)
            url (full path incl. protocol, ip/hostname, port, path): str
            headers (headers created with HeaderFields method) : dict
            certificateAuthority (path to the certificate authority certificate which was used to sign the certificate of the ASN CSE ACME): str
        Returns:
            response (response from the request) : requests.models.Response
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

    def CheckResponse(self, response:requests.models.Response) -> str:
        """
        Check if a HTTP REST API request was successful. Prints a few lines to the console.

        Parameters:
            self (the class)
            response (the repsonse from the HTTP REST API request to ASN CSE ACME) : requests.models.Response
        Returns:
            response_text (response text) : str
        """
        response_text = ""
        # When respone is of HTTP status code 200 (ok) 
        if response.status_code == 200:
            print("GET request successful")
            print("Response Content:")
            print(response.text)
            print()
            response_text = response.text
        else:
            print(f"GET request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            print()
            response_text = "request failed"
        return response_text

    def GetSubscriptionResourceName(self, response_text:str) -> str:
        """
        Try to extract the subscription resource name.

        Parameters:
            self (the class)
            response_text (the repsonse content from the HTTP REST API request to ASN CSE ACME) : str
        Returns:
            response_text (response text) : str
        """
        try:
            json_object = json.loads(response_text)
            return json_object["m2m:sub"]["rn"]
        except:
            return response_text

    def SetupLEDs(self, leds:list) -> list:
        """
        Configure the GPIO pins for the LEDs.

        Parameters:
            self (the class)
            leds (list of leds, each entry in the list is a list with the three pins of the leds for red, green and blue) : list
        Returns:
            led_list (list of configured leds) : list
        """
        led_list = []

        power_state = False
        red_color = 0
        green_color = 0
        blue_color = 0

        #For each entry in the leds list
        for led_pins in leds:
            #Set the LED GPIO pins to output mode
            self.GPIO.setup(led_pins[0], self.GPIO.OUT)
            self.GPIO.setup(led_pins[1], self.GPIO.OUT)
            self.GPIO.setup(led_pins[2], self.GPIO.OUT)

            #Set the GPIO pins to PWM with 100Hz
            red_pwm = self.GPIO.PWM(led_pins[0], 100)
            green_pwm = self.GPIO.PWM(led_pins[1], 100)
            blue_pwm = self.GPIO.PWM(led_pins[2], 100)

            #Atart the GPIO PWM for the pins
            red_pwm.start(0)
            green_pwm.start(0)
            blue_pwm.start(0)

            #Add the three led pins, the power state of the LED and the three values for the individual RGB colors as a list to the led_list
            led_list.append([red_pwm, green_pwm, blue_pwm, power_state, red_color, green_color, blue_color])

        return led_list

    def UpdatePWM(self, led_list:list, led_id:int):
        """
        Change the state and color of an LED with PWM.
        
        Parameters:
            self (the class)
            led_list (the list of all LEDs which was created with the SetupLEDs method were each entry consists of led pins, power state and colors) : list
            led_id (which LED in the led_list to use) : int
        """
        #When the powerState is False turn of all LEDs
        if led_list[led_id][3] == False:
            led_list[led_id][0].ChangeDutyCycle(0)
            led_list[led_id][1].ChangeDutyCycle(0)
            led_list[led_id][2].ChangeDutyCycle(0)
        #When the powerState is True set the new color
        elif led_list[led_id][3] == True:
            #change the pwm cycle to the rgb values (0-255) devided by 255 (0-1) multiplied by 100 (0-100) and rounded to zero decimal places
            led_list[led_id][0].ChangeDutyCycle(round(led_list[led_id][4]/255*100))
            led_list[led_id][1].ChangeDutyCycle(round(led_list[led_id][5]/255*100))
            led_list[led_id][2].ChangeDutyCycle(round(led_list[led_id][6]/255*100))

    def UpdateLEDs(self, led_list:list, json_message:dict, subscription_resource_name:str) -> list:
        """
        Update the values in the

        Parameters:
            self (the class)
            led_list (the list of all LEDs which was created with the SetupLEDs method were each entry consists of led pins, power state and colors) : list
            json_message (the notification from the ASN CSE ACME in json format) : dict
            subscription_resource_name (the resource name of the subscription - the LED is indicated by the fourth char in the string) : str
        Returns:
            led_list (the updated list) : list
        """
        #Get the LED id from the fourth char in the resource name of the subscription minus 1 (because list starts with index zero)
        led_id = int(subscription_resource_name[3]) - 1
        #When the resource name of the subscription and the module class indicates that this notification is for the binarySwitch component of the LED
        if "SubscriptionDeviceLightBinarySwitch" in subscription_resource_name and "cod:binSh" in json_message["m2m:sgn"]["nev"]["rep"]:
            #Update pwer state with the value from the json
            led_list[led_id][3] = json_message["m2m:sgn"]["nev"]["rep"]["cod:binSh"]["powSe"]
        #When the resource name of the subscription and the module class indicates that this notification is for the color component of the LED
        elif "SubscriptionDeviceLightColour" in subscription_resource_name and "cod:color" in json_message["m2m:sgn"]["nev"]["rep"]:
            #update the colors with the values from the json
            led_list[led_id][4] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["red"]
            led_list[led_id][5] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["green"]
            led_list[led_id][6] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["blue"]
        #Use UpdatePWM to update the physical LED
        self.UpdatePWM(led_list, led_id)
        return led_list

    def run(self):
        """
        Thread start
        """
        #Dict to cache subscription resources (id : name)
        subscription_resources = {}
        #Initial LED configuration
        led_list = self.SetupLEDs(self.leds)
        #Do the following while the exit event isn't set
        while not self.exit_event.is_set():
            #Get a new notification from the queue (the notification server will put messages into the queue)
            json_message = self.data_queue.get()
            #Print message to console
            print(f"Recieved: {json_message}")
            #When the subscription id isn't in the subscription_resources dict
            if json_message["m2m:sgn"]["sur"] not in subscription_resources:
                #
                subscription_resource_split = str(json_message["m2m:sgn"]["sur"]).split('/')
                #Send a HTTP REST API GET request to the ASN CSE ACME to resolve the subscription resource id to the name of the subscription resource
                #With GetSubscriptionResourceName the name is extracted from the json response
                subscription_resource_name = self.GetSubscriptionResourceName(
                                                self.CheckResponse(
                                                    self.GetResource(self.cse + "/" + subscription_resource_split[-1], 
                                                                     self.HeaderFields(self.user, self.app_id + "-" + str(time.time()), self.releaseVersionIndicator),
                                                                     self.certificateAuthority)))
                #When the request hasn't failed
                if subscription_resource_name != "request failed":
                    #Add the pair subscription resource id and subscription resource name to the caching dict
                    subscription_resources[json_message["m2m:sgn"]["sur"]] = subscription_resource_name

            #Get the subscription resource name with the subscription resource id from the cache dict
            if json_message["m2m:sgn"]["sur"] in subscription_resources:
                #Update the LEDs with the content of the message
                led_list = self.UpdateLEDs(led_list, json_message, subscription_resources[json_message["m2m:sgn"]["sur"]])
            #Tell that the current task is done    
            self.data_queue.task_done()

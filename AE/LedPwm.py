import threading
import queue
import requests
import time
import json
import RPi.GPIO as GPIO

class LedPwm(threading.Thread):
    def __init__(self, data_queue:queue.Queue, cse:str, app_id:str, box_count:int, user:str, releaseVersionIndicator:str, leds:list):
        super().__init__()
        self.data_queue = data_queue
        self.cse = cse
        self.app_id = app_id
        self.box_count = box_count
        self.user = user
        self.releaseVersionIndicator = releaseVersionIndicator
        self.leds = leds

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

    def CheckResponse(self, response:requests.models.Response) -> str:
        return_value = ""
        if response.status_code == 200:
            print("GET request successful")
            print("Response Content:")
            print(response.text)
            print()
            return_value = response.text
        else:
            print(f"GET request failed with status code: {response.status_code}")
            print("Response Content:")
            print(response.text)
            print()
            return_value = "request failed"
        return return_value

    def GetSubscriptionResourceName(self, response_text):
        json_object = json.loads(response_text)
        return json_object["m2m:sub"]["rn"]

    def SetupLEDs(self, leds:list) -> list:
        GPIO.setmode(GPIO.BCM)
        led_list = []

        status = False
        red_color = 0
        green_color = 0
        blue_color = 0

        for led_pins in leds:
            GPIO.setup(led_pins[0], GPIO.OUT)
            GPIO.setup(led_pins[1], GPIO.OUT)
            GPIO.setup(led_pins[2], GPIO.OUT)

            red_pwm = GPIO.PWM(led_pins[0], 100)
            green_pwm = GPIO.PWM(led_pins[1], 100)
            blue_pwm = GPIO.PWM(led_pins[2], 100)

            red_pwm.start(0)
            green_pwm.start(0)
            blue_pwm.start(0)

            led_list.append([red_pwm, green_pwm, blue_pwm, status, red_color, green_color, blue_color])

        return led_list

    def UpdatePWM(self, led_list:list, led_id:int):
        if led_list[led_id][3] == False:
            led_list[led_id][0].ChangeDutyCycle(0)
            led_list[led_id][1].ChangeDutyCycle(0)
            led_list[led_id][2].ChangeDutyCycle(0)
        elif led_list[led_id][3] == True:
            led_list[led_id][0].ChangeDutyCycle(led_list[led_id][4]/255*100)
            led_list[led_id][1].ChangeDutyCycle(led_list[led_id][5]/255*100)
            led_list[led_id][2].ChangeDutyCycle(led_list[led_id][6]/255*100)

    def UpdateLEDs(self, led_list:list, json_message:dict, subscription_resource_name:str) -> list:
        led_id = int(subscription_resource_name[3]) -1
        if "SubscriptionDeviceLightBinarySwitch" in subscription_resource_name and "cod:binSh" in json_message["m2m:sgn"]["nev"]["rep"]:
            led_list[led_id][3] = json_message["m2m:sgn"]["nev"]["rep"]["cod:binSh"]["powSe"]
        elif "SubscriptionDeviceLightColour" in subscription_resource_name and "cod:color" in json_message["m2m:sgn"]["nev"]["rep"]:
            led_list[led_id][4] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["red"]
            led_list[led_id][5] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["green"]
            led_list[led_id][6] = json_message["m2m:sgn"]["nev"]["rep"]["cod:color"]["blue"]

        self.UpdatePWM(led_list, led_id)
        return led_list

    def run(self):
        subscription_resources = {}
        led_list = self.SetupLEDs(self.leds)
        while True:
            json_message = self.data_queue.get()
            print(f"Consumed: {json_message}")
            if json_message["m2m:sgn"]["sur"] not in subscription_resources:
                subscription_resource_split = str(json_message["m2m:sgn"]["sur"]).split('/')
                subscription_resource_name = self.GetSubscriptionResourceName(self.CheckResponse(self.GetResource(self.cse + "/" + subscription_resource_split[-1], self.HeaderFields(self.user, self.app_id + "-" + str(time.time()), self.releaseVersionIndicator))))
                if subscription_resource_name != "request failed":
                    subscription_resources[json_message["m2m:sgn"]["sur"]] = subscription_resource_name

            if json_message["m2m:sgn"]["sur"] in subscription_resources:
                print(subscription_resources[json_message["m2m:sgn"]["sur"]])
                led_list = self.UpdateLEDs(led_list, json_message, subscription_resources[json_message["m2m:sgn"]["sur"]])
            self.data_queue.task_done()

        GPIO.cleanup()

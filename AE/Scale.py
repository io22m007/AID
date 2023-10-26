from hx711 import HX711
import threading
import requests
import time

class Scale(threading.Thread):
    def __init__(self, exit_event:threading.Event, cse:str, cse_rn:str, ae:str, app_id:str, box_count:int, user:str, releaseVersionIndicator:str, scales:list):
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

    def UpdateResource(self, url:str, headers:dict, primitiveContent:dict) -> requests.models.Response:
        print(url)
        print(url)
        print(url)
        print(url)
        return requests.put(url, headers=headers, json=primitiveContent)

    def HeaderFields(self, originator:str, requestIdentifier:str, releaseVersionIndicator:str) -> dict:
        headers = {
            'X-M2M-Origin': originator,
            'X-M2M-RI': requestIdentifier,
            'X-M2M-RVI': releaseVersionIndicator,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def RegalBoxDeviceScaleWeightUpdatePrimitiveContent(self, weight:float) -> dict:
        data = {
            "cod:weigt": {
                "weigt": weight
            }
        }
        return data

    def CheckResponse(self, response:requests.models.Response) -> str:
        return_value = ""
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
        scale_list = []

        for scale_data in scales:
            hx = HX711(dout_pin=scale_data[0], pd_sck_pin=scale_data[1])
            err = hx.zero()
            if err:
                raise ValueError('Tare is unsuccessful.')
            hx.set_scale_ratio(scale_data[2])
            scale_list.append(hx)

        return scale_list

    def run(self):
        scale_list = self.SetupScale(self.scales)
        while not self.exit_event.is_set():
            start = time.time()
            for box_counter in range(1, self.box_count + 1):
                reading = scale_list[box_counter - 1].get_weight_mean(50)
                if reading:
                    self.CheckResponse(self.UpdateResource(self.cse + "/" + self.cse_rn + "/" + self.ae + "/Box-" + str(box_counter) + "/DeviceScale/weight", self.HeaderFields(self.user, self.app_id + "-" + str(time.time()), self.releaseVersionIndicator), self.RegalBoxDeviceScaleWeightUpdatePrimitiveContent(reading/1000)))
            try:
                time.sleep(time.time() - start - 10)
            except:
                pass

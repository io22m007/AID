import threading
import configparser
import queue
import json
import RPi.GPIO as GPIO
from OnlineCheck import CheckOnline
from CreateStructure import AE_Creation
from NotificationServerSmall import NotificationServer
from LedPwm import LedPwm
from Scale import Scale

if __name__ == "__main__":
    try:
        #Inital hello message
        print("hello")
        #Create a new data queue variable for communication between the notificationServer thread and the ledPWM thread
        data_queue = queue.Queue()
        #Set the GPIO mode to BCM numbering scheme (GPIO xy)
        GPIO.setmode(GPIO.BCM)
        #Create exit event variable to end the hardware controlling threads properly on exit
        exit_event = threading.Event()
        #Create a configparser instance to load configuration file
        config = configparser.ConfigParser()
        #Load ae.ini config file into configparser instance
        config.read('ae.ini')

        #Print that the check if the ASN CSE ACME is online will now begin
        print("online check")

        #Start CheckOnline.py with the following parameters:
        #- The protocol&IP/Hostname of the ASN CSE ACME + colon + port of the ASN CSE ACME
        #- The ID of the application entity - the application entity has not been created yet, but this information will form part of the request identifier
        #- The user which will be used to check the online state
        #- The version of oneM2M
        #- The path to the Certificate Authority certificate which was used to sign the certificate of the ASN CSE ACME
        CheckOnline(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('AE', 'app_id'), config.get('CSE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('General', 'ca'))

        #Print that the notification server will now start 
        print("notification server")
        #Create a new notification server instance as a separate thread with the following parameters:
        #- The data queue variable to communicate control commands to the led pwm control thread to control the LED
        #- The port this notification server is going to use
        #- The certificate file for this notification server
        #- The private key file for this notification server
        notificationServer_thread = NotificationServer(data_queue, int(config.get('NotificationServerRegal', 'port')), config.get('NotificationServerRegal', 'certfile'), config.get('NotificationServerRegal', 'keyfile'))
        #Start the notification server thread
        notificationServer_thread.start()

        #Print that the creation of the application entity on the ASN CSE ACME will now start 
        print("ae creation")

        #Start AE_Creation.py with the following parameters:
        #- The protocol&IP/Hostname of the ASN CSE ACME + colon + port of the ASN CSE ACME
        #- The resourcename of the ASN CSE ACME
        #- The name of the application entity which will be created
        #- The ID of the application entity - this information will also form part of the request identifier
        #- The number of boxes on the Raspi (a box is a scale and a led)
        #- The user which will create the AE on the ASN CSE ACME
        #- The version of oneM2M
        #- The protocol&IP/Hostname of the notification server of this application + colon + port of the notification server of this application
        #- The protocol&IP/Hostname of the notification server of the remote NodeRed application + colon + port of the notification server of the remote NodeRed application
        #- The path to the Certificate Authority certificate which was used to sign the certificate of the ASN CSE AMCE
        AE_Creation(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('AE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('NotificationServerRegal', 'ip_host') + ":" + config.get('NotificationServerRegal', 'port'), config.get('NotificationServerNodeRed', 'ip_host') + ":" + config.get('NotificationServerNodeRed', 'port'), config.get('General', 'ca'))

        #Create a new led pwm control instance as a separate thread with the following parameters:
        #- The exit event variable to properly exit the thread upon exiting the application with a keyboard interrupt
        #- The data queue variable to receive control input from the notification server thread to control the LED
        #- The protocol&IP/Hostname of the ASN CSE ACME + colon + port of the ASN CSE ACME
        #- The ID of the just created application entity - this information will form part of the request identifier
        #- The user which will make additional requests to the ASN CSE ACME
        #- The version of oneM2M
        #- The configured LED devices - This is a list which contains one list per entry. Each LED entry list consists of the following: R pin, G pin, B pin
        #- The path to the Certificate Authority certificate which was used to sign the certificate of the ASN CSE AMCE
        ledPWM_thread = LedPwm(exit_event, data_queue, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('AE', 'app_id'), config.get('LED', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('LED', 'devices')), GPIO, config.get('General', 'ca'))
        #Create a new scale instance as a separate thread with the following parameters:
        #- The exit event variable to properly exit the thread upon exiting the application with a keyboard interrupt
        #- The protocol&IP/Hostname of the ASN CSE ACME + colon + port of the ASN CSE ACME
        #- The resourcename of the ASN CSE ACME
        #- The name of the application entity which was just be created
        #- The ID of the just created application entity - this information will form part of the request identifier
        #- The number of boxes on the Raspi (a box is a scale and a led)
        #- The user which will make send scale measurement data to the ASN CSE ACME
        #- The version of oneM2M
        #- The configured scale devices - This is a list which contains one list per scale entry. Each scale entry list consists of the following: DT pin, SCK pin, offset, ratio
        #- The path to the Certificate Authority certificate which was used to sign the certificate of the ASN CSE AMCE
        scale_thread = Scale(exit_event, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('Scale', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('Scale', 'devices')), config.get('General', 'ca'))

        #Start the led pwm control thread
        ledPWM_thread.start()
        #Start the scale measurement thread
        scale_thread.start()

    #When a keyboard interrupt occurs
    except KeyboardInterrupt:
        #Set that the led control and scale threads should end
        exit_event.set()
        #Cleanup the GPIO configuration
        GPIO.cleanup()
        #Wait until the led pwm control thread has finished
        ledPWM_thread.join()
        #Wait until the scale thread has finished
        scale_thread.join()

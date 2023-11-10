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
        print("hello")
        data_queue = queue.Queue()
        GPIO.setmode(GPIO.BCM)

        exit_event = threading.Event()

        config = configparser.ConfigParser()
        config.read('ae.ini')

        print("online check")
        CheckOnline(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_id'), config.get('AE', 'app_id'), config.get('CSE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('General', 'ca'))

        print("notification server")
        notificationServer_thread = NotificationServer(data_queue, int(config.get('NotificationServerRegal', 'port')), config.get('NotificationServerRegal', 'certfile'), config.get('NotificationServerRegal', 'keyfile'))
        notificationServer_thread.start()

        print("ae creation")
        AE_Creation(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('AE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('NotificationServerRegal', 'ip_host') + ":" + config.get('NotificationServerRegal', 'port'), config.get('NotificationServerNodeRed', 'ip_host') + ":" + config.get('NotificationServerNodeRed', 'port'), config.get('General', 'ca'))

        ledPWM_thread = LedPwm(exit_event, data_queue, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('AE', 'app_id'), config.get('LED', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('LED', 'devices')), GPIO, config.get('General', 'ca'))
        scale_thread = Scale(exit_event, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('Scale', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('Scale', 'devices')), config.get('General', 'ca'))

        ledPWM_thread.start()
        scale_thread.start()

    except KeyboardInterrupt:
        exit_event.set()

        GPIO.cleanup()

        ledPWM_thread.join()
        scale_thread.join()

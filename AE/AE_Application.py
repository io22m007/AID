import threading
import configparser
import queue
import json
import RPi.GPIO as GPIO
from CreateStructure import AE_Creation
from NotificationServerSmall import NotificationServer
from LedPwm import LedPwm
from Scale import Scale

if __name__ == "__main__":
    try:
        data_queue = queue.Queue()
        GPIO.setmode(GPIO.BCM)

        exit_event = threading.Event()

        config = configparser.ConfigParser()
        config.read('ae.ini')

        notificationServer_thread = NotificationServer(data_queue, int(config.get('NotificationServer', 'port')), config.get('NotificationServer', 'certfile'), config.get('NotificationServer', 'keyfile'))
        notificationServer_thread.start()

        AE_Creation(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('AE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('NotificationServer', 'ip_host') + ":" + config.get('NotificationServer', 'port'))

        ledPWM_thread = LedPwm(exit_event, data_queue, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('AE', 'app_id'), config.get('LED', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('LED', 'devices')), GPIO)
        scale_thread = Scale(exit_event, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('Scale', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('Scale', 'devices')))

        ledPWM_thread.start()
        scale_thread.start()

    except KeyboardInterrupt:
        exit_event.set()

        GPIO.cleanup()

        ledPWM_thread.join()
        scale_thread.join()

import threading
import configparser
import queue
import json
from CreateStructure import AE_Creation
from NotificationServerSmall import NotificationServer
from LedPwm import LedPwm

if __name__ == "__main__":
    data_queue = queue.Queue()

    config = configparser.ConfigParser()
    config.read('ae.ini')

    notificationServer_thread = NotificationServer(data_queue, int(config.get('NotificationServer', 'port')), config.get('NotificationServer', 'certfile'), config.get('NotificationServer', 'keyfile'))
    notificationServer_thread.start()

    ae_creation_thread = AE_Creation(config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port') + "/" + config.get('CSE', 'cse_rn'), config.get('AE', 'ae'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('AE', 'user'), config.get('General', 'releaseVersionIndicator'), config.get('NotificationServer', 'ip_host') + ":" + config.get('NotificationServer', 'port'))

    ledPWM_thread = LedPwm(data_queue, config.get('CSE', 'ip_host') + ":" + config.get('CSE', 'port'), config.get('AE', 'app_id'), int(config.get('AE', 'box_count')), config.get('LED', 'user'), config.get('General', 'releaseVersionIndicator'), json.loads(config.get('LED', 'pins')))
    ledPWM_thread.start()

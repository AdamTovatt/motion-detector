from network_credentials import NetworkCredentials
import time
import network

class WifiHelper:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def disconnect(self):
        self.wlan.active(False)

    def connect(self, credentials, max_wait_time):
        self.wlan.active(True)
        self.wlan.connect(credentials.ssid, credentials.password)

        max_wait = max_wait_time
        while max_wait > 0:
            status = self.wlan.status()
            if status != 1:
                return status
            max_wait -= 1
            print("waiting for connection...")
            time.sleep(1)
            
        return 0
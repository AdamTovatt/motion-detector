from machine import Pin
from network_credentials import NetworkCredentials
from on_board_led import OnBoardLed
from http_access_point import HttpAccessPoint
import time
import network

led = OnBoardLed()
led.off()

try:
    pir = Pin(20, Pin.IN, Pin.PULL_DOWN)

    credentials = NetworkCredentials.load()
    
    if credentials is None:
        print("Could not load credentials, will start access point")
        
        accessPoint = HttpAccessPoint("Samsung Smart Toilet", "needscleaning")
        accessPoint.start()
        
        time.sleep(0.5)
        led.blinkAlert(1)

        credentials = accessPoint.getNetworkCredentials()
        accessPoint.stop()

        print("Got credentials from access point")
        print(credentials)
        credentials.save()
    
    print("Have credentials now: ")
    print(credentials)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(credentials.ssid, credentials.password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() != 1:
            print("Connection event: ")
            print(wlan.status())
            if wlan.status() < 0:
                print("removing credentials")
                NetworkCredentials.remove()
            break
        max_wait -= 1
        print("waiting for connection...")
        time.sleep(1)         

    while True:
        if pir.value() == 1:
            led.on()
        else:
            led.off()
        time.sleep(0.1)
except Exception as exception:
    print(f"An error occurred: {exception}")
    led.blinkError()

led.off()
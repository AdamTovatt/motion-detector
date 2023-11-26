from machine import Pin
from network_credentials import NetworkCredentials
from wifi_helper import WifiHelper
from api_helper import ApiHelper
from on_board_led import OnBoardLed
from http_access_point import HttpAccessPoint
import time
import network
import lowpower

SENSOR_PIN = 20

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

    wifi = WifiHelper()
    connectionResult = wifi.connect(credentials, 10)

    if connectionResult < 0:
        led.blinkAlert(3)
        NetworkCredentials.remove()
        machine.reset()
        
    if connectionResult == 0:
        led.blinkAlert(2)
        machine.reset()
    
    if connectionResult == 3 or connectionResult == 2:
        led.blinkSuccess(2)

    # we should now be connected to the wifi
    
    api = ApiHelper()
    
    if not api.hasCredentials:
        api.createDetector()
    
    wifi.disconnect()
    
    print("Ready and waiting for motion")

    while True:
        if pir.value() == 0:
            print("waiting")
        else:
            print("motion")
        time.sleep(1)

    #while True:
    #    print("Going to dormant mode")
    #    lowpower.dormant_until_pin(SENSOR_PIN)
    #    print("Woke up")
    #    api.registerMotion()

    while True:
        if pir.value() == 1:
            led.on()
        else:
            led.off()
        time.sleep(0.1)
        
except Exception as exception:
    print(f"An error occurred: {exception}")
    raise
    led.blinkError()

led.off()
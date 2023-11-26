from machine import Pin
from network_credentials import NetworkCredentials
from wifi_helper import WifiHelper
from api_helper import ApiHelper
from on_board_led import OnBoardLed
from http_access_point import HttpAccessPoint
from motion_detector import MotionDetector
import time
import network
import lowpower

SENSOR_PIN = 20

led = OnBoardLed()
led.off()

led.blinkAlert(1)

try:
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
    
    motionDetector = MotionDetector(SENSOR_PIN)
 
    while True:
        motionDetector.waitForMotion(motion_interval = 120) # will not return more often than 120 seconds
        print("Going to register motion")
        api.registerMotion()
        print("Did register motion")

    #while True:
    #    print("Going to dormant mode")
    #    lowpower.dormant_until_pin(SENSOR_PIN)
    #    print("Woke up")
    #    api.registerMotion()
        
except Exception as exception:
    print(f"An error occurred: {exception}")
    led.blinkError(4)
    machine.reset()

led.off()
from machine import Pin
from on_board_led import OnBoardLed
from http_access_point import HttpAccessPoint
import time

led = OnBoardLed()
led.off()

try:
    pir = Pin(20, Pin.IN, Pin.PULL_DOWN)

    accessPoint = HttpAccessPoint("Samsung Smart Toilet", "needscleaning")
    accessPoint.start()
    
    time.sleep(0.5)
    led.blinkAlert(1)

    accessPoint.getNetworkCredentials()
    accessPoint.stop()

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
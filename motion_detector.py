from machine import Pin
from on_board_led import OnBoardLed
import time

class MotionDetector:
    def __init__(self, pinNumber):
        # Store the pin number as a field
        self.pin = Pin(pinNumber, Pin.IN, Pin.PULL_DOWN)
        self.last_motion_time = 0  # Variable to store the time of the last motion
        self.led = OnBoardLed()

    def waitForMotion(self, motion_interval=None):
        while True:
            time.sleep(1)
            if self.pin.value() == 1:
                self.led.on()
                current_time = time.time()
                # Check if enough time has passed since the last motion
                if motion_interval is None or (current_time - self.last_motion_time) >= motion_interval:
                    # Update the last motion time
                    self.last_motion_time = current_time
                    return
                else:
                    # If not enough time has passed, continue waiting
                    time.sleep(1)
            else:
                self.led.off()
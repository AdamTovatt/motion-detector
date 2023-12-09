from machine import Pin, ADC
from on_board_led import OnBoardLed
import time

class MotionDetector:
    def __init__(self, pinNumber):
        # Store the pin number as a field
        self.pin = ADC(Pin(pinNumber))
        self.last_motion_time = 0  # Variable to store the time of the last motion
        self.led = OnBoardLed()

    def waitForMotion(self, motion_interval=None):
        while True:
            time.sleep(0.2)
            motion = (self.pin.read_u16() > 1000)
            if motion:
                self.led.on()
                current_time = time.time()
                # Check if enough time has passed since the last motion
                if motion_interval is None or (current_time - self.last_motion_time) >= motion_interval:
                    # Update the last motion time
                    self.last_motion_time = current_time
                    return
            else:
                self.led.off()
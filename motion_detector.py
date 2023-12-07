from machine import Pin
import time

class MotionDetector:
    def __init__(self, pinNumber):
        # Store the pin number as a field
        self.pin = Pin(pinNumber, Pin.IN, Pin.PULL_DOWN)
        self.last_motion_time = 0  # Variable to store the time of the last motion

    def waitForMotion(self, motion_interval=None):
        while True:
            time.sleep(1)
            if self.pin.value() == 0:
            else:
                current_time = time.time()
                # Check if enough time has passed since the last motion
                if motion_interval is None or (current_time - self.last_motion_time) >= motion_interval:
                    # Update the last motion time
                    self.last_motion_time = current_time
                    return
                else:
                    # If not enough time has passed, continue waiting
                    time.sleep(1)
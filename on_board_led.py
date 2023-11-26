from machine import Pin
import time

class OnBoardLed:
    def __init__(self):
        # Set private field
        self.led = Pin("LED", Pin.OUT)

    def on(self):
        # Turn the LED on
        self.led.on()

    def off(self):
        # Turn the LED off
        self.led.off()

    def blinkError(self):
        while(True):
            self.on()  # Initial state is on
            time.sleep(1)  # Stay on for 1 second
            self.off()  # Turn off
            time.sleep(0.5)  # Stay off for 0.5 seconds

    def blinkSuccess(self, times):
        for _ in range(times):
            # Function to blink the LED in a success pattern
            for _ in range(3):
                self.on()  # Turn the LED on
                time.sleep(0.1)  # Stay on for 0.1 seconds
                self.off()  # Turn the LED off
                time.sleep(0.1)  # Stay off for 0.1 seconds

            time.sleep(0.5)  # Wait for a short duration between blinks
            
    def blinkAlert(self, times):
        for _ in range(times):
            # Function to blink the LED in an alert pattern
            for _ in range(4):
                self.on()  # Turn the LED on
                time.sleep(0.2)  # Stay on for 0.1 seconds
                self.off()  # Turn the LED off
                time.sleep(0.15)  # Stay off for 0.1 seconds

            time.sleep(0.5)  # Wait for a short duration between blinks


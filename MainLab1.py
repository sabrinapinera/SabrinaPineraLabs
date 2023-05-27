from machine import Pin
from Displays import *
from Buzzer import *
import time

class TrafficLight:
    def __init__(self, red, yellow, green):
        self.red = Pin(red, Pin.OUT)
        self.yellow = Pin(yellow, Pin.OUT)
        self.green = Pin(green, Pin.OUT)
        self.states = ["Red", "Yellow", "Green"]
        self.state = self.states[0]

    def next_state(self):
        self.state = self.states[(self.states.index(self.state) + 1) % len(self.states)]

    def set_state(self, state):
        if state not in self.states:
            raise ValueError("Invalid state.")
        self.state = state

    def update_lights(self):
        self.red.value(self.state == "Red")
        self.yellow.value(self.state == "Yellow")
        self.green.value(self.state == "Green")

class PedestrianButton:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.is_pressed = False

    def check_press(self):
        if not self.button.value():
            self.is_pressed = True
            return True
        return False

class Crosswalk:
    def __init__(self, light, button, buzzer):
        self.light = light
        self.button = button
        self.buzzer = Pin(buzzer, Pin.OUT)
        self._display = LCDDisplay(sda = 20, scl = 21, i2cid = 0)

    def run(self):
        while True:
            if self.button.check_press():
                self.light.set_state("Red")
                self._display.reset()
                self._display.showText("Walk")
                time.sleep(0.5)
                for i in range(10, 0, -1):
                    self._display.reset()
                    self._display.showNumber(i)
                    self.buzzer.on()
                    time.sleep(0.5)
                    self.buzzer.off()
                    time.sleep(0.5)
                self._display.showText("Don't Walk")
                self.button.is_pressed = False
            else:
                self.light.next_state()
                if self.light.state == "Green" or self.light.state == "Yellow":
                    self._display.showText("Don't Walk")

                else:
                    self._display.reset()
                    self._display.showText("Red Light")
                self.light.update_lights()
                time.sleep(1)  # adjust this as needed for the length of light cycle

# example of how to initialize and run
light = TrafficLight(red=0, yellow=3, green=7)
button = PedestrianButton(pin=17)
crosswalk = Crosswalk(light, button, buzzer=13)
crosswalk.run()
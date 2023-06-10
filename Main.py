from machine import Pin
from Displays import *
from Buzzer import *
from Sensors import *
from CompositeLights import *
import time

class TrafficLight:
    def __init__(self, red1, yellow1, green1, red2, yellow2, green2):
        self.red1 = Pin(red1, Pin.OUT)
        self.yellow1 = Pin(yellow1, Pin.OUT)
        self.green1 = Pin(green1, Pin.OUT)
        self.red2 = Pin(red2, Pin.OUT)
        self.yellow2 = Pin(yellow2, Pin.OUT)
        self.green2 = Pin(green2, Pin.OUT)
        self.states = ["Red", "Yellow", "Green"]
        self.state1 = self.states[0]
        self.state2 = self.states[0]

    def next_state(self):
        self.state1 = self.states[(self.states.index(self.state1) + 1) % len(self.states)]
        self.state2 = self.states[(self.states.index(self.state2) + 1) % len(self.states)]

    def set_state(self, state1, state2):
        if state1 not in self.states or state2 not in self.states:
            raise ValueError("Invalid state.")
        self.state1 = state1
        self.state2 = state2

    def update_lights(self):
        self.red1.value(self.state1 == "Red")
        self.yellow1.value(self.state1 == "Yellow")
        self.green1.value(self.state1 == "Green")
        self.red2.value(self.state2 == "Red")
        self.yellow2.value(self.state2 == "Yellow")
        self.green2.value(self.state2 == "Green")

class Motionsensor(DigitalSensor):

    def __init__(self, pin):
        super().__init__(pin, lowactive=False)

    def motionDetected(self):
        return self.tripped()

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
                sensor1 = Pin(sensor1_pin, Pin.IN).value()
                sensor2 = Pin(sensor2_pin, Pin.IN).value()

                if sensor1 and not sensor2:  # Sensor 1 active, Sensor 2 inactive
                    self.light.set_state("Green", "Red")
                elif not sensor1 and sensor2:  # Sensor 1 inactive, Sensor 2 active
                    self.light.set_state("Red", "Green")
                else:  # Both sensors active or inactive
                    self.light.next_state()

                if self.light.state1 == "Green" or self.light.state1 == "Yellow":
                    self._display.showText("Don't Walk")
                else:
                    self._display.reset()
                    self._display.showText("Red Light")

                self.light.update_lights()
                time.sleep(3) 

# Example of how to initialize and run
light = TrafficLight(red1=0, yellow1=3, green1=7, red2=10, yellow2=11, green2=12)
button = PedestrianButton(pin=17)
crosswalk = Crosswalk(light, button, buzzer=19)
sensor1_pin = 28
sensor2_pin = 27
crosswalk.run()
from Sensors import *
from CompositeLights import *

class Motionsensor(AnalogSensor):

    def __init__(self, pin):
        super().__init__(pin)

    def motionDetected(self):
        return self.tripped()

class PartyLight:

    def __init__(self, npin):
        self._pin = npin
        self._neo = NeoPixel(pin=self._pin, numleds=16, brightness=1)

    def on(self):
        self._neo.on()

    def off(self):
        self._neo.off()

    def disco(self):
        self._neo.run(2)
        
class MyPartyLight:

    def __init__(self, npin):
        self._pin = npin
        self._pix = Pixel(DimLight(0, "Red"),DimLight(1, "Green"), DimLight(2, "Blue"))

    def on(self):
        self._pix.on()

    def off(self):
        self._pix.off()

    def disco(self):
        self._pix.run()
        
        

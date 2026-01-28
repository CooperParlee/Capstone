"""
Filename: node.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: Class declaration for a generic pressure/temperature node.
"""

from time import time

class Node:
    id = -1
    temperature = -1
    pressure = -1
    flow_rate = -1

    temperature_units = "undefined"
    pressure_units = "undefined"

    def __init__(self, id):
        self.id = id
        self.startTime = time()
        self.timeSinceStart = 0
        self.inlet_attached = None
        self.outlet_attached = None

    def getTemperature(self):
        return self.temperature
    
    def getPressure(self):
        return self.pressure
    
    def getFlowRate(self):
        return self.flow_rate

    def setTemperature (self, temperature):
        self.temperature = temperature

    def setPressure (self, pressure):
        self.pressure = pressure

    def setFlowRate (self, flow_rate):
        self.flow_rate = flow_rate
    
    def setTemperatureUnits(self, units):
        self.temperature_units = units
    
    def setPressureUnits(self, units):
        self.pressure_units = units
    
    def update(self):
        self.timeSinceStart = time() - self.startTime

    def getTimeSinceStart(self):
        return self.timeSinceStart
        
    def attachInlet(self, inletDevice):
        """Sets the device that is attached to the inlet of the node.

        Args:
            inletDevice (Device): the new inlet device to the node.
        """
        self.inlet_attached = inletDevice
    
    def attachOutlet(self, outletDevice):
        """Sets the device that is attached to the outlet of the node.

        Args:
            outletDevice (Device): the new outlet device of the node.
        """
        self.outlet_attached = outletDevice
    
    def getOutletDevice(self):
        return self.outlet_attached

    def getInletDevice(self):
        return self.inlet_attached

    def getId(self):
        return self.id
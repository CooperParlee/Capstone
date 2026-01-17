"""
Filename: devicePump.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-12-2026
Description: Device which takes a control setpoint and changes the inlet and outlet pressures of the adjacent nodes accordingly.
"""

from src.devices.deviceInline import DeviceInline
from src.nodes.nodeManager import NodeManager
from warnings import warn

class DevicePump (DeviceInline):
    def __init__(self, manager : NodeManager, inlet=-1, outlet=-1):
        super().__init__(manager, inlet, outlet)
        self.setpoint = 0
        self.operatingPoint = 0 
        self.temperatureRise = 0

    def set(self, setpoint : float):
        if (setpoint > 1.0 or setpoint < 0):
            warn("Setpoint should be a floating point value between 0.0 and 1.0")
        self.setpoint = min(max(setpoint, 0), 1) # constrain the setpoint between 0 and 1

    
        

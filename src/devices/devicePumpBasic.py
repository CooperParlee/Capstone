"""
Filename: devicePump.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-12-2026
Description: Device which takes a control setpoint and changes the inlet and outlet pressures of the adjacent nodes accordingly.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.nodes.nodeManager import NodeManager

from src.devices import DeviceInline
from warnings import warn
from time import time


class DevicePumpBasic (DeviceInline):
    def __init__(self, manager : "NodeManager", inlet=-1, outlet=-1):
        super().__init__(manager, inlet, outlet)
        self.setpoint = 0
        self.operatingPoint = 0
        self.lastUpdate = -1
    def setPumpCurve(self, pumpCurve):
        """
        Provide a reference to a function for the pump curve; 
        """
        self.pumpCurve = pumpCurve

    def getPumpCurve(self):
        return self.pumpCurve

    def set(self, setpoint : float):
        if (setpoint > 1.0 or setpoint < 0):
            warn("Setpoint should be a floating point value between 0.0 and 1.0")
        self.setpoint = min(max(setpoint, 0), 1) # constrain the setpoint between 0 and 1

    def update (self):
        if (self.lastUpdate is None or self.lastUpdate == -1):
            self.lastUpdate = time()
        else:
            self.deltaT = time() - self.lastUpdate
"""
Filename: deviceParallel.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: File for the class declaration for a generic parallel device, such as a sensor.
"""
from src.nodes.node import Node
from src.devices import Device

class DeviceParallel (Device):
    attached_node: Node = -1

    def __init__ (self, attached_node : Node):
        if(not isinstance(attached_node, Node)):
            raise TypeError("Attached node must be of type Node.")
        self.attached_node = attached_node

    def get (self):
        self.temp = self.attached_node.getTemperature()
        self.pressure = self.attached_node.getPressure()
        self.flow = self.attached_node.getFlowRate()
        
    def getInlet(self):
        return self.attached_node


    
"""
Filename: deviceParallel.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: File for the class declaration for a generic parallel device, such as a sensor.
"""
from nodes.node import Node
from device import Device

class DeviceParallel (Device):
    attached_node: Node = -1

    def __init__ (self, attached_node : Node):
        if(type(attached_node) is not Node):
            raise TypeError("Attached node must be of type Node.")
        self.attached_node = attached_node

    
"""
Filename: deviceInline.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: File for the class declaration for a generic inline device.
"""
from warnings import warn
from src.devices.device import Device
from src.nodes.node import Node
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.nodes.nodeManager import NodeManager

class DeviceInline(Device):
    
    inlet_node: Node = -1
    outlet_node: Node = -1

    def computeDeltas(self):
        if (type(self.inlet_node) is Node and type(self.outlet_node) is Node):
            pass
        else:
            warn("Both inlet and outlet nodes must be defined to compute deltas.")
            
        # Always assume that flow rate will be the same into and out of a device
        self.outlet_node.setFlowRate(self.inlet_node.getFlowRate())
    
    def __init__(self, manager : 'NodeManager', inlet=-1, outlet=-1, k=0):
        super().__init__(k=k)
        # Initialize nodes if inlet or outlet go unspecified.
        if (inlet == -1):
            inlet = manager.addNode()
        if (outlet == -1):
            outlet = manager.addNode()
        self.inlet_node = inlet
        self.outlet_node = outlet
        
    def setResistanceCoefficient (self, k):
        self.k = k

    def getResistanceCoefficient (self):
        return self.k

    def getInlet(self):
        return self.inlet_node

    def getOutlet(self):
        return self.outlet_node
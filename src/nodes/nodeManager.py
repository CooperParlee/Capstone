"""
Filename: nodeManager.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: Class declaration for a program that manages the creation of nodes 
and the automatic assignment of node IDs.
"""
from src.nodes.node import Node
from src.devices.device import Device
from src.devices.devicePipe import DevicePipe
from warnings import warn

class NodeManager:
    # Default unit values
    default_temp = 'undefined'
    default_pressure = 'undefined'
    default_mflow = 'undefined'

    nodes: list[Node] = []

    def __init__(self, d_temp='K', d_press='kPa', d_mflow='kg/s'):
        self.default_temp = d_temp
        self.default_pressure = d_press
        self.default_mflow = d_mflow
        self.nodes = []

    def addNode(self, node=None):
        if(node is None):
            nodeCt = len(self.nodes)
            node = Node(nodeCt)

        if (not isinstance(node, Node)):
            raise TypeError("Specified argument node is not of type Node.")

        node.setPressureUnits(self.default_pressure)
        node.setTemperatureUnits(self.default_temp)
        if (self.nodes is None):
            self.nodes[0] = node
        
        self.nodes.append(node)

    def update(self):
        for node in self.nodes:
            node.update()

class ControlLoop:
    devices : list[Device] = []

    def __init__(self, density=999, viscosity=1.02E-3):
        self.density = density
        self.viscosity = viscosity
        self.k = -1
        self.devices = []
        self.pipes = []

    def addDevice (self, device):
        if (isinstance(device, Device)):
            if (self.devices is None):
                self.devices = [Device]
            else:
                self.devices.append(device)
            if (isinstance(device, DevicePipe)):
                self.pipes.append(device)
        else:
            warn(f"{device} is not an instance of Device; ignoring.")
    def addDevices(self, devices):
        for device in devices:
            self.addDevice(device)
    def getDevices(self):
        return self.devices

    def computeKFactor(self):
        """Compute the k factor for all inline devices in the control loop.

        Returns:
            float: the sum of all of the k factors.
        """
        k = 0

        for device in self.devices:
            k += device.getK()

        self.k = k

        return self.k

    def getKFactor (self):
        """Retrieves the precalculated k factor from memory or calculates it if the value is undetermined. More efficient than computeKFactor().

        Returns:
            float: minor loss K-factor.
        """
        if (self.k == -1):
            return self.computeKFactor()
        else: 
            return self.k
    def computeTotalMajor (self, Q):
        """Compute the total major loss for all pipes within the system

        Args:
            Q (float): Specified flow rate (m^3/s)

        Returns:
            float: Major friction loss for the whole system in meters.
        """
        headLoss = 0
        for pipe in self.pipes:
            headLoss += pipe.computeMajorLoss(Q)

        return headLoss
    

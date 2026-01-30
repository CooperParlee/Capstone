"""
Filename: nodeManager.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: Class declaration for a program that manages the creation of nodes 
and the automatic assignment of node IDs.
"""
from src.nodes.node import Node
from src.devices import Device
from src.devices import DevicePipe
from src.devices import DeviceInline
from src.devices import DeviceParallel
from src.devices import DevicePump

from warnings import warn
from scipy import optimize as opt

class NodeManager:
    # Default unit values
    default_temp = 'undefined'
    default_pressure = 'undefined'
    default_mflow = 'undefined'
    

    nodes: list[Node] = []

    def __init__(self, d_temp='K', d_press='kPa', d_mflow='kg/s', default_diameter=0.1):
        self.default_temp = d_temp
        self.default_pressure = d_press
        self.default_mflow = d_mflow
        self.default_diameter = default_diameter
        self.nodes = []
    def getDefaultDiameter (self):
        return self.default_diameter

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
        return node

    def getNodes(self):
        return self.nodes

    def getNode (self, id):
        if (self.nodes[id]):
            return self.nodes[id]
        else: 
            return None

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
        self.nodes = {}
        self.pumps = []

    def addNode(self, node):
        id = node.getId()

        if (id not in self.nodes):
            self.nodes[id] = node
        else:
            print(f"Oh shiii, {id} is already in my nodes")
    def addDevice (self, device):
        if (isinstance(device, Device)):
            if (self.devices is None):
                self.devices = [Device]          
            else:
                self.devices.append(device)
            
            if (isinstance(device, DevicePipe)):
                self.pipes.append(device)

            if (isinstance(device, DevicePump)):
                self.pumps.append(device)
            # Add nodes contained within the device to the existing list of nodes based upon id

            # Todo: validate and remove this
            # if (isinstance(device, DeviceInline)):
            #     self.addNode(device.getInlet())
            #     self.addNode(device.getOutlet())
            # if (isinstance(device, DeviceParallel)):
            #     self.addNode(device.getInlet())
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
        diameter = -1

        for device in self.devices:
            k += device.getK()
            if isinstance(device, DevicePipe):
                if (diameter == -1):
                    diameter = device.getDiameter()
                elif (diameter != -1 and diameter != device.getDiameter()):
                    warn("SIMULATION WARNING: The computeKFactor() method should only be used when the pipes are a constant " \
                    "diameter. When the diameter is not constant, the velocity term becomes incorrect! Please use " \
                    "computeTotalMinor() instead.")

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
    
    def computeTotalMinor (self, Q):
        """Compute the total minor losses for all pipes and fittings

        Args:
            Q (float): Specified flow rate (m^3/s)
        """
        headLoss = 0

        for device in self.devices:
            if isinstance(device, DeviceInline):
                headLoss += device.computeMinorLoss(Q)
            else:
                print(f"device was not an inline device {type(device)}")
        
        return headLoss
    
    def totalPumpCurve (self, q):
        return (sum(pump.getCurve()(q) for pump in self.pumps)
        - self.computeTotalMinor(q) - self.computeTotalMajor(q))

    def computeOpPoint (self): 
        soln = opt.root_scalar(lambda q: self.totalPumpCurve(q) - self.computeTotalMinor(q) - self.computeTotalMajor(q), 
        method="brentq", bracket=[0, 15/60])
        return soln.root, self.totalPumpCurve(soln.root)
        
        

"""
Filename: devicePipe.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: Class declaration for a pipe.
"""
from src.devices import DeviceInline
from src.nodes.node import Node
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.nodes.nodeManager import NodeManager

from math import pi
from numpy import log10

class DevicePipe(DeviceInline):
    diameter: float = -1.0
    length: float = -1.0
    roughness: float = 0.0 

    def __init__ (self, manager : 'NodeManager', inlet_node : Node, outlet_node : Node, roughness=0, length=0, diameter=0, density=999, viscosity=1.02E-3):
        """Initialize a pipe object with given inlet and outlet nodes and optional roughness, length and diameter values.

        Args:
            manager (NodeManager): NodeManager object to check/add nodes to.
            inlet_node (Node): Inlet node for the system
            outlet_node (Node): Outlet node for the system
            roughness (int, optional): Pipe roughness (m). Defaults to 0.
            length (int, optional): Total pipe length (m). Defaults to 0.
            diameter (int, optional): Pipe diameter (m). Defaults to 0.
            density (float, optional): Density of the contained media (kg/m^3). Defaults to 999.
            viscosity (float, optional): Viscosity of the contained media (m^2/s). Defaults to 1.02E-3.
        """
        self.roughness = roughness
        self.length = length
        self.diameter = diameter
        self.density = density
        self.viscosity = viscosity
        super().__init__(manager, inlet_node, outlet_node, diameter=diameter)

    def setRoughness(self, roughness):
        """Set the pipe roughness.

        Args:
            roughness (float): Pipe roughness (m)
        """
        self.roughness = roughness

    def setLength (self, length):
        """Set the pipe length in meters.

        Args:
            length (float): Total pipe length (m)
        """
        self.length = length

    def setDiameter (self, diameter):
        """Set the pipe diameter in meters.

        Args:
            diameter (float): Total pipe diameter (m)
        """
        self.diameter = diameter

    def setK(self, k):
        """Add some additional minor losses via a k value for things like fittings that may be on the pipe. Don't do it with another device.

        Args:
            k (float): Minor loss k value for fittings (unitless)
        """
        self.k = k

    def computeDeltas(self):
        super().computeDeltas()

    def computeMajorLoss (self, Q):
        """Compute the major friction loss from pipe roughness for a given flow rate, Q (in m^3/s). Limitation is that this only works for turbulent
        flow as it uses the Swamee-Jain equation. Technically, it will work for laminar flow, but it will be very conservative.

        Args:
            Q (float): Specified flow rate (m^3/s).

        Returns:
            float: Major friction loss for the pipe in meters.
        """
        g = 9.81 # m/s^2
        A = self.diameter**2 * pi / 4
        v = Q/A # velocity (m/s)
        Re = self.density * v * self.diameter / self.viscosity

        # Compute friction factor in that pipe (Swamee-Jain)

        print(f"Diameter: {self.diameter} Re: {Re}")
        f = 0.25 / (log10(self.roughness/(3.7*self.diameter) + 5.74/Re**0.9))**2

        # Darcy-Weisbach
        h_friction = f * (self.length/self.diameter) * (v**2/(2*g))

        return h_friction

    def getDiameter(self):
        return self.diameter
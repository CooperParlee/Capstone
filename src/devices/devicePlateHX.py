"""
Filename: devicePlateHX.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-30-2026
Description: File declaration for a basic heat exchanger.
"""

from src.devices import DeviceInline
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.nodes.nodeManager import NodeManager

class DevicePlateHX(DeviceInline):
    def __init__(self, manager : 'NodeManager', inlet=-1, outlet=-1, k=0, diameter=-1, verbose=False):
        super().__init__(manager=manager, inlet=inlet, outlet=outlet, k=k, diameter=diameter, verbose=verbose)
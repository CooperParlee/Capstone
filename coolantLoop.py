"""
Filename: coolantLoop.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-17-2026
Description: Unit test that creates a basic cooling water loop with two heat exchangers, such as the CFW system on TSSOM.
"""

from src.nodes.nodeManager import NodeManager, ControlLoop
from src.devices import DevicePumpBasic
from src.devices import DevicePipe
from src.devices import DeviceInline

import numpy as np
import matplotlib.pyplot as plt

# Default characteristics
# 8-inch pipe
dia = 0.2027 # (m)
rough = 4.6E-5 # (m)
density = 999 # (kg/m^3)
viscosity = 1.02E-3 # (m^2/s)

#Initialize the node manager
mgr = NodeManager(default_diameter = dia)

# Initialize a control loop w/ default unit settings
controlLoop = ControlLoop(density=density, viscosity=viscosity)

# Initialize pump, let it initialize its own nodes
pump = DevicePumpBasic(mgr)

hxcooler = DeviceInline(mgr, k=0.1)
hxheater = DeviceInline(mgr, k=0.5)

# Create a pipe out of the pump and into the heat exchanger
p1 = DevicePipe(mgr, pump.getOutlet(), hxcooler.getInlet(), roughness=rough, length=5, diameter=dia,
                viscosity = viscosity, density = density)
# Now do the same with the cooler into the heater hx
p2 = DevicePipe(mgr, hxcooler.getOutlet(), hxheater.getInlet(), roughness=rough, length=10, diameter=dia,
                viscosity = viscosity, density = density)
# Finally, pipe from heater to pump suction
p3 = DevicePipe(mgr, hxheater.getOutlet(), pump.getInlet(), roughness=rough, length=5, diameter=dia,
                viscosity = viscosity, density = density)

controlLoop.addDevices([pump, hxcooler, hxheater, p1, p2, p3])

k = controlLoop.getKFactor()

# Flow rate in m^3/min
q = np.linspace(0, 12, 20) 
mjr = []
mnr = []

for _q in q:
    mjr.append(controlLoop.computeTotalMajor(_q/60))
    mnr.append(controlLoop.computeTotalMinor(_q/60))

mjr = np.array(mjr)
mnr = np.array(mnr)

print(k)

plt.plot(q, mjr, label="Major Losses", color="blue")
plt.plot(q, mnr, label="Minor Losses", color="red")
plt.plot(q, mjr + mnr, label="Total", color="green")
plt.title("Heat Exchanger System Operating Point")
plt.xlabel(r"Flow Rate ($m^3min^{-1}$)")
plt.ylabel("Head Loss (m)")
plt.legend()
plt.show()
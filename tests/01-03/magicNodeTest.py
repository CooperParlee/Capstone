"""
Filename: deviceParallel.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-03-2026
Description: Basic test of the engine using the fabled magic node.
"""

from src.nodes.nodeManager import NodeManager
from src.nodes.magicNode import MagicNode
from src.modBus.modbusManager import ModbusManager
from src.devices.deviceTempSensor import DeviceTempSensor

from time import sleep

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading
import asyncio

#Initialize the node manager
nodeManager = NodeManager()
# Create a special node and add it to the manager
magicNode = MagicNode(0)
nodeManager.addNode(magicNode)

tempSensor = DeviceTempSensor(magicNode)

modbusManager = ModbusManager()
modbusManager.addSensor(tempSensor, 400)

# Set up a moving dataframe with a maximum length of 150
x_data = deque(maxlen=150)
y_data = deque(maxlen=150)

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1, 1)
ax.set_xlim(0, 10)

# Create an update function. There might be better names for this.
def update():

    while (True):
        # Set it to programmatically update the node manager (which, in turn, updates all of the nodes)
        nodeManager.update()
        
        sleep(0.05)

# Create a function which regenerates and returns the graph view with the new data
def updateGraph(frame):
    timeSinceStart = magicNode.getTimeSinceStart()

    x_data.append(timeSinceStart)
    y_data.append(magicNode.getTemperature())

    line.set_data(list(x_data), list(y_data))

    # If it's been more than 10 seconds since the start, move the viewport x-range
    if(timeSinceStart > 10):
        ax.set_xlim(timeSinceStart - 10, timeSinceStart)
    return line,

# Start a new thread for the simulation, daemon means long-running b.g. process???
simulationThread = threading.Thread(target=update, daemon=True)
simulationThread.start()

# Start another thread for the modbus server
def start_server():
    asyncio.run(modbusManager.run_server())

serverThread = threading.Thread(target=start_server)
serverThread.start()

# This handles the actual animation of the graph using the updateGraph function and the original figure
# Do not cache the axes (blit) because we regenerate them when the viewport moves
pltAnimation = animation.FuncAnimation(fig, updateGraph, interval=100, blit=False)

plt.show(block=True)



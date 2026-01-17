"""
Filename: modbusServHost.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-01-2026
Description: Hosts a Modbus server which can be asynchronously written to by other Python programs.
"""

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext
from pymodbus.datastore import ModbusSequentialDataBlock
import asyncio
import random

async def update_sensor_data (context):
    # Set the *C min and max temps for the virtual sensor.
    minTemp = 100
    maxTemp = 150

    temperature = (maxTemp + minTemp) / 2 # initial temperature

    # Absolute integer magnitude of temperature variation.
    variation = int(10)

    #TODO: add temperature scaling

    while True:
        # Vary the temperature a little bit.
        temperature = temperature + random.randint(-variation, variation)

        # Constrain the randomized temperature value to be within the acceptable ranges.
        temperature = min(temperature, maxTemp)
        temperature = max(temperature, minTemp)

        print(temperature)
        # Get the datastore, set as ID 1
        server_context = context[1]

        # Update input register (3) at address 100 with the temperature
        server_context.setValues(3, 300, [int(temperature)])

        await asyncio.sleep(2)

async def run_server():
    # Initialize the datastore for the 4 i/o classes
    store = ModbusDeviceContext(
        di = ModbusSequentialDataBlock(100, [False]*100), # discrete inputs (100) - read only
        co = ModbusSequentialDataBlock(200, [False]*100), # coils (100) - read/write bits
        hr = ModbusSequentialDataBlock(300, [0]*100), # holding registers (read/write 16-bits)
        ir = ModbusSequentialDataBlock(400, [0]*100), # input registers (100) - read only 16-bit
    )

    context = ModbusServerContext(devices=store, single=True) # Create context containing one store as single context

    asyncio.create_task(update_sensor_data(context))

    await StartAsyncTcpServer(context=context, address=("127.0.0.1", 5020))

asyncio.run(run_server())
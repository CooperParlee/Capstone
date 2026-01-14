"""
Filename: modbusManager.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-14-2026
Description: Manager for modbus addresses
"""

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusDeviceContext
from pymodbus.datastore import ModbusSequentialDataBlock
import asyncio

from src.devices.device import Device

class ModbusManager:
    async def updateSensors(self, context : ModbusServerContext):
        server_context = context[1]
        while True:
            await asyncio.sleep(0.5)
            for sensor in self.ids:
                for address in sensor.getAddresses():
                    value = sensor.get()
                    print(f"Updating sensor on address {address} to {value}")
                    server_context.setValues(4, address, value)


    async def run_server(self, address="127.0.0.1", port = 5020):
        # Initialize the datastore for the 4 i/o classes
        self.store = ModbusDeviceContext(
            di = ModbusSequentialDataBlock(100, [False]*100), # discrete inputs (100) - read only
            co = ModbusSequentialDataBlock(200, [False]*100), # coils (100) - read/write bits
            hr = ModbusSequentialDataBlock(300, [0]*100), # holding registers (read/write 16-bits)
            ir = ModbusSequentialDataBlock(400, [0]*100), # input registers (100) - read only 16-bit
        )

        context = ModbusServerContext(devices=self.store, single=True) # Create context containing one store as single context

        asyncio.create_task(self.updateSensors(context))

        await StartAsyncTcpServer(context=context, address=(address, port))

    def __init__(self):
        self.ids = {}
        asyncio.run(self.runserver)

    def addSensor(self, device: Device, id=-1):
        if (id == -1):
            # Find next empty id
            for i in range(400, 499):
                if i not in self.ids:
                    id = i
                    break
            if (id == -1): 
                yield LookupError("Unable to find an empty sensor id in the specified range")
        self.ids[id] = device
        device.addAddress(id)
        


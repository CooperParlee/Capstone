"""
Filename: deviceSensor.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-14-2026
Description: A basic class for reading temperature sensor values
"""
from src.devices import DeviceParallel

class DeviceTempSensor (DeviceParallel):
    def get(self):
        super().get()
        return self.temp

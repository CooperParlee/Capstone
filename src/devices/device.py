"""
Filename: device.py
Author: Cooper Parlee <cooper.parlee@mma.edu>
Date: 01-02-2026
Description: File for the class declaration for a generic device.
"""

from warnings import warn

class Device:
    addresses = []

    def __init__(self, k=0, verbose=False):
        self.k = k
        self.verbose = verbose

    def getK(self):
        return self.k

    def setK(self, k):
        self.k = k

    def getAddresses(self):
        return self.addresses
    
    def addAddress(self, address):
        if (type(address) is not int):
            raise TypeError("Address must be of type integer.")

        self.addresses.append(address)

    def removeAddress(self, address):
        if (address in self.addresses):
            self.addresses.remove(address)
        else:
            warn(f"Address {address} was not found and cannot be removed.")

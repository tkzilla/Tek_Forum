#-------------------------------------------------------------------------------
# Name:  Save Screenshot (Hard Copy) to PC for 5 Series MSO Oscilloscopes
#
# Purpose:  This example demonstrates how to save a screen shot (hard copy) image
#  from a 5 Series MSO oscilloscope to the PC.
#
# Development Environment: Python 3.6, PyVisa 1.8, NI-VISA 2017, Windows 10 x64
#
# Compatible Instruments: 5 Series MSO, MSO54, MSO56, MSO58
#
# Compatible Interfaces:  USB, Ethernet
#
# Tektronix provides the following example "AS IS" with no support or warranty.
#
#-------------------------------------------------------------------------------

from datetime import datetime # std library
import time # std library
import visa # https://pyvisa.readthedocs.io/

# Replace string with your instrument's VISA Resource Address
visaRsrcAddr = "MSO58"

rm = visa.ResourceManager()
scope = rm.open_resource(visaRsrcAddr)
print(scope.query('*IDN?'))  # Print instrument id to console window

# Save image to instrument's local disk
scope.write('SAVE:IMAGe \"C:/Temp.png\"')

# Generate a filename based on the current Date & Time
dt = datetime.now()
fileName = dt.strftime("MSO5_%Y%m%d_%H%M%S.png")

# Wait for instrument to finish writing image to disk
scope.query('*OPC?')

# Read image file from instrument
scope.write('FILESystem:READFile \"C:/Temp.png\"')
imgData = scope.read_raw(1024*1024)

# Save image data to local disk
file = open(fileName, "wb")
file.write(imgData)
file.close()

# Image data has been transferred to PC and saved. Delete image file from instrument's hard disk.
scope.write('FILESystem:DELEte \"C:/Temp.png\"')

scope.close()
rm.close()

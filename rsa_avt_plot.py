"""
"""
Date: 9/29/2014
Tested on a 64-bit Windows 7 computer
using NI-VISA 5.4 with Python 2.7.6, PyVISA 1.5, NumPy 1.8.1, and MatPlotLib 1.3.1
Tested on RSA5126B
Program: Amplitude vs Time Trace Transfer
This program transfers the Amplitude vs Time trace from the RSA to the computer
and plots the results. Test signal is a 1 MHz 80% modulation depth AM signal centered at 1 GHz.
"""

import visa
import numpy as np
import matplotlib.pyplot as plt

#establish communication with RSA
rsa = visa.instrument('TCPIP0::RSA5126BB040364.home::inst0::INSTR')
#rm = visa.ResourceManager()
#rsa = rm.open_resource('TCPIP0::RSA5126BB040364.home::inst0::INSTR')
print(rsa.ask('*idn?'))

#reset the instrument
rsa.write('*rst')
#stop acquisitions while setting up instrument
rsa.write('abort')
#open spectrum, time overview, and amplitude vs time displays
rsa.write('display:general:measview:new spectrum')
rsa.write('display:general:measview:new toverview')
rsa.write('display:general:measview:new avtime')

#configure acquisition parameters
meas_freq = 1.5e9
meas_bandwidth = 20e6
time_scale = 10e-6
time_offset = 0
trig_level = -12

#configure amplitude vs time measurement
rsa.write('spectrum:frequency:center {0}'.format(meas_freq))
rsa.write('spectrum:frequency:span {0}'.format(meas_bandwidth))
rsa.write('sense:avtime:span {0}'.format(meas_bandwidth))
rsa.write('sense:analysis:length {0}'.format(time_scale))
rsa.write('sense:analysis:start {0}'.format(time_offset))

#configure power level trigger
rsa.write('trigger:event:input:type power')
rsa.write('trigger:event:input:level {0}'.format(trig_level))
rsa.write('initiate:continuous off')
rsa.write('trigger:status on')

#start acquisition
rsa.write('initiate:immediate')
rsa.ask('*opc?')

#get raw amplitude vs time data from RSA
rsa.write('fetch:spectrum:trace1?')
rawdata = rsa.read_raw()

"""
The raw data begins with a header that contains information that is useful for transferring the waveform.
We will need to read it and then remove it from the actual waveform data.
The first character in the header is a '#' character.
The second character contains the number of digits in the number of data points in the record
(for example if the number of data points was 100, this character would be 3).
The next number is the number of data points whose length is specified by the second character
A full example: If I had a 1000 point-long waveform, the header would be '#41000'
"""

#determine the length of the header by adding 2 to the number of digits in the waveform length
#(one for the # character and one for the character being read)
headerlength = 2 + int(rawdata[1])
#get the number of bytes from the header
bytes = int(rawdata[2:headerlength])
#since the trace data is 4 bytes per point...
numberofpoints = bytes/4
#strip out the header by saving the data from the end of the header to the index before end of the waveform
#the last data point is excluded because it is a newline character
rawdata = rawdata[headerlength:-1]

#get the minimum and maximum time in the measurement from the RSA
time_max = float(rsa.ask('display:avtime:x:scale:full?'))
time_min = float(rsa.ask('display:avtime:x:scale:offset?'))

#generate the time vector for plotting
increment = (time_max-time_min)/numberofpoints
time = np.arange(time_min, (time_max-increment), increment)
#have NumPy interpret the raw binary data as 32-bit floating point numbers
data = np.fromstring(rawdata, dtype = np.float32)


#plot the data
plt.plot(time,data)
plt.suptitle('Amplitude vs Time')
plt.ylabel('Amplitude (dBm)')
plt.xlabel('Time (s)')
plt.xlim(time_min,time_max)
plt.show()

rsa.close()

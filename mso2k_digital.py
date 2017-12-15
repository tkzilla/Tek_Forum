##############################################################################################
##  
##  Date: July 2nd 2015
##  Details: This is a Python  example for digital channel data being queried on the MSO2000/B scopes         
## 
##############################################################################################

import visa # http://pyvisa.sourceforge.net/  version 1.6
import numpy # http://www.numpy.org/      version 1.6.1
import pylab #plotting tool


print 'Starting program'

rm = visa.ResourceManager()

#myscope = rm.open_resource('TCPIP::192.168.1.50::INSTR')  #insert IP address of device
myscope = rm.open_resource('USB::0x0699::0x03A4::C000001::INSTR') #use this for USB devices

#identify connected scope
IDN = myscope.ask('*IDN?')
print 'Successfully connected to: ', IDN

#check error status register
ESR = myscope.ask('*ESR?')
print 'Error status register: ', ESR

ALLEV = myscope.ask('ALLEV?')
print 'All Event details: ', ALLEV

myscope.write('data:encdg SRP')
print 'Encoding type: ', myscope.ask('data:encdg?')

myscope.write('DATA:WIDTH 1')
print 'Data width: ', myscope.ask('DATA:WIDTH?')

myscope.write('wfmoutpre:byt_nr 1')
print 'wfm preamble btye size: ', myscope.ask('wfmoutpre:byt_nr?')

myscope.write('data:start 1')
print 'Start of data: ', myscope.ask('data:start?')

myscope.write('data:stop 200000')
print 'Stop of data: ', myscope.ask('data:stop?')

myscope.write('DATa:RESOlution FULL')
print 'Data resolution setup: ', myscope.ask('DATa:RESOlution?')

myscope.write('DATa:COMP SINGULAR_YT')
print 'Data composition type: ', myscope.ask('DATa:COMP?')

xincr = float(myscope.ask('WFMPRE:XINCR?'))


digital_channel = range(16)
d0 = []
d1 = []
d2 = []
d3 = []
d4 = []
d5 = []
d6 = []
d7 = []
d8 = []
d9 = []
d10 = []
d11 = []
d12 = []
d13 = []
d14 = []
d15 = []

#loop to grab all digital channel data
for i in digital_channel:

    #selected digital channel
    myscope.write('data:source D' + str(digital_channel[i]))
    print 'Transmitting Data From Source: ', myscope.ask('data:source?')

    #query the digital channel
    myscope.write('curve?')
    data = myscope.read_raw()

    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    digital_wave = data[headerlen:-1]

    temp8bits = numpy.fromstring(digital_wave, dtype = 'u1')

    extracted8bit = numpy.unpackbits(temp8bits.reshape((temp8bits.shape[0],1)), axis=1)

    exec 'd%s = extracted8bit[:,7]' %digital_channel[i]

Time = numpy.arange(0, xincr * len(d0), xincr)

pylab.plot(Time, d0+15, label='D0')
pylab.plot(Time, d1+14, label='D1')
pylab.plot(Time, d2+13, label='D2')
pylab.plot(Time, d3+12, label='D3')
pylab.plot(Time, d4+11, label='D4')
pylab.plot(Time, d5+10, label='D5')
pylab.plot(Time, d6+9, label='D6')
pylab.plot(Time, d7+8, label='D7')
pylab.plot(Time, d8+7, label='D8')
pylab.plot(Time, d9+6, label='D9')
pylab.plot(Time, d10+5, label='D10')
pylab.plot(Time, d11+4, label='D11')
pylab.plot(Time, d12+3, label='D12')
pylab.plot(Time, d13+2, label='D13')
pylab.plot(Time, d14+1, label='D14')
pylab.plot(Time, d15+0, label='D15')

pylab.ylim(-1,17)
pylab.legend()
pylab.show()


##############################################################################################
##
##  Date: July 28th 2015
##  Details: This is a Python  example for digital channel data being queried on the MSO5000/B
##
##############################################################################################


#using python 2.7
import visa # http://pyvisa.sourceforge.net/ v1.6
import numpy # http://www.numpy.org/ v1.6.1
import pylab


rm = visa.ResourceManager()
#myscope = rm.open_resource('TCPIP::192.168.1.100::INSTR')
myscope = rm.open_resource('USB::0x0699::0x0507::C000001::INSTR')



#myscope.write('*cls')
IDN = myscope.ask('*IDN?')
print 'Successfully connected to: ', IDN


myscope.write('data:source digitalall')

myscope.write('WFMOutpre:ENCdg BINary')
# set data start
myscope.write('data:start 1')
# set data stop
myscope.write('data:stop 100000')
#check encoding
wfmoutpreamble = myscope.ask('WFMOutpre?')
wfmoutpreamble_split = wfmoutpreamble.split(';')
BYT_NR = wfmoutpreamble_split[0] # this can be 1,2,4, or 8 for the number of bytes per data point. 1 or 2 for waveform channel data, 4 is good for math data, 8 bytes are good for pixal maps
print 'BYT_NR: ', BYT_NR
BIT_Nr = wfmoutpreamble_split[1]
print 'BIT_NR: ', BIT_Nr
ENCDG = wfmoutpreamble_split[2]
print 'ENCODING: ', ENCDG
BN_FMT = wfmoutpreamble_split[3]    # is this RI, RP, FP formating?
print 'BN_FMT: ', BN_FMT
BYT_ORDER_MSB_OR_LSB = wfmoutpreamble_split[4]  #Is this MSB or LSB first
print 'BYT FORMAT: ', BYT_ORDER_MSB_OR_LSB

myscope.write('DATA:ENCdg SRP')

#grab the x axis details
xincr = float(myscope.ask('WFMPRE:XINCR?'))

#query the data for the digital channels
myscope.write('CURVE?')
data = myscope.read_raw()

headerlen = 2 + int(data[1])
header = data[:headerlen]
digital_wave = data[headerlen:-1]

#d = numpy.zeros((len(digital_wave),16))

temp8bits = numpy.fromstring(digital_wave, dtype = 'u1')

extracted8bit = numpy.unpackbits(temp8bits.reshape((temp8bits.shape[0]/2,2)), axis=1)

#for n in range(16):
d0 = extracted8bit[:,7]
d1 = extracted8bit[:,6]
d2 = extracted8bit[:,5]
d3 = extracted8bit[:,4]
d4 = extracted8bit[:,3]
d5 = extracted8bit[:,2]
d6 = extracted8bit[:,1]
d7 = extracted8bit[:,0]
d8 = extracted8bit[:,15]
d9 = extracted8bit[:,14]
d10 = extracted8bit[:,13]
d11 = extracted8bit[:,12]
d12 = extracted8bit[:,11]
d13 = extracted8bit[:,10]
d14 = extracted8bit[:,9]
d15 = extracted8bit[:,8]

for n in range(len(d15)):
    if d15[n] == 1:
        d15[n] = 0
    else:
        d15[n] = 1


Time = numpy.arange(0, xincr * len(d8), xincr)

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


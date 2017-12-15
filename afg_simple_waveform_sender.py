'''
Create waveform and send to AFG3000

This script crates a 5mS waveform that starts with a 1uS low value, sends
a 1.2mS high pulse, then for the remained of the 5ms will send a squarewave
with a set frequency and duty cycle.  The waveform is then sent to and AFG 3000,
and set to play in burst mode, with and internal timmer triggering one cycle
of the waveform every 200mS

python 2.7 (http://www.python.org/)
pyvisa 1.3 (http://pypi.python.org/pypi/PyVISA/1.3)
'''
#Enter your values here
frequency = 10e3
DutyCycle = 40                      # in percent

#Get the this from The OpenChoice Instrument Manager
instrumentdescriptor = 'USB0::0x0699::0x0345::CU000007::INSTR'

numpoint = int(125e3)               #Change this if needed, but should be OK
samplerate = 25e6
timeacq = numpoint / samplerate     # Set this so you get 5mS

#import needed librarys
import visa
from struct import pack
print 'Creating Waveform'
#Create the waveform
waveform = []

for j in range(numpoint):
    index = j * 1/float(samplerate)
    if -1 < index <= 1e-6:  #sets the initial dellay at 0
        waveform.append(0)
    elif 1e-6 < index <= 1.201e-3: # set the first 1.2mS pulse
        waveform.append(1)
    else:
        break #stop here once the 1.2mS time has been created

# Build one segment of the square wave, space first, on second
samplesperwave = samplerate / frequency
on_samples = DutyCycle / 100.0 * samplesperwave
off_samples = samplesperwave - on_samples
onewave = []
for j in range(int(off_samples)):
    onewave.append(0)
for j in range(int(on_samples)):
    onewave.append(1)

#Cycle the one wave until total time on is at 5mS
while len(waveform) * 1/float(samplerate) < 5e-3:
    for j in onewave:
        if len(waveform) * 1/float(samplerate) < 5e-3:
            #makes sure that we stop at 5mS, even if not even dividied
            waveform.append(j)

#Write the waveform to a text file 'testwave.txt'
fid = open('testwave.txt', 'w')
for j in waveform:
    fid.write(str(j) + '\n')
fid.close()

#Scale waveform magnitutde to raw value max for AFG
for j in range(len(waveform)):
    waveform[j] = waveform[j] * 16382

#create the binary block header.  Values will be converted to uint
header = '#' + str(len(str(numpoint * 2))) + str(numpoint * 2)

#create a binary string from the waveform values to transfer
binwavefrom = pack('>'+'h'*len(waveform), *waveform)

print 'Compelted Createing Waveform'
print 'Sending waveform to AFG'


#Next sending to the AFG
AFG = visa.instrument(instrumentdescriptor)
print AFG.ask('*IDN?')
#reset and clear the AFG status
AFG.write('*rst')
AFG.write('*cls')

#setup the waveform, lenght = number of points for waveform defined above
AFG.write('trace:define ememory, ' + str(numpoint))
#transfer waveform to afg
AFG.write('trace ememory, '+ header + binwavefrom)

#configure the channel to play arbitrary waveform, burst mode, .2ms timer
#on trigger, 0 - 5V output, 1 cycle of waveform per occurance.
AFG.write('source1:function ememory')
AFG.write('source1:frequency 200')
AFG.write('source1:burst:mode trig')
AFG.write('source1:burst:ncycles 1')
AFG.write('source1:burst:state on')
AFG.write('trigger:sequence:timer 0.2')
AFG.write('source1:voltage:high 5')
AFG.write('source1:voltage:low 0')

#finnaly, turn the output on
AFG.write('output1 on')

#freeze the output window until key is pressed
raw_input('Press any key to Exit')

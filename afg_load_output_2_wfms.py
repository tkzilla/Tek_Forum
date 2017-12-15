# Date: 6/17/14
# Tested on a 64-bit Windows 7 computer
# using TekVISA 4.0.0 and Python 2.7.6 with PyVISA 1.5
# Program: AFG3000 Dual Channel Arb Waveform Load and Output
# This program configures amplitude and frequency for both channels,
# loads two separate waveforms into the AFG, and outputs them
# on Channel 1 and Channel 2, respectively.

import visa
instrument = visa.instrument('USB::0x0699::0x0345::C010255::INSTR')

#Waveform name includes number of points for the sake of clarity
#Note the inclusion of double-quotes within the string
wfm1name = '\"Cardiac_10k.tfw\"'
wfm2name = '\"Sinc_10k.tfw\"'

ID = instrument.ask('*IDN?')    #Query instrument identifier.
print(ID)                       #Display instrument identifier
instrument.write('*RST')        #Reset the instrument

# Set up amplitude and frequency
instrument.write('source1:frequency 5e5')                         #Set channel 1 to output 500 kHz
instrument.write('source1:voltage:level:amplitude 2')   #Set channel 1 amplitude to 2Vpp

instrument.write('source2:frequency 1e6')                         #Set channel 2 to output 1 MHz
instrument.write('source2:voltage:level:low -1')        #Set channel 2 high level at 1V
instrument.write('source2:voltage:level:high 1')        #Set channel 2 low level at -1V

# Load TFW files into channels 1 and 2
# Since there is only one memory location into which a user can load a
# waveform, it is necessary to copy each waveform into a separate memory
# location in order to avoid overwriting the first waveform with the second
instrument.write('mmemory:load:trace ememory, {0}'.format(wfm1name))    #Load the waveform file into ememory
instrument.write('data:copy user1, ememory')                #Copy the waveform from ememory into User1
instrument.write('source1:function user1')                  #Assign the waveform in User1 to Channel 1

instrument.write('mmemory:load:trace ememory, {0}'.format(wfm2name))    #Load the waveform file into ememory
instrument.write('data:copy user2, ememory')                #Copy the waveform from ememory into User2
instrument.write('source2:function user2')                  #Assign the waveform in User2 to Channel 2

instrument.write('output1:state on')          #Turn on Channel 1 output
instrument.write('output2:state on')          #Turn on Channel 2 output

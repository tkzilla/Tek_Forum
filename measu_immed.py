#-------------------------------------------------------------------------------
#  Using MEASU:IMM to get 5 frequency measurements on channel 1
#
#  single-shot with *OPC sync guarantees that each measurement is on a new
#  acquisition
#
# python 2.7 (http://www.python.org/)
# pyvisa 1.4 (http://pyvisa.sourceforge.net/)
#-------------------------------------------------------------------------------

import visa

# connect to scope
scope = visa.instrument('tcpip::134.62.36.68::instr')
print scope.ask('*idn?')

# rest scope and autoset
scope.write('*rst')
scope.write('autoset execute')
scope.ask('*opc?')

# configure single-shot acquisition
scope.write('acquire:state off')
scope.write('acquire:stopafter sequence')

# configure measurement and query the value
scope.write('measurement:immed:source ch1')
scope.write('measurement:immed:type frequency')

for i in range(5):
    # start new acquisition
    scope.write('acquire:state on')

    # wait for acquisition to complete
    scope.ask('*opc?')

    # make the measurement
    print scope.ask('measurement:immed:value?')
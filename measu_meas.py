#-------------------------------------------------------------------------------
#  Using MEASU:MEASU to get frequency measurement on channel 1.


# python 2.7 (http://www.python.org/)
# pyvisa 1.4 (http://pyvisa.sourceforge.net/)
#-------------------------------------------------------------------------------

import visa
import time

#Connect to scope
scope = visa.instrument('tcpip::134.62.34.164::instr')
print scope.ask("*IDN?")
#Rest scope and autoset
scope.write("*RST")
scope.write("AUTOset EXECute")
scope.ask("*OPC?")
#Configure measurement and query the value
scope.write("MEASUrement:MEAS1:SOURCE CH1")
scope.write("MEASUrement:MEAS1:TYPE FREQuency")
scope.write("MEASUrement:MEAS1:STATE ON")
time.sleep(.5)
print scope.ask("MEASUrement:MEAS1:VALue?")




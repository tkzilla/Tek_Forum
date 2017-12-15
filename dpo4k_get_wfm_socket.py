#-------------------------------------------------------------------------------
#  Get a screen catpure from DPO4000 series scope and save it to a file

# python        2.7         (http://www.python.org/)
# numpy         1.6.2       (http://numpy.scipy.org/)
# MatPlotLib    1.0.1       (http://matplotlib.sourceforge.net/)
#-------------------------------------------------------------------------------

import socket
import numpy as np
from struct import unpack
import pylab
import time


class Socket_Instrument(object):
    ''' socket replacement for visa.instrument class'''
    def __init__(self, IPaddress, PortNumber = 4000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((IPaddress, PortNumber))
        self.s.setblocking(False)

    def write(self, cmd):
        self.s.send(cmd + '\n')

    def ask(self, cmd, buffer = 1024, timeout = 5):
        self.s.send(cmd + '\n')
        response = ''
        while True:
            char = ""
            try:
                char = self.s.recv(1)
            except:
                time.sleep(0.1)
                if response.rstrip() != "":
                    break
            if char:
                response += char
        return response.rstrip()

    def read(self):
        response = ''
        while True:
            char = ""
            try:
                char = self.s.recv(1)
            except:
                time.sleep(0.1)
                if response.rstrip() != "":
                    break
            if char:
                response += char
        return response.rstrip()

    def close(self):
        self.s.close()

scope = Socket_Instrument('134.62.36.67')
print scope.ask('*IDN?')

scope.write('DATA:SOU CH1')
scope.write('DATA:WIDTH 1')
scope.write('DATA:ENC RPB')


ymult = float(scope.ask('WFMPRE:YMULT?'))
yzero = float(scope.ask('WFMPRE:YZERO?'))
yoff = float(scope.ask('WFMPRE:YOFF?'))
xincr = float(scope.ask('WFMPRE:XINCR?'))



scope.write('CURVE?')
data = scope.read()
scope.close()
headerlen = 2 + int(data[1])
header = data[:headerlen]
ADC_wave = data[headerlen:-1]

ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))

Volts = (ADC_wave - yoff) * ymult  + yzero

Time = np.arange(0, xincr * len(Volts), xincr)
pylab.plot(Time, Volts)
pylab.show()

'''
Acquire a RF waveform from a MDO and plot it.


python 2.7 (http://www.python.org/)
pyvisa 1.3 (http://pypi.python.org/pypi/PyVISA/1.3)
Numpy 1.6.1 (http://sourceforge.net/projects/numpy/)
'''
import visa
import numpy as np
import pylab
from struct import unpack


def GetCurve(scope):
    temp = scope.timeout
    scope.timeout = 20
    scope.write('CURVE?')
    data = scope.read_raw()
    scope.timeout = temp
    headerlen = 2 + int(data[1])
    header = data[:headerlen]
    wave = data[headerlen:-1]
    return header, wave


scope = visa.instrument('USB0::0x0699::0x040C::QU000136::INSTR')
print scope.ask('*IDN?')

scope.write('DATA:SOU RF_NORMAL')
datalen = int(scope.ask('wfmpre:nr_pt?'))
start = float(scope.ask('rf:start?'))
stop = float(scope.ask('rf:stop?'))
scope.write('DATA:ENC SFP')
header, datac = GetCurve(scope)

#each point is a floating point value, 4 bytes per point
datac = unpack('%sf' % datalen,datac)
step = (stop - start) / (len(datac)-1)
x = np.arange(start, stop + step, step)
y = np.array(datac)
y = 10 * np.log10(y/.001)




pylab.plot(x,y)
pylab.xlim(start, stop)
pylab.show()
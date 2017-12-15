# rsa_snmp_test.py
# proof of concept for continuous monitoring of a frequency level
# with an snmp message sent when measurement falls below a set threshold
# uses:
# python v2.7.3 (32-bit): http://www.python.org/
# pyvisa v1.4: http://pyvisa.sourceforge.net/
# pyasn1 v0.1.4: http://pyasn1.sourceforge.net/
# pysnmp v4.2.3: http://pysnmp.sourceforge.net/

def main():
    import time
    import visa

    # variables
    threshold = -30 # dBm
    center = 800e6 # Hz
    span = 10e6 # Hz
    trap_destination = '192.168.1.110'

    # instrument connection
    rsa = visa.instrument('gpib8::1')
    print rsa.ask('*idn?')

    # measurement initialization
    print 'setting up measurement'
    rsa.write('*rst') # reset instrument to start from known state
    rsa.write('abort') # stop acquisitions while measurement is configured
    rsa.write('spectrum:frequency:center %e' % center)
    rsa.write('spectrum:frequency:span %e' % span)
    rsa.write('calculate:marker:add')
    rsa.write('calculate:spectrum:marker0:x %e' % center)
    rsa.write('initiate') # start acquisitions
    rsa.timeout = 30
    rsa.ask('*opc?') # query to check if acquisitions started
    rsa.timeout = 5

    # initial measurement
    a = rsa.ask_for_values('calculate:spectrum:marker0:y?')
    if a[0] > threshold:
        low_signal = False
    else:
        low_signal = True

    # measurement loop
    print 'setup done, measuring signal'
    try:
        while True:
            if a[0] > threshold:
                if low_signal:
                    print('signal restored')
                    low_signal = False
                else:
                    print('signal nominal')
            else:
                if low_signal:
                    print('low signal')
                else:
                    print('low signal, sending message')
                    send_trap(trap_destination)
                    low_signal = True
            time.sleep(1)
            a = rsa.ask_for_values('calculate:spectrum:marker0:y?')
    except:
        print 'measurements stopped'

def send_trap(ip_addr = '127.0.0.1'):
    from pysnmp.entity.rfc3413.oneliner import ntforg
    from pysnmp.proto import rfc1902

    def cbFun(sendRequestHandle, errorIndication, cbCtx):
        if errorIndication:
            print(errorIndication)
        else:
            print('INFORM %s delivered' % sendRequestHandle)

    ntfOrg = ntforg.AsynNotificationOriginator()

    ntfOrg.sendNotification(
        ntforg.CommunityData('public'),
        ntforg.UdpTransportTarget((ip_addr, 162)),
        'inform',
        ntforg.MibVariable('SNMPv2-MIB', 'coldStart'),
        ( ('1.3.6.1.2.1.1.5.0', rfc1902.OctetString('system name')), ),
        (cbFun, None)
    )

    ntfOrg.snmpEngine.transportDispatcher.runDispatcher()

if __name__ == '__main__':
    main()

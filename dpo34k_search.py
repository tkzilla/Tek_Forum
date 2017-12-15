# dpo 3k/4k search example
# attach prob comp signal to channel 1

import time
import visa  # pyvisa v1.4 http://sourceforge.net/projects/pyvisa/

mdo = visa.instrument('tcpip::192.168.1.65::instr')
r = mdo.ask('*idn?')
print(r)


def print_status():
    r = mdo.ask('*esr?')
    r = int(r)
    print('event status register: 0b{:08b}'.format(r))
    print(mdo.ask('allev?'))


def return_status():
    r = mdo.ask('*esr?')
    r = int(r)
    if r != 0:
        print(mdo.ask('allev?'))
    return r


def setup():
    mdo.write('*rst')
    mdo.write('acquire:state off')
    mdo.write('header off')
    # set volts/div
    mdo.write('ch1:scale 0.5')
    # set position
    mdo.write('ch1:position -2.5')
    # set trigger level
    mdo.write('trigger:a:level:ch1 1.25')
    # set time/div
    mdo.write('horizontal:scale 400e-6')
    mdo.write('acquire:stopafter seq')
    print('check status')
    print_status()


def acq1():
    mdo.write('acquire:state on')
    mdo.write('*opc?')
    attempts = 0
    while attempts < 5:
        print('attempt: {}'.format(attempts))
        try:
            r = mdo.read()
            print('triggered')
            break
        except:
            print('no trigger')
            attempts += 1
    if attempts == 5:
        raise Exception('no trigger after 5 attempts')
    print('acquire done, checking status')
    print_status()


def search():
    mdo.write('search:search1:trigger:a:level 2.0')
    mdo.write('search:search1:state on')
    r = mdo.ask('search:search1:total?')
    attempts = 0
    while attempts < 10:
        t = return_status()
        if t == 0:
            break
        else:
            attempts += 1
            time.sleep(0.05)
            r = mdo.ask('search:search1:total?')
    if attempts == 10:
        raise Exception('measurement could not complete after 10 attempts')
    print('found {} edges'.format(r))


def main():
    print('@@ clear instrument status...')
    mdo.write('*cls')
    print('@@ setup scope...')
    setup()
    print('@@ acquire 1 waveform...')
    acq1()
    print('@@ search with good delay handling...')
    search()
    print('@@ same search, note no delay...')
    search()
    print('@@ acquire again...')
    acq1()
    print('@@ search again...')
    search()
    print('@@ check instrument status...')
    print_status()


if __name__ == "__main__":
    main()

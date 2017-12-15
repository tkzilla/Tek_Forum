# Date: 6/24/14
# Tested on a 64-bit Windows 7 computer
# using Ni-VISA 5.4 with Python 2.7.6, and PyVISA 1.5
# Tested on TDS3054B and TDS3054C
# Program: Import settings to scope
# This program lets the user save scope settings to a text file, default the scope,
# and load settings to the scope from a file.

import visa
from sys import exit

#Open visa object
scope = visa.instrument('tcpip::tsc-tds3054c::instr')

#Identify instrument
ID = scope.ask('*IDN?')
print(ID)

#Control loop
while True:
    directive = raw_input('What would you like to do?\n'
                          'Save scope settings to a file. (type \"1\")\n'
                          'Load default settings on the scope. (type \"2\")\n'
                          'Load scope settings from a file. (type \"3\")\n'
                          'Quit. (type "q")\n>>>')

    if directive == '1':
        settings = scope.ask('*LRN?')   #Get settings string
        print('Settings transferred to Python.')
        filename = raw_input('What would you like to call your file?\n>>>') #specify filename
        setfile = open(filename, 'w')   #open file with write permission
        setfile.write(settings)         #write the settings string to the file
        setfile.close()                 
        print('File created in default directory.\n')
    elif directive == '2':
        scope.write('*RST')
        print('Scope returned to default setup.\n')
    elif directive == '3':
        filename = raw_input('What file would you like to load?\n>>>')      #specify filename
        setfile = open(filename, 'r')   #open file with read permission
        settings = setfile.read()       #read contents to settings variable
        scope.write(settings)           #write settings to scope
        print('Settings transferred to scope.\n')
    elif directive == 'q':
        print('Bye.\n')
        exit(0)
    else:
        print('Invalid choice. Please choose 1, 2, 3, or q and press Enter.\n')

## Python Socket Control 1
# Date: 09-15-2009
# ==================
# Demonstrate how to communicate with Tektronix instruments using an TCP socket
# connection.
#
# COMPATIBILITY
# ==================
# All Windows based instruments with TekVISA v3.2 or later
# AWG400, 500, 600, 700
# ==================
#
# TESTED & DEVELOPED
# ==================
# Microsoft Windows XP SP3
# Python v2.6
# Ethernet (DHCP)
# DPO7254 FW v4.3.5 Build 6
# ==================
#
# Tektronix provides the following example "AS IS" with no support or warranty.
 
import socket
 
input_buffer = 2 * 1024
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("134.62.63.56", 4000))
 
cmd = "*idn?" + "\n"
s.send(cmd)
id = s.recv(input_buffer)
print id
 
cmd = "*rst" + "\n"
s.send(cmd)
 
s.close()


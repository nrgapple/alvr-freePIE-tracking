import socket
import sys
import time
import struct
import signal

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
    
def loop():
    s = struct.Struct('f f f f f f')
    data = serverSock.recv(s.size)
    unpacked_data = s.unpack(data)

    #alvr.head_position[0] = unpacked_data[0] * multiplier
    #alvr.head_position[1] = unpacked_data[1] * multiplier
    #alvr.head_position[2] = unpacked_data[2] * multiplier

    #alvr.head_orientation[0] = unpacked_data[3]
    #alvr.head_orientation[1] = unpacked_data[4]
    #alvr.head_orientation[2] = unpacked_data[5]
	#diagnostics.debug("x: {0}", str(unpacked_data[0]))
    diagnostics.watch(unpacked_data)

# update -----
if starting:
	serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
	serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
	#alvr.override_head_position = True
	#alvr.override_head_orientation = True

loop()

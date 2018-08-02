import time
import sys
import socket 
import struct
import random

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

def get_values():
    x = random.randrange(1, int(time.time())) / int(time.time())
    y = random.randrange(1, int(time.time())) / int(time.time())
    z = random.randrange(1, int(time.time())) / int(time.time())
    r_x = random.randrange(1, int(time.time())) / int(time.time())
    r_y = random.randrange(1, int(time.time())) / int(time.time())
    r_z = random.randrange(1, int(time.time())) / int(time.time())
    data = [x, y, z, r_x, r_y, r_z]

    return data

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (UDP_IP_ADDRESS, UDP_PORT_NO)

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    while(True):
        start = time.time()

        data = get_values()
        print("\r" + "sending data=" + str(data),  end="")
        packer = struct.Struct('f f f f f f')
        packed_data = packer.pack(*data)
        try:
            sent = sock.sendto(packed_data, server_address)
        except:
             print("error")
        #print("\r" + binascii.hexlify(packed_data), end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
import time
import sys
import socket 
import struct
import triad_openvr
import math

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
INTERVAL_ARG = '-i'
TRACKED_DEVICE = '-d'

def get_values(name):
    data = v.devices[name].get_pose_euler()
    for i in range(3, 6):
        data[i] = math.radians(data[i])
    return data


# Main ------
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (UDP_IP_ADDRESS, UDP_PORT_NO)


if INTERVAL_ARG in sys.argv:
    interval = 1/float(sys.argv[sys.argv.index(INTERVAL_ARG) + 1])
else:
    interval = 1/250

if TRACKED_DEVICE in sys.argv:
    device_name = sys.argv[sys.argv.index(TRACKED_DEVICE) + 1]
else:
    device_name = list(v.devices.keys())[0]
    
if interval:
    print("sending data for device [" + device_name + "]:")
    print("  x=   |  y=   |  z=   | r_x=  | r_y=  | r_z   |")
    while(True):
        start = time.time()
        
        data = get_values(device_name)
        txt = ""
        for each in data:
            if each > 0:
                txt += " "
            txt += "%.4f" % each
            txt += "|"
        
        print("\r" + txt,  end="")
        packer = struct.Struct('f f f f f f')
        packed_data = packer.pack(*data)
        try:
            sent = sock.sendto(packed_data, server_address)
        except:
             print("error")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
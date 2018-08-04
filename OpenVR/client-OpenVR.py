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


valid = False
dot = 0
wasEverInvalid = False
while valid is False:
    try:
        v = triad_openvr.triad_openvr()
    except:
        wasEverInvalid = True
        dot = dot + 1
        dot_string = ""
        for i in range(dot % 10):
            dot_string += "."
        print("\r" + "still searching for tracker" + dot_string, end="", flush=True)  
        v = triad_openvr.triad_openvr()
        time.sleep(.5) 
    finally:
        valid = True    
if wasEverInvalid is True:
    print(end="\n")

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

def get_values(tracker_name, reference_device):
    tracker_data = device.get_pose_euler_uncalibrated()
    reference_data = reference_device.get_pose_euler_uncalibrated()

    tracker_data[0] = tracker_data[0]
    tracker_data[2] = tracker_data[2]
    send_pos = list(map(float.__sub__, tracker_data, reference_data))

    for i in range(3, 6):
        send_pos[i] = math.radians(send_pos[i])

    return send_pos

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

valid2 = False    
dot = 0
wasEverInvalid2 = False
while valid2 is False:
    for device in v.object_names["Tracking Reference"]:
        mode = v.devices[device].get_mode()
        if mode == 'C':
            ref_dev = v.devices[device]
            print("found" + str(ref_dev))
            valid2 = True
    if valid2 is False:
        wasEverInvalid2 = True
        dot = dot + 1
        dot_string = ""
        for i in range(dot % 10):
            dot_string += "."
        print("\r" + "searching for ref" + dot_string, end="", flush=True)  
        v = triad_openvr.triad_openvr()
        time.sleep(.5)
if wasEverInvalid is True:
    print("\n")

valid3 = False
dot = 0
wasEverInvalid = False
while valid3 is False:
    v = triad_openvr.triad_openvr()
    for key, value in v.devices.items():
        if key == device_name:
            valid3 = True
            device = value
    if valid3 is False:
        wasEverInvalid = True
        dot = dot + 1
        dot_string = ""
        for i in range(dot % 10):
            dot_string += "."
        print("\r" + "still searching for tracker" + dot_string, end="", flush=True)  
        v = triad_openvr.triad_openvr()
        time.sleep(.5)     
if wasEverInvalid is True:
    print(end="\n") 

if interval:
    print("sending data for device [" + device_name + "]:")
    print("  x=   |  y=   |  z=   | r_x=  | r_y=  | r_z=  |")
    while(True):
        start = time.time()
        
        data = get_values(device_name, ref_dev)

        txt = ""
        for each in data:
            if each > 0:
                txt += " "
            txt += "%.4f" % each
            txt += "|"
        print("\r" + txt,  end="", flush=True)
        packer = struct.Struct('f f f f f f')
        packed_data = packer.pack(*data)
        try:
            sent = sock.sendto(packed_data, server_address)
        except:
             print("error")
        prev_pos = data
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
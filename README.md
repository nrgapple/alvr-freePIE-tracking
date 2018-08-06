# alvr-freePIE-tracking
6 Dof tracking for [ALVR](https://github.com/polygraphene/ALVR) using freePIE and OpenVR tracking.

Works with a Vive tracker or just one of your controllers! 

## Usage

1. Open cmd at this path  
  ```
  python client-OpenVR.py -d <tracked-device>
  ```
  The tracked device could be `controller_1`, `controller_2`, or `tracker_1` depending if you have a Vive tracker or not.

2. Open and Run `server-FreePIE.py` in FreePIE


3. While in ALVR in your headset, take it off and then put it back on looking directly at your first light house. This should properly orient you.

4. Thats it! It works pretty good!

Thanks u/penkamaster for adding that you have to look at the light house for it to correctly orient you. That was the final step I needed!

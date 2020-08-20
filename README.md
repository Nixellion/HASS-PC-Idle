# PC Idle

Here's a little script I wrote to track when a PC is being used or not, and change a boolean in HomeAssistant based on that. I use it to enhance room-prescence detection, as bluetooth tracking is not very reliable when it comes to tracking RSSI. 

## Installation

Currently only Windows is supported, Linux support will come some day.

1. If you don't have it yet, download Python 3.x from python.org and install it.
2. Open windows CMD
3. `cd DISK:` where DISK is the drive letter you have the script on
4. `cd path` where you can copy paste the path to the pc_idle.py without the filename
5. `pip3 install -r requirements.txt` to install all the dependencies
5. Copy config-example.yaml into config.yaml
6. Open config.yaml and enter your HomeAssistant API URL. Could be an IP or a domain name.
7. Go to your HomeAssistant -> Profile -> and generate a long lived token
8. Paste it into config after `token:`... Well, if you use HomeAssistant you should know YAML :D
9. Adjust other parameters to your liking
10. In the CMD type `pc_idle.py` and hit enter. (You may need to specifically type `python3 pc_idle.py` or worst case `C:\PathToPython\python.exe pc_idle.py` but this most likely means that Python is not in your PATH environment variable and is installed wrongly. If you did it on purpose then you know how to fix it though :) )

You can also use Windows Scheduler to schedule it to start on boot or login. 

By default every second it will check if a PC was idle for more than 10 seconds, and if it was - it will turn_on the boolean. If it's less than 10 seconds it will turn_off the boolean. So the logic in naming and using your boolean should be "Is_PC_Idle?". 

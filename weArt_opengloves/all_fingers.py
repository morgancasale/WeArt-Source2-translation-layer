import time
import logging
from utilities import *

max_analog_value_OpenGloves = 255
triggerThreshold = max_analog_value_OpenGloves/2

# Connection to the OpenGloves driver settings
communication_through_pipes = False

pipe_path = "\\\\.\\pipe\\vrapplication\\input\\glove\\v2\\right"
COM_port = "COM8" # set COM9 (COMn+1) in the openGloves driver
baud_rate = 115200


# Create a WeArtClient object
client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT, log_level=logging.INFO)
client.Run()
client.Start()
print("WeArt client connected!")

# Listener to receive data status from Middleware
mwListener = MiddlewareStatusListener()
client.AddMessageListener(mwListener)

# Calibration manager 
calibration = WeArtTrackingCalibration()
client.AddMessageListener(calibration)
# Start Calibration Finger tracking algorithm
client.StartCalibration()

# Wait for the result
print("Calibrating...")
while(not calibration.getResult()):
    time.sleep(1)
print("Calibration completed!")

# Stop calibration
client.StopCalibration()

time.sleep(2)

fingers_act_points = [ActuationPoint.Thumb, ActuationPoint.Index, ActuationPoint.Middle]

# Add finger tracking for each finger
fingersTracking = [WeArtThimbleTrackingObject(HandSide.Right, point) for point in fingers_act_points]
[client.AddThimbleTracking(fingerTracking) for fingerTracking in fingersTracking]
print("Added finger tracking for each finger!")

time.sleep(2)

ser = None

if not communication_through_pipes:
    try:
        ser = serial.Serial(COM_port, baud_rate, timeout=1)
        print("Serial port connected!")
    except:
        print("Serial port connection failed!")
        exit()

while True:
    flexion = []
    splay = []

    finger_names = ["Thumb", "Index", "Middle"]
    i = 0
    for fingerTracking in fingersTracking:
        print(f"Reading tracking data for {finger_names[i]} finger: ")

        closures = getClosuresOG_to_WeArt(fingerTracking, max_analog_value_OpenGloves)
        flexion.append(closures)

        if(i == 0):
            spl = getSplayOG_to_WeArt(fingerTracking, max_analog_value_OpenGloves)
            splay.append(spl)

        i += 1
    
    flexion = flexion + [flexion[2]]*2

    splay += [int(max_analog_value_OpenGloves/2)]*4

    if communication_through_pipes:
        # Send the flexion and splay values to the OpenGloves driver through named pipes
        sendPipePacket(pipe_path, buildPipePacket(flexion, splay))
    else:
        # Send the flexion and splay values to the OpenGloves driver through COM port
        sendCOMPacket(ser, buildCOMPacket(flexion, splay, triggerThreshold))
        
    # printTrackingInfo(flexion, splay)

    time.sleep(0.1)
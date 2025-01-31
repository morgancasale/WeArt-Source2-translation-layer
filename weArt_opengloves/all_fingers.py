import time
import logging
from utilities import *

max_analog_value_OpenGloves = 255

pipe_path = "\\\\.\\pipe\\vrapplication\\input\\glove\\v2\\right"

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

time.sleep(5)

fingers_act_points = [ActuationPoint.Thumb, ActuationPoint.Index, ActuationPoint.Middle]

# Add finger tracking for each finger
fingersTracking = [WeArtThimbleTrackingObject(HandSide.Right, point) for point in fingers_act_points]
[client.AddThimbleTracking(fingerTracking) for fingerTracking in fingersTracking]
print("Added finger tracking for each finger!")

time.sleep(5)

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

    splay += [max_analog_value_OpenGloves/2]*4

    # Send the flexion and splay values to the OpenGloves driver
    # with open(pipe_path, "wb") as pipe:
    #     pipe.write(buildPipePacket(flexion, splay))
    sendPacket(pipe_path, buildPipePacket(flexion, splay))

    # printTrackingInfo(flexion, splay)

    time.sleep(1)
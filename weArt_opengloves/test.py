from weartsdk.WeArtHapticObject import WeArtHapticObject
from weartsdk.WeArtCommon import HandSide, ActuationPoint, CalibrationStatus, TextureType
from weartsdk.WeArtTemperature import WeArtTemperature
from weartsdk.WeArtTexture import WeArtTexture
from weartsdk.WeArtForce import WeArtForce
from weartsdk.WeArtEffect import TouchEffect
from weartsdk.WeArtTrackingCalibration import WeArtTrackingCalibration
from weartsdk.WeArtThimbleTrackingObject import WeArtThimbleTrackingObject
from weartsdk.WeArtTrackingRawData import WeArtTrackingRawData
from weartsdk.MiddlewareStatusListener import MiddlewareStatusListener
from weartsdk.WeArtAnalogSensorData import WeArtAnalogSensorData

from weartsdk.WeArtClient import WeArtClient
from weartsdk import WeArtCommon

import time
import logging

'''
Sample demo script to show the functionallity of the WEART Python SDK 
'''

if __name__ == '__main__':
    
    # Istantiate TCP/IP client to communicate with the Middleware
    client = WeArtClient(WeArtCommon.DEFAULT_IP_ADDRESS, WeArtCommon.DEFAULT_TCP_PORT, log_level=logging.INFO)
    client.Run()
    client.Start()

    # Listener to receive data status from Middleware
    mwListener = MiddlewareStatusListener()
    client.AddMessageListener(mwListener)

    # Calibration manager 
    calibration = WeArtTrackingCalibration()
    client.AddMessageListener(calibration)
    # Start Calibration Finger tracking algorithm
    client.StartCalibration()

    # Wait for the result
    while(not calibration.getResult()):
        time.sleep(1)
    
    # Stop calibration
    client.StopCalibration()


    # Istantiate a ThimbeTrackingObject to read closure and abductions value from the thimble
    fingerTracking = WeArtThimbleTrackingObject(HandSide.Right, ActuationPoint.Index)
    client.AddThimbleTracking(fingerTracking)

    # Read tracking data for 200 iterations
    for i in range(200):
        closure = fingerTracking.GetClosure()
        abduction = fingerTracking.GetAbduction()
        print(f"{closure}, {abduction}")
        time.sleep(0.1) 
    
    '''
    # Instantiate Analog Sensor raw data
    # This feature work just enabling the functionality from the Middleware
    # during this condition streaming the WeArtTrackingRawData doesn't work
    analogSensorData = WeArtAnalogSensorData(HandSide.Right, ActuationPoint.Index)
    client.AddMessageListener(analogSensorData)

    # Read sample analog sensor data
    ts = analogSensorData.GetLastSample().timestamp
    while ts == 0:
        time.sleep(1)
        ts = analogSensorData.GetLastSample().timestamp
    sample = analogSensorData.GetLastSample()
    print(sample)
    '''

    
    # Stop client and close the commnunication with the Middleware
    client.Stop()
    client.Close()
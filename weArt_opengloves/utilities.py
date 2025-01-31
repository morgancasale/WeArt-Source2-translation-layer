import numpy as np
import struct

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

def getClosuresOG_to_WeArt(fingerTracking, max_analog_value_OpenGloves):
    # OpenGloves SDK:
    # All finger inputs (splay and curl + joint curls) are scalar values. 
    # They range from 0 to the max analog value.
    WA_closure = fingerTracking.GetClosure()
    

    # WeArt SDK:
    # The closure value ranges from 0 (opened) to 1 (closed).
    OG_closure = np.interp(WA_closure, [0, 1], [0, max_analog_value_OpenGloves])
    print(f"WAClosure --> OGClosure: {WA_closure} --> {OG_closure}")

    # OpenGloves SDK:
    # <finger> joint 0 encodes for the carpometacarpal joint (this is typically only used by the thumb). 
    # It should most likely be left blank for any other finger.
    # <finger> joint 1 encodes for the bend at the metacarpophalangeal joint
    # <finger> joint 2 encodes for the bend at the proximal interphalangeal joint
    # <finger> joint 3 encodes for the bend at the distal interphalangeal joint (not present on thumb)
    # If a curl of a joint is not specified, the curl for the whole hand is used.
    closures = [0] + [OG_closure]*3

    return closures

def getSplayOG_to_WeArt(fingerTracking, max_analog_value_OpenGloves):
    # OpenGloves SDK:
    # For splay, half the max analog value is set as the finger being straight, 
    # without any splay, and decreasing towards 0 is splaying the finger to the left. 
    # The maximum value is 10 degrees, but can be changed.
    WA_splay = fingerTracking.GetAbduction()
    
    # WeArt SDK:
    # The abduction value ranges from 0 (finger near the hand's central axis) 
    # to 1 (finger far from the hand central axis).
    OG_splay = np.interp(WA_splay, [0, 1], [max_analog_value_OpenGloves/2, 0])
    print(f"WASplay --> OGSplay: {WA_splay} --> {OG_splay}")

    return OG_splay

def buildPipePacket(flexion, splay):
    # OpenGloves SDK:
    # // "\\.\pipe\vrapplication\input\glove\v2\<left/right>"
    # struct InputData {
    #   const std::array<std::array<float, 4>, 5> flexion;
    #   const std::array<float, 5> splay;
    #   const float joyX;
    #   const float joyY;
    #   const bool joyButton;
    #   const bool trgButton;
    #   const bool aButton;
    #   const bool bButton;
    #   const bool grab;
    #   const bool pinch;
    #   const bool menu;
    #   const bool calibrate;
    #   const float trgValue;
    # };
    
    # Define the struct format based on InputData
    # flexion: 4x5 floats, splay: 5 floats, joyX: float, joyY: float, 10 booleans, trgValue: float
    # 20 floats for flexion, 5 floats for splay, 2 floats for joy, 10 booleans, 1 float
    STRUCT_FORMAT = "<20f5f2f10?f"

    joyX, joyY = 0, 0
    booleans = [False]*8
    trgValue = 0

    # Combine all the data into a single list
    data = flexion + splay + [joyX, joyY] + booleans + [trgValue]

    return struct.pack(STRUCT_FORMAT, *data)

def printTrackingInfo(flexion, splay):
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    for i, (flex, spl) in enumerate(zip(flexion, splay)):
        print(f"{finger_names[i]}: Flexion = {flex}, Splay = {spl}")

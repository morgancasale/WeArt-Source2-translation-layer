import socket
import json
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip=socket.gethostbyname("127.0.0.1")
port=29000
address=(ip,port)
client.connect(address)
while True:
    data = client.recv(1024)
    msg = str(data).split("[WeArt_s] ")

    if(len(msg)>1):
        msg = msg[1].split(" [WeArt_e]")[0]
        info = json.loads(msg)

        for fingerInfo in info:
            print("Finger: " + fingerInfo["fingername"])
            modelname = fingerInfo["modelname"] if fingerInfo["modelname"] is not None else "None"
            print("Model: " + modelname + "\n")
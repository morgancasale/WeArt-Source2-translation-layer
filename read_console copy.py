import socket
from threading import Thread
import json

models = {}

def receive_data(client_socket, models):
    while True:
        try:
            # Receive data from server
            data = client_socket.recv(1024)
            print(str(data))
            msg = str(data).split("[WeArt_s] ")

            if len(msg) > 1:
                msg = msg[1].split(" [WeArt_e]")[0]
                print(msg)

                if "mapname" in msg:
                    models = json.loads(msg)
                    models["models"] = []
                elif "Model: " in msg:
                    model = msg.split("Model: ")[1]
                    models["models"].append(model)
                elif "END" in msg:
                    json.dump(models, open("models.json", "w"))

                # for fingerInfo in info:
                #     print("Finger: " + fingerInfo["fingername"])
                #     modelname = fingerInfo["modelname"] if fingerInfo["modelname"] is not None else "None"
                #     print("Model: " + modelname + "\n")
        except Exception as e:
            print(f"Error receiving data: {e}")
            client_socket.close()
            break

def send_data(client_socket):
    while True:
        try:
            # Get user input to send to server
            message = input("Enter message to send to server: ")
            client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending data: {e}")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = socket.gethostbyname("127.0.0.1")
    port = 29000
    address = (ip, port)

    # Connect to server
    client.connect(address)
    print("Connected to server.")

    # Create threads for sending and receiving
    receive_thread = Thread(target=receive_data, args=(client,models,))
    send_thread = Thread(target=send_data, args=(client,))

    # Start threads
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    # Close the connection
    client.close()

if __name__ == "__main__":
    main()

import os
import speech_recognition as sr
import socket
import tqdm

#setting up socket engine
server_ip = '127.0.0.1'
server_port = 9999
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen()
connection, client_address = sock.accept()
filename = '2'+connection.recv(1024).decode()
filesize = connection.recv(1024).decode()

print("Connection from", client_address)
print(filename)   
print(filesize)


received_file = open(filename, 'wb')
filebytes = b""

done = False

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(filesize))

while not done:
    data = connection.recv(1024)
    if filebytes[-5:] == b"<END>":
        done = True
    else:
        filebytes = filebytes + data
        progress.update(1024)
        received_file.write(data)
        #received_file.close()
        #connection.close()
        #sock.close()
      
        #processing data
        #if cooked_porridge:
        #    r = sr.Recognizer()
        #    with sr.AudioFile(cooked_porridge) as source:
        #        audio_data = r.record(source)
        #        text = r.recognize_google(audio_data)
        #        print(text)
        #        print("Sending data back to the client")
        #        connection.sendall(text)
        #else:
        #    print("No more data from", client_address)
        #    break

    #connection.close()




import speech_recognition as sr
import socket

server_ip = '127.0.0.1'
server_port = 5000
server_address = (server_ip, server_port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)

sock.listen(1)

while True:
    print("Waiting for connection")
    connection, client_address = sock.accept()
    print("Connection from", client_address)

    while True:
        data = connection.recv(1024)
        print("Received", data)
        print('processing data')
        
        
        
        if data:
            print("Sending data back to the client")
            connection.sendall(data)
        else:
            print("No more data from", client_address)
            break

    connection.close()



filename = "test.wav"
r = sr.Recognizer()

with sr.Audiofile(filename) as source:
    audio_data = r.record(source)
    text = r.recognize_google(audio_data)
    print(text)
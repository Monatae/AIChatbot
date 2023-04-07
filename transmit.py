import os
import socket
server_ip = '127.0.0.1'
server_port = 5001
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address))


#function to send audio file
def sendaudio(filename):
    file = open(filename, 'rb')
    data = file.read()
    filesize = str(os.path.getsize(filename = filename))
    sock.send(filename.encode())
    sock.send(filesize.encode(errors='ignore'))
    sock.sendall(data)
    sock.send(b"<END>")
    file.close()
    

def receive_transcript():
    transcript = sock.recv(1024).decode() 
    print(transcript)



if __name__ == "__main__":
    sendaudio('test.wav')
    receive_transcript()
    
    
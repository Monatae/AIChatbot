import os, socket


#setting up connection to the speech recognition server
server_ip = '127.0.0.1'
server_port = 9999
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address))




filename = 'test.wav'
file = open(filename, 'rb')
data = file.read()
filesize = str(os.path.getsize(filename = filename))

def sendaudio(filename):
    sock.send(filename.encode())
    sock.send(filesize.encode(errors='ignore'))
    sock.sendall(data)
    sock.send(b"<END>") 
    #file.close()
    #sock.close()


if __name__ == "__main__":
    sendaudio('test.wav')
    
    
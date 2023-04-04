import socket
import tqdm
from time import sleep
from google.cloud import speech

# setting up socket engine
server_ip = "127.0.0.1"
server_port = 9999
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen()


connection, client_address = sock.accept()
filename = "3" + connection.recv(1024).decode()
filesize = connection.recv(1024).decode()

print("Connection from", client_address)
print(filename)
print(filesize)


received_file = open(filename, "wb")
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
        received_file.close()
        print("No more data from", client_address)
        break

sleep(10)

# speech recognition
client = speech.SpeechClient.from_service_account_file("key.json")

with open("test.wav", "rb") as f:
    content = f.read()

audio_file = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    sample_rate_hertz=16000, enable_automatic_punctuation=True, language_code="en-US"
)

response = client.recognize(config=config, audio=audio_file)


for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
    connection.send("{}".format(result.alternatives[0].transcript).encode())

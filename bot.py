from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import socket
#from transmit import sendaudio, receive_transcript
from datalab import *

#setting up connection to the speech recognition server
server_ip = '127.0.0.1'
server_port = 5000
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((server_address))
####this is where sendaudio and receive_transcript functions come into play#####


#setting up the chatbot
friday = ChatBot("Friday",
                 read_only = True,
                 storage_adapter ="chatterbot.storage.SQLStorageAdapter",
                 database_uri="sqlite:///database.sqlite3"
                 )

#training the chatbot
friday.set_trainer(ChatterBotCorpusTrainer)
friday.train("chatterbot.corpus.english.quries", "chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")
exit_tuple = ('exit', 'see you later', 'bye')
user_input = input('You: ') #place twilio whatsapp endpoint here
revised_user_input = user_input.replace('You: ', '', 1)

if check_existence(revised_user_input) == False:
    print('Friday: Sorry, I do not fully understand')
else:
    while check_existence(revised_user_input) == True:
        #this is where the entire exchange will happen
        #user input is fed into the chatbot from this point and the response is generated here.
        #I am the Salt Bae of spaghetti code!
        #Tarmica, this is our custom pre processor function
        if user_input.lower() in exit_tuple:
            print('Friday: Bye')
            break
        else:
            response = friday.get_response(revised_user_input)
            print('Friday: ', response) #place twilio whatsapp endpoint here
        
        
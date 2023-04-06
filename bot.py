from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import socket
#from transmit import sendaudio, receive_transcript
from datalab import *
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

#twilio constants
account_sid = 'AC81c0755065e9eba6542ca94a9571ca8e'
auth_token = '3092f6576db06deb1cac112ea17d86e1'
client = Client(account_sid, auth_token)

#setting up connection to the speech recognition server
server_ip = '127.0.0.1'
server_port = 5001
server_address = (server_ip, server_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_address))
####this is where sendaudio and receive_transcript functions come into play#####


#setting up the chatbot




app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    friday = ChatBot("Friday",
                 read_only = True,
                 storage_adapter ="chatterbot.storage.SQLStorageAdapter",
                 database_uri="sqlite:///database.sqlite3"
                 )

    #training the chatbot
    friday.set_trainer(ChatterBotCorpusTrainer)
    friday.train("chatterbot.corpus.english.quries", "chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")
    exit_tuple = ('exit', 'see you later', 'bye')
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    # Use Chatterbot to generate a response
    if check_existence(incoming_msg) == False:
        resp.message('Sorry, I do not fully understand')
    else:
        while check_existence(incoming_msg) == True:
            if incoming_msg.lower() in exit_tuple:
                resp.message('Bye')
                break
            else:
                response = friday.get_response(incoming_msg)
                statement = response.text
                resp.message(statement)
                break
            
    return str(resp)



if __name__ == '__main__':
    app.run(debug=True, port=5000)


        
        
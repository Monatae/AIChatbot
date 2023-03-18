from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pandas as pd
import sqlite3
import socket

#setting up connection to the speech recognition server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(())



#setting up the chatbot
friday = ChatBot("Friday")

#training the chatbot
friday.set_trainer(ChatterBotCorpusTrainer)
friday.train("chatterbot.corpus.english.quries")

exit_tuple = ('exit', 'see you later', 'bye')

while True:
    #database connection
    con = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query("SELECT * from StatementTable", con)
    
    user_input = input('You: ')
    
    
    if user_input.lower() in exit_tuple:
        print('Friday: Bye')
        break
    
    elif user_input not in df['text']:
        print('Friday: I am sorry, but I do not understand.')
    
    else:
        response = friday.get_response(user_input.replace('You: ', '', 1))
        print('Friday: ', response)
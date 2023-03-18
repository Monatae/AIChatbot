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
friday.train("chatterbot.corpus.english.quries", "chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")

exit_tuple = ('exit', 'see you later', 'bye')

while True:
    #database connection
    connection = sqlite3.connect("db.sqlite3")
    df = pd.read_sql_query("SELECT * from StatementTable", connection)
    
    user_input = input('You: ')
    revised_user_input = user_input.replace('You: ', '', 1)
    
    
    #searching through database
    
    if df.query(revised_user_input) is False:
        print('Friday: I am sorry, but I do not understand.')
        
    elif user_input.lower() in exit_tuple:
        print('Friday: Bye')
        break
    
    else:
        response = friday.get_response(user_input.replace('You: ', '', 1))
        print('Friday: ', response)
    
    
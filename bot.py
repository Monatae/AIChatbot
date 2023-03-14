from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


friday = ChatBot("Friday")

friday.set_trainer(ChatterBotCorpusTrainer)
friday.train("chatterbot.corpus.english",
            "chatterbot.corpus.english.quries")

exit_tuple = ('exit', 'see you later', 'bye')

while True:
    user_input = input('You: ')
    if user_input.lower() in exit_tuple:
        print('Friday: Bye')
        break
    else:
        response = friday.get_response(user_input.replace('You: ', '', 1))
        print('Friday: ', response)
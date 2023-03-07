from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


chatbot = ChatBot("Friday")

#trainer = ListTrainer(chatbot)
#sample_conversation = ['hello', 'how are you?']
#trainer.train(sample_conversation)

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.english", "chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")

exit_tuple = ('exit', 'see you later', 'bye')
while True:
    request = input('You: ')
    if request.lower() in exit_tuple:
        print('Friday: Bye')
        break
    else:
        response = chatbot.get_response(request)
        print('Friday: ', response)
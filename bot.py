from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


friday = ChatBot("Friday", storage_adapter="chatterbot.storage.SQLStorageAdapter", database_uri="sqlite:///database.sqlite3", read_only=True)

#trainer = ListTrainer(chatbot)
#trainer.train(sample_conversation)

friday.set_trainer(ChatterBotCorpusTrainer)
friday.train("chatterbot.corpus.english", "chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")

exit_tuple = ('exit', 'see you later', 'bye')
while True:
    request = input('You: ')
    if request.lower() in exit_tuple:
        print('Friday: Bye')
        break
    else:
        response = friday.get_response(request)
        print('Friday: ', response)
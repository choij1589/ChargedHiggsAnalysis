from secret import token, chat_id
import telegram

class Messenger():
    def __init__(self):
        bot = telegram.Bot(token=token)
    
    def sendMessage(self, text):
        self.bot.sendMessage(chat_id=chat_id, text=text)

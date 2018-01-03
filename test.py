from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup ,ReplyKeyboardMarkup,ReplyKeyboardRemove
from transitions.extensions import GraphMachine
import logging
import random
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

class TocMachine(GraphMachine):
    def __init__(self):
        self.machine = GraphMachine(
            model = self,
            states=[
                'user',
                'state1',
                'state2',
                'state3',
                "state4"
            ],
            transitions=[
                {
                    'trigger': 'advance',
                    'source': 'user',
                    'dest': 'state1',
                    'conditions': 'is_going_to_state1'
                },
                {
                    'trigger': 'advance',
                    'source': 'user',
                    'dest': 'state2',
                    'conditions': 'is_going_to_state2'
                },
                {
                    'trigger': 'advance',
                    'source': 'user',
                    'dest': 'state3',
                    'conditions': 'is_going_to_state3'
                },
                {
                    'trigger': 'go_back',
                    'source': [
                        'state1',
                        'state2',
                        'state4'
                        
                    ],
                    'dest': 'user'
                },
                {
                    'trigger': 'go_otherstate',
                    'source': 'state3',
                    'dest': 'state4',
                    'conditions':'is_going_to_state4'
                }

            ],
            initial='user',
            auto_transitions=False,
            show_conditions=True
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        #return text.lower() == 'go to state1'#if the text equal to go to state 1 return true
        return text.lower() == 'any moe girl?'
    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'tell me something'
    
    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == 'are u a good robot?'
    def is_going_to_state4(self,update):
        judge = 0 
        if(update.message.text.lower()=='chose1'):
            judge = 1
        elif(update.message.text.lower()=='chose2'):
            judge = 1
        return judge == 1

    def on_enter_state1(self, update):
        update.message.reply_text("here is your moe girl")
        select = random.randint(1,5)
        if select == 1:
            update.message.reply_photo('http://www.v3wall.com/wallpaper/1920_1080/1201/1920_1080_20120107124215764155.jpg')
        elif select == 2:
            update.message.reply_photo('https://i2.kknews.cc/SIG=ba8uqs/39n500044spoon747s1r.jpg')
        elif select == 3:
            update.message.reply_photo('https://i.pximg.net/c/600x600/img-master/img/2016/06/11/20/15/26/57343936_p0_master1200.jpg')
        elif select == 4:
            update.message.reply_photo('https://farm7.static.flickr.com/6061/6046161500_3e06d987ee.jpg')
        else:
            update.message.reply_photo('https://truth.bahamut.com.tw/s01/201507/7aecd9f64d4509479b78e3bbed1a7c9c.JPG')
        self.go_back(update)
    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        #update.message.reply_text("I'm entering state2")
        keyboard = [[InlineKeyboardButton("維基介紹", url='https://zh.wikipedia.org/wiki/%E5%91%BD%E9%81%8B%E7%9F%B3%E4%B9%8B%E9%96%80')],
                [InlineKeyboardButton("動畫pv", url='https://www.youtube.com/watch?v=dd7BILZcYAY')],
                [InlineKeyboardButton("巴哈姆特討論區", url='https://forum.gamer.com.tw/A.php?bsn=17358')]]
        reply = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("here is a recommanded anime",reply_markup=reply)
        self.go_back(update)
       
    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("I'm entering state3")
        #testkeyboard = [['chose1'],['chose2']]
        #reply_keybaord = ReplyKeyboardMarkup(testkeyboard)
        #update.message.reply_text(text="which choice do u want to take",reply_markup=reply_keybaord)
        self.go_otherstate(update)

    def on_exit_state3(self, update):
        print('Leaving state3')
    
    
    def on_enter_state4(self, update):

        #reply_keybaord = ReplyKeyboardRemove()
        #update.message.reply_text(text="done",reply_markup=reply_keybaord)
        update.message.reply_text("yes i am")
        #if(update.message.text.lower()=='chose1'):
            #update.message.reply_text("I 11")
        #else:
            #update.message.reply_text("I22")
        self.go_back(update)

    def on_exit_state4(self, update):
        print('Leaving state4')
    


machine = TocMachine()
machine.get_graph().draw('my_state_diagram.png', prog='dot')
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    # update.message.reply_text(update.message.text)
    machine.advance(update)

def echo2(bot, update):
    machine.go_otherstate(update)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("524666257:AAHK__fkicu641tjPeDi-w0lnWExUpDIgWs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, echo2))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
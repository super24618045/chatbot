from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from transitions.extensions import GraphMachine
import logging

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
                        'state3'
                    ],
                    'dest': 'user'
                },
                {
                    'trigger': 'go_otherstate',
                    'source': 'state3',
                    'dest': 'state1'
                },
                {
                    'trigger': 'gogoro',
                    'source': 'state2',
                    'dest': 'state1'
                },

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
        return text.lower() == 'go to menu'
    
    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == 'want?'

    def on_enter_state1(self, update):
        update.message.reply_text("here is your moe girl")
        update.message.reply_photo('http://www.v3wall.com/wallpaper/1920_1080/1201/1920_1080_20120107124215764155.jpg')
        self.go_back(update)
    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        #update.message.reply_text("I'm entering state2")
        keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("here is the menu",reply_markup=reply_markup)
        query=update.callback_query
        if query.data == '1':
            self.go_back(update)
        else:
            self.gogoro(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("I'm entering state3")
        self.go_go_otherstate(update)

    def on_exit_state3(self, update):
        print('Leaving state3')
    


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
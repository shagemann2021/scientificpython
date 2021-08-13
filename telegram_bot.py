from telegram.ext import *
from telegram import Update
import responses as re
import scipy_webscraper as scraper
import matplotlib.pyplot as plt
import messenger as pleasedoit
import scipy_webscraper as scraper

# Indicate starting
print("let's go")


# Bot token
api = '1885324908:AAEs_gWkOZmff-WDVAup5sWdhWebDcKKenc'


# Save user input
global_input = None


# possible switch to activate / deactivate plotting
switch = "off"





'''
Functions for the bot
'''




# Commands
def start_command(update, context):
    '''
    Function for the "/start" commands

    variables:
    update:
    context:
    '''
    update.message.reply_text("I am very limited so far but soon I'll be able to share information about the stock market")


def help_command(update: Update, context: CallbackContext) -> None:
    '''
    Function for the "/help" command. Sends information about the possible commands and the bot itself

    variables:
    update:
    context:
    '''
    update.message.reply_text("I can not help you")


def photo_sender(update: Update, context: CallbackContext) -> None:
    '''
    Function to send photos from url/local path to chat

    variables:
    update:
    context:
    '''

    # Fetches individual id from user
    chat_id = update.message.chat.id
    # Copies photo into chat using the bots function with a path or a url as second argument
    update.message.bot.send_photo(chat_id, open("graph.png", "rb"))


#message_handler
def message_receiver(update: Update, context: CallbackContext) -> None:
    '''
    Passes the user input to responses to get the output of the bot.

    '''
    # Format input
    # "update.message.text" stores user input
    user_input = str(update.message.text).lower()
    # Compute response
    resp = re.response(user_input)

    # Pass response to bot
    update.message.reply_text(resp)


# Sends input from user back to him
# def echo(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(update.message.text)


def user_input_sharer(update: Update, context: CallbackContext) -> None:
    '''
    Saves user input as global variable.

    '''

    #print(type(str(update.message.text)/"/".lower()))
    global global_input
    global_input = str(update.message.text).lower()

    # Call function to share user input with scraper
    scraper.txt_writer(str(global_input))
    #t.lol(global_input)
    #print(global_input)




def error(update, context):
    '''
    Outputs message in console if querie is unmatched.
    '''
    print("Bot received an unknown input")




def main():
    '''
    Where the magic happens.

    We run all the bot commands:
    - initalize it
    - all message- / command- handlers to send stuff to user_input
    - Update the bot every second to check for new user inputs

    The plotting:
    So for plotting happens here too (needs to be in main somehow) but does not work properly
    Completely commented, as it is buggy
    '''
    #print(user_input_sharer())

    #Initialize bot
    bot = Updater(api, use_context = True)
    dispatcher = bot.dispatcher

    # Command handler
    # Messages with "/"
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))



    # fetches all inputs without "/"
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, user_input_sharer))

    # Error handler
    dispatcher.add_error_handler(error)

    # Let bot fetch for input from telegram
    bot.start_polling()
    bot.idle()


# Was neccessary for scraper main()
#if __name__ == "__main__":
main()









# Skizze decider fun
# if decider(1) == True:
    # Callt send_photo function for specific string (in chat /b)
#     dispatcher.add_handler(CommandHandler(Filters.command & ~Filters.text, photo_sender))

# Send some kind of error signal
# else:
#     print("input is not a stock")

# Message handler
# Filters for text and not command inputs
#dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, message_receiver))

#main()

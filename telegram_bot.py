# Instantiating the bot
from telegram.ext import *
from telegram import Update
# Communication between Telegram Bot and Web Scraper
import messenger
# Wait for other programs to finish
import time
# Change Working directory
import os
# Scrape current stock data
import yfinance as yf




'''
This program is a Telegram bot. When it is started it will keep running and can
receive input from users in the corresponding Telegram chat, as well as send
pictures and messages back to the user.
'''


# Indicate starting
print("let's go")


# Bot token
api = '1974428884:AAHJhCzmng54oBisKoRXWB8i24w5m3vjdz4'


# Save user input
global_input = None




'''
Functions for the bot
'''




def start_command(update, context):
    '''
    Function for the "/start" command.

    ~~~variables~~~
    update: So the function can use data from the chat (chat_id etc.) fetched by start_polling() in main()
    context: Assures all handlers (Message- & Commandhandler in main()) work in the same group
    '''
    update.message.reply_text("I can send you information about the stock market. Just type in current <yahoo finance ticker symbol> for the current stock price. Use simple/regression/detailed for plots with Bitcoin-USD prices from 01.01.2020 to today. Use simple/regression/detailed <yahoo finance ticker symbol> for plots for the according stock. Use simple/regression/detailed <yahoo finance ticker symbol> <year-month-date> for plots for the according stock from your individual starting time up to today. Use simple/regression/detailed <yahoo finance ticker symbol> <year-month-date> <year-month-date> for plots for the according stock from your individual starting time up to your individual ending time. Use close to terminate the scraper running in the background.")




def help_command(update: Update, context: CallbackContext) -> None:
    '''
    Function for the "/help" command.

    ~~~variables~~~
    update: So the function can use data from the chat (chat_id etc.) fetched by start_polling() in main()
    context: Assures all handlers (Message- & Commandhandler in main()) work in the same group
    '''
    update.message.reply_text("How to use the Telegram Bot: For the current stock price write: current <Ticker_symbol> | For the graphs type your requests in the following order: '<type_of_graph> <Ticker_symbol> <start_date> <end_date>' (dates are typed in the form: year-month-day) | To close the scraper in the background (plots will not work before starting the scraper again) type: close | Example commands for the Telegram Bot could be:  'current TCEHY' | 'detailed' | 'simple BTC-USD' | 'regression TCEHY 01.01.2020' | 'detailed TSLA 01.01.2017 01.01.2019'")




def photo_for_querie(update: Update, context: CallbackContext) -> None:
    '''
    Saves user input as global variable. Checks the input for specific keywords
    and either sends the current stock, graphs showing the stocks development or
    an erro to the user.

    ~~~variables~~~
    update: So the function can use data from the chat (chat_id etc.) fetched by start_polling() in main()
    context: Assures all handlers (Message- & Commandhandler in main()) work in the same group
    '''
    # Saves user input as global variable
    global global_input#
    # Transforms it into lowercase string
    global_input = str(update.message.text).lower()

    # Splits string at spaces
    input_split = global_input.split()


    # Prints the current price of a given stock
    if input_split[0] == "current":
        # Scrapes the current stock price from Yahoo Finance
        stock = yf.Ticker(input_split[1])
        price = stock.info['regularMarketPrice']

        #Sends stock price to user
        update.message.reply_text(price)


    # Sends different plots for defined stock and time period (both optional)
    elif input_split[0] == "simple" or input_split[0] == "regression" or input_split[0] == "detailed":
        # Function call to write input into inputs.txt file
        messenger.txt_writer(str(global_input))

        # Stop program until other ones are finished with saving the plot
        time.sleep(6)

        # Fetching users chat id to send the plot (saved in wd) as picture
        chat_id = update.message.chat.id
        update.message.bot.send_photo(chat_id, open("graph.png", "rb"))


    # Input includes more than 4 keywords
    elif len(input_split) > 4:
        update.message.reply_text("I am not capable to take that many arguments. Please try again with less")


    # Input from user matches no keyword. Sends error message to him
    else :
        update.message.reply_text("I am sorry but this is not the right keyword. Type /help to find out about everything I can do for you!")




def error(update, context):
    '''
    Outputs message in console if querie is unmatched so the bot wont crash if
    anything throws an error.

    ~~~variables~~~
    update: So the function can use data from the chat (chat_id etc.) fetched by start_polling() in main()
    context: Assures all handlers (Message- & Commandhandler in main()) work in the same group
    '''
    print("Bot received an unknown input")




def main():
    '''
    Where the magic happens.

    It includes all bot commands to run it:
    - initalizes it
    - all message- / command- handlers to send data to user for different queries
    - Update the bot constantly to check for new user inputs

    '''
    #Initialize bot
    bot = Updater(api, use_context = True)
    dispatcher = bot.dispatcher

    # Command handler
    # Messages with "/"
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # fetches all inputs without "/"
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, photo_for_querie))

    # Error handler
    dispatcher.add_error_handler(error)

    # Let bot fetch for input from telegram
    bot.start_polling()
    bot.idle()




# Checks wether we have a program or library
# Runs the program
if __name__ == "__main__":
    main()

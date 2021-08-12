

def response(user_input):
    '''
    Lists all possible responses the bot gives to specific queries
    '''

    # Format user input as lowercase string
    inp = str(user_input).lower()

    # Anser to "huhu"
    if inp == "huhu":
        return "please leave me alone"


    # Input does not match any response (Error)
    else:
        return "I do not know this querie. Please type /help to see all the things I can do for you"

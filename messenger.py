'''
I send data from bot to scraper and back. Both of them really care about their
indipendence so I take care they do not notice anything from each other.


Personal working directory has to be set!
'''
import os


### Set your current working directory ###
os.chdir("C:/Users/bad42/Desktop/scientificpython")
# Checks for current working directory
print("The current working directory (messenger) is:" + os.getcwd())



def txt_writer(inp):
    '''
    Saves a given string into the inputs.txt file

    ~~~variables~~~
    inp: A string to write (built to receive user input from bot)
    '''
    with open("inputs.txt", "a") as test:
        test.write(inp)
        # Writes a new line after each input
        test.write("\n")

from pathlib import Path
import requests
import csv
import os
import os.path
import scraper_with_all_graphs


### Set your current working directory ###
os.chdir("C:/Users/bad42/Desktop/final_project")
# Checks for current working directory
print("The current working directory (scraper) is:" + os.getcwd())

# Showing the prgram has started
print("Scanning text file...")


global size
size = 0
global size2
size2 = Path("inputs.txt").stat().st_size

while(True):
    """
    Endless loop which constantly checks for new input in the txt file, which is written by the Telegram bot.
    When a user gives input the file size changes and the if statement will be called. The lines of the file
    will be read in as a list and depending on the input the corresponding function will be called and the
    right plot will be saved in the folder in which our program resides.
    """
    size = size2
    size2 = Path("inputs.txt").stat().st_size

    # if the size of the file changes, the txt file is read and a function is called with its last entry
    if size != size2:
        lis = list(csv.reader(open('inputs.txt')))
    # To make sure our index is not out of bounds with the first entry
        if len(lis) == 1:
            last_line = lis[0]
            last_line = str(last_line[0])
            last_line_list = last_line.split()
        else:
            last_line = lis[len(lis)-1]
            last_line = str(last_line[0])
            last_line_list = last_line.split()
        # Checking for the first word and choose the correspoinding plot
        # It is possible to call it with just the keyword for the plot, the keyword and ticker symbol,
        # the keyword, ticker symbol, start of time period or with the keyword, ticker symbol, start and end of time period.
        # missing values will be substituted with the standart values (ticker = BTC-USD, start period = 2020-01-01, end period = today)
        if last_line_list[0] == "simple":
            if len(last_line_list) == 1:
                scraper_with_all_graphs.simple()
            if len(last_line_list) == 2:
                scraper_with_all_graphs.simple(t=last_line_list[1])
            if len(last_line_list) == 3:
                scraper_with_all_graphs.simple(t=last_line_list[1], p1=last_line_list[2])
            if len(last_line_list) == 4:
                scraper_with_all_graphs.simple(t=last_line_list[1], p1=last_line_list[2], p2=last_line_list[3])

        elif last_line_list[0] == "regression":
            if len(last_line_list) == 1:
                scraper_with_all_graphs.regression()
            if len(last_line_list) == 2:
                scraper_with_all_graphs.regression(t=last_line_list[1])
            if len(last_line_list) == 3:
                scraper_with_all_graphs.regression(t=last_line_list[1], p1=last_line_list[2])
            if len(last_line_list) == 4:
                scraper_with_all_graphs.regression(t=last_line_list[1], p1=last_line_list[2], p2=last_line_list[3])

        elif last_line_list[0] == "detailed":
            if len(last_line_list) == 1:
                scraper_with_all_graphs.full_graph()
            if len(last_line_list) == 2:
                scraper_with_all_graphs.full_graph(t=last_line_list[1])
            if len(last_line_list) == 3:
                scraper_with_all_graphs.full_graph(t=last_line_list[1], p1=last_line_list[2])
            if len(last_line_list) == 4:
                scraper_with_all_graphs.full_graph(t=last_line_list[1], p1=last_line_list[2], p2=last_line_list[3])
        # with the word "close" we can terminate our scraper
        elif last_line_list[0] == "close":
            exit()

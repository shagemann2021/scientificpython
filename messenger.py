'''
I send data from bot to scraper and back. Both of them really care about their
indipendence so I take care they do not notice anything from each other
'''

def txt_writer(inp):
    with open("tester.txt", "a") as test:
        test.write(inp)
        test.write("\n")

import json
import random

class Quote:
    def __init__(self, name):
        self.name = name
        self.author = ""

    def print_quote(self) -> None:
        print("Quote: ", self.name)
        print("Quote Author: ", self.author)

class QuoteDatabase:
    quote_of_the_day = ""
    quote_dictionary = []
    quote_count = 0

    def __init__(self, file: str):
        with open(file) as f:
            database = json.load(f)
        print("Retrieving Quotes from", file, "- date created: ", database['date_created'])

        for quote in database['quote_list']:
            tempquote = Quote(quote['quote'])
            tempquote.author = quote['author']

            self.quote_count += 1
            self.quote_dictionary.append(tempquote)

        self.GetRandomQuote()

    """ Prints Exercises in Exercise Dictionary """
    def print_exercise(self):
        for quote in self.quote_dictionary:
            quote.print_quote()

    def GetRandomQuote(self) -> None:
        self.quote_of_the_day = random.choice(QuoteDatabase.quote_dictionary)

    def GetQOTD(self) -> str:
        return "Quote Of The Day\n\n" + self.quote_of_the_day.name + "\n     - " + self.quote_of_the_day.author

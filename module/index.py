'''
FOREX Transactions
'''
import csv
import os
import click
import pycountry

class FileError(Exception):
    '''
    Exception for errors due too currency pairs or codes
    '''
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class TransactionOrder:
    '''
    Common base class for all transaction orders
    '''
    def __init__(self, data):
        self.order = {}
        self.order["id"] = int(data[0])
        self.order["account"] = data[1]
        self.order["pair"] = data[2]
        self.order["action"] = data[3]
        self.order["price"] = float(data[4])
        self.order["match"] = False

    @staticmethod
    def are_already_matched(match, other_match):
        '''
        Check if one of the orders has already found a match
        '''
        if (match is False or match == 'REJECTED') and\
           (other_match is False or other_match == 'REJECTED'):
            return False
        return True

    @staticmethod
    def are_compatible_orders(action, other_action):
        '''
        Check if the order is known
        '''
        if action and other_action in ('BUY', 'SELL') and\
           action != other_action:
            return True
        return False

    @staticmethod
    def are_different_accounts(account_1, account_2):
        '''
        Check if transaction actors are a different person
        '''
        if account_1 != account_2:
            return True
        return False

    @staticmethod
    def are_same_currency_pairs(currency_pair_1, currency_pair_2):
        '''
        Check if they want to trade the exact same currency pairs
        '''
        if currency_pair_1 == currency_pair_2:
            return True
        return False

    def are_prices_compatible(self, other):
        '''
        Check if the prices set are compatible
        '''
        if self.order["action"] in 'BUY' and\
           self.order["price"] >= other.order["price"]:
            return True
        elif other.order["action"] in 'BUY' and\
             other.order["price"] >= self.order["price"]:
            return True
        else:
            return False

    def execute_order(self, other):
        '''
        If all conditions are respected for the trade, execute it
        '''
        if self.are_same_currency_pairs(self.order["pair"], other.order["pair"]) and\
           self.are_different_accounts(self.order["account"], other.order["account"]) and\
           self.are_prices_compatible(other) and\
           self.are_compatible_orders(self.order["action"], other.order["action"]) and\
           not self.are_already_matched(self.order["match"], other.order["match"]):
            self.order["match"] = other.order["id"]
            other.order["match"] = self.order["id"]

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.order["id"], self.order["account"],\
                                                    self.order["pair"], self.order["action"],\
                                                    self.order["price"], self.order["match"])

def create_csv(matches):
    '''
    Create a new CSV file containing orders status
    '''
    with open('matches.csv', mode='w') as csvfile:
        categories = ["id", "account", "pair", "action", "price", "match"]
        writer = csv.DictWriter(csvfile, fieldnames=categories)
        try:
            writer.writeheader()
            for item in matches:
                writer.writerow(item.order)
        except csv.Error as error:
            print("Unable to write data inside the CSV file.\n{}".format(error))
        finally:
            del writer

def match_orders(orders):
    '''
    Match or Reject orders
    '''
    position = 0
    while position < len(orders):
        index = -1
        while index < len(orders) - 1:
            orders[position].execute_order(orders[index + 1])
            index = index + 1
        if isinstance(orders[position].order["match"], bool) and\
           not orders[position].order["match"]:
            orders[position].order["match"] = 'REJECTED'
        position = position + 1
    return orders

def is_not_categories(row):
    '''
    Check if the row is not the initial row composed of categories
    '''
    try:
        categories = ["id", "account", "pair", "action", "price"]
        for item in row:
            if item in categories:
                return False
    except IndexError as error:
        print("Unable to parse row inside the csv file.\n{}".format(error))
    return True

def store_orders(file):
    '''
    Store order of each account in a list of Class instances
    '''
    orders = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        try:
            for row in reader:
                row = clean_row(row)
                if is_not_categories(row):
                    orders.append(TransactionOrder(row))
        except csv.Error as error:
            print("Unable to get orders stored inside the CSV file.\n{}".format(error))
            return None
        finally:
            del reader
    return orders

def is_currency_code(currency_codes):
    '''
    Recover the official list of currency code and then check if the currency codes are correct
    '''
    currency_code_list = []
    for item in list(pycountry.currencies):
        currency_code_list.append(str(item).split(',')[0][-4:-1])
    try:
        for currency_code in currency_codes:
            if currency_code not in currency_code_list:
                raise FileError("Insert correct currency codes inside your csv file please.")
    except FileError as error:
        print(error)
        return False
    except IndexError as error:
        print(error)
        return False
    return True

def find_currency_pair(currency_pair):
    '''
    Find the currency pair, split it into a list of currency codes and then passed it as parameter
    '''
    if currency_pair == 'pair':
        return True
    try:
        slash = currency_pair.find('/')
        if slash == -1:
            raise FileError("Insert correct currency pairs inside your csv file please.")
        currency_codes = currency_pair.split('/')
    except FileError as error:
        print(error)
        return False
    return is_currency_code(currency_codes)

def clean_row(row):
    '''
    Clean each row of any whitespace
    '''
    new_row = []
    try:
        for item in row:
            item = item.strip()
            if len(item) == 0:
                raise FileError("One currency pair is empty inside your csv.")
            new_row.append(item)
    except FileError as error:
        print(error)
        return False
    finally:
        del row
    return new_row

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv') or os.path.getsize(file) <= 0:
        print("Insert a correct CSV file please.")
        return False
    with open(file, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        try:
            for row in reader:
                row = clean_row(row)
                if not row or not find_currency_pair(row[2]):
                    return False
        except csv.Error as error:
            print(error)
            return False
        finally:
            del reader
    return True

@click.group()
def cli():
    '''
    Python Script which match buy and sell orders of individual currency pairs
    '''

@cli.command('trade')
@click.argument('file', type=click.Path(exists=True))
def trade_currencies(file):
    '''
    Execute trade orders when prices match or reject them
    '''
    if is_csv(file):
        orders = store_orders(file)
        matches = match_orders(orders)
        create_csv(matches)
        del matches

if  __name__ == '__main__':
    cli()

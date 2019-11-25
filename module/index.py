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
    def __init__(self, id, account, pair, action, price):
        self.id = int(id)
        self.account = account
        self.pair = pair
        self.action = action
        self.price = float(price)

    def __eq__(self, other):
        return (self.id, self.account) == (other.dominant, other.quote)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.id, self.account, self.pair, self.action, self.price)

    def __del__(self):
        return

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

def is_not_categories(row):
    '''
    Check if the row is not the initial row composed of categories
    '''
    try:
        for item in row:
            if item == 'id':
                return False
            else:
                continue
    except:
        print("Unable to parse row inside the csv file.")
    return True

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

def store_orders(file):
    '''
    Store order of each account in a Class instance
    '''
    orders = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = clean_row(row)
            if is_not_categories(row):
                orders.append(TransactionOrder(row[0], row[1], row[2], row[3], row[4]))
    return orders

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv') or os.path.getsize(file) <= 0:
        print("Insert a correct CSV file please.")
        return False
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            row = clean_row(row)
            if not row or not find_currency_pair(row[2]):
                return False
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
        for item in orders:
            print(item)
    return orders

if  __name__ == '__main__':
    cli()

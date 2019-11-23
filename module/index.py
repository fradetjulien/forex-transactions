import csv
import click
import pycountry

class CurrencyPairs:
    '''
    Common base class for all orders
    '''
    def __init__(self, dominant, quote):
        self.dominant = dominant
        self.quote = quote

    def __eq__(self, other):
        return (self.dominant, self.quote) == (other.dominant, other.quote)

    def __str__(self):
        return 'Here will be displayed all result orders.'

    def __del__(self):
        return

def is_currency_code(currency_codes):
    '''
    Recover the official list of currency code and then check if the currency codes are correct
    '''
    currency_code_list = []
    for item in list(pycountry.currencies):
        currency_code_list.append(str(item).split(',')[0][-4:-1])
    for currency_code in currency_codes:
        if currency_code not in currency_code_list:
            print("Insert correct currency codes inside your csv file please.")
            return False
    return True

def find_currency_pair(currency_pair):
    '''
    Find the currency pair, split it into a list of currency codes and then passed it as parameter
    '''
    if currency_pair == 'pair':
        return True
    else:
        try:
            currency_codes = currency_pair.split('/')
            return is_currency_code(currency_codes)
        except:
            print("Insert correct currency codes inside your csv file please.")
    return False

def clean_row(row):
    '''
    Clean each row of any whitespace
    '''
    new_row = []
    for item in row:
        item = item.strip()
        new_row.append(item)
    del row
    return new_row

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv'):
        print("Insert a correct CSV file please.")
        return False
    try:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONE)
            for row in reader:
                row = clean_row(row)
                if not find_currency_pair(row[2]):
                    return False
            return True
    except:
        print("Insert a correct CSV file please.")
        return False

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
        matches = CurrencyPairs('USD', 'EUR')
        return matches
    return None

if  __name__ == '__main__':
    cli()

import csv
import click

class CurrencyPairs:
    '''
    Common base class for all orders
    '''
    def __init__(self, dominant, quote):
        self.dominant = dominant
        self.quote = quote

    def __eq__(self, other):
        return ((self.dominant, self.quote) == (other.dominant, other.quote))

    def __str__(self):
        return 'Here will be displayed all result orders.'

    def __del__(self):
        return

def is_csv(file):
    '''
    Check if the file received in parameter is a correct CSV file
    '''
    if not file.endswith('.csv'):
        print("Insert a correct CSV file please.")
        return False
    try:
        with open(file, newline='') as csvfile:
            csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
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

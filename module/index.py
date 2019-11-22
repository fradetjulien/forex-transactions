import click
import csv

def init_data():
    '''
    '''
    data = {
    }
    return data

def read_data(file):
    '''
    '''
    data = init_data()
    return data

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

    '''

@cli.command('trade')
@click.argument('file', type=click.Path(exists=True))
def trade_currencies(file):
    '''
    Execute trade orders when it's possible and reject it when it's impossible
    '''
    if is_csv(file):
        data = read_data(file)
        return data

if  __name__ == '__main__':
    cli()
import csv
import re
import argparse

def query_data(filename, queries):
    '''
    Uses a csv_reader to parse each row of the

    :param filename: the filename of the csv datafile
    :param queries: a list of queries that is used to find matching entries
    *This will be replaced when moving to DB
    '''

    # Translates the original query list to a set of lowercase values
    queries = format_list(queries)
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            sanitized_row = format_list(row)
            intersection = sanitized_row.intersection(queries)
            # True when the row has all the values in the query
            if intersection == queries:
                yield row

def format_list(entry_list):
    '''
    Returns a formatted copy of a list. Will split each list by spaces,
    remove any non-alphanumeric characters, and shifts them to lowercase.

    :param entry_list: List that may have non-alphanumeric and inconsistent capitalization
    :return: the formatted entry_list
    '''
    formatted_set = set()
    if not entry_list:
        return formatted_set

    for entry in entry_list:
        entry = re.sub('[^0-9a-zA-Z\s]+', '', entry)
        entry = entry.lower().strip()
        if ' ' in entry:
            address = entry.split()
            for word in address:
                formatted_set.add(word)
        else:
            formatted_set.add(entry)

    return formatted_set


def create_parser():
    '''
    Creates a argument parser to handle cli input.

    If moving to a external database, this can be expanded to include flags that handle
    label the input from the user. Labeled input can be used to write DB queries.

    :return: a parser object
    '''
    app_description = 'Searches a csv address book for the query given.'
    parser = argparse.ArgumentParser(description=app_description)

    parser.add_argument('query', nargs='+',
                        help='argument that takes a string of varying length \
                        and searches the address book with it')
    parser.add_argument('-f', '--filename', dest='filename', nargs=1,
                        help='the filename of the address book csv. Default: ./%(default)s',
                        default='data.csv')

    return parser

if __name__ == '__main__':
    # parse
    parser = create_parser()
    user_input = parser.parse_args()

    # search
    filename = user_input.filename[0]
    query_string = user_input.query

    found = False
    for matching_entry in query_data(filename, query_string):
        if matching_entry:
            found = True
        print(' '.join(matching_entry))

    if not found:
        print('Not in address book')

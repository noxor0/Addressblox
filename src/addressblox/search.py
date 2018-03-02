import csv
import re
import argparse
import sys

from addressblox.constants import ABBREVIATION_DICT

def query_data(filename, queries):
    '''
    Uses a csv_reader to parse each row of the CSV file, and returns matching entries.

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

def handle_abbreviations(entry_set):
    '''
    Allows for queries to recognize abreviations as well during query look ups.
    Expands all abbreviations to their long form equivalent.

    St and Street are the same thing, thus a query to for either one should
    return the other as well.

    :params entry_set: the set to be modified.
    '''
    for item in entry_set:
        if item in ABBREVIATION_DICT:
            entry_set.add(ABBREVIATION_DICT[item])
            entry_set.remove(item)

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
    handle_abbreviations(formatted_set)

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

    parser.add_argument('query', nargs='*', default='',
                        help='argument that takes a string of varying length \
                        and searches the address book with it')
    parser.add_argument('-f', '--filename', dest='filename',
                        help='the filename of the address book csv. Default: ./%(default)s',
                        default='data/data.csv')
    parser.add_argument('-i', '--interactive', dest='interactive', action='store_true',
                        help='Runs the application in interactive mode, and allows\
                        multiple queries until user types "quit"')
    return parser

def search_for_query(user_input, interactive_query=None):
    '''
    Handles logic for taking user input and passing it into the query function.

    :params user_input: namespace that has the pased user input. This contains
    the query, the filename, and if the program is to be run in interactive mode.
    '''
    filename = user_input.filename
    # query_string = None
    if interactive_query:
        query_string = interactive_query
    else:
        query_string = user_input.query

    found = False
    try:
        metrics = 0
        for matching_entry in query_data(filename, query_string):
            if matching_entry and not found:
                print('--------------', '\nFound:')
                found = True
            metrics += 1
            print(' '.join(matching_entry))
        # Metrics are important.
        print('Total entries found: {}'.format(metrics))
    except FileNotFoundError:
        error_string = ('File {} not found, please check that it exists in the '
              'directory and try again').format(filename)
        print(error_string)
        sys.exit(0)

    if not found:
        print('Not in address book')

def interactive_mode(user_input):
    '''
    Creates a constant loop that allows the user to run multiple different queries
    without having to restart the program.

    Works best when run with docker container.

    :params user_input: namespace that has the pased user input. This contains
    the query, the filename, and if the program is to be run in interactive mode.
    '''
    interactive_text =('Type the name, address, or age of the person you want to look up\n'
                      'Blank query will return all entries\n'
                      '> ')
    try:
        interactive_query = None
        while interactive_query != ['quit']:
            interactive_query = input(interactive_text).split()
            search_for_query(user_input, interactive_query)
            print()
    except KeyboardInterrupt:
        print()
        print("Cancelled by keyboard")
        sys.exit(0)

def main():
    # parse
    parser = create_parser()
    user_input = parser.parse_args()

    if user_input.interactive:
        interactive_mode(user_input)
        sys.exit(0)
    else:
        search_for_query(user_input)
        sys.exit(0)

if __name__ == '__main__':
    main()

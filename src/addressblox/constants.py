''' Holds constants used in the program for simple modification '''
ABBREVIATION_DICT = {
    'st' : 'street',
    'ave' : 'avenue',
    'blvd' : 'boulevard',
    'rd' : 'road',
    'dr' : 'drive',
    'hwy' : 'dighway',
    'pike' : 'pk',
    'parkway' : 'pkwy',
    'ln' : 'lane',
}

DEFAULT_DATA_PATH = 'data/data.csv'

REGEX_ALPHANUMERIC = r'[^0-9a-zA-Z\s]+'
REGEX_ALPHANUMERIC_PERIOD = r'[^0-9a-zA-Z\s.]+'

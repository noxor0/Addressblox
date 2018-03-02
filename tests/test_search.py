import unittest
from unittest.mock import patch

from contextlib import contextmanager
from io import StringIO
import sys

from addressblox import search

class Namespace:
    '''
    Just used to emulate the parse_args() return value
    '''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@contextmanager
def captured_output():
    '''
    Really clever way to handle checking stdout that I hadnt thought of.
    https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
    '''
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.user_input_namespace = Namespace(query=['Dave', '123'],
                                        filename='data/data.csv',
                                        interactive='False')

    def test_handle_abbreviations(self):
        actual = set(['st', 'ave', 'blvd', 'ln'])
        search.handle_abbreviations(actual)
        expected = set(['street', 'avenue', 'boulevard', 'lane'])
        self.assertEqual(actual, expected)


    def test_search_for_query(self):
        expected = 'Dave Smith 123 main st. seattle wa 43'
        with captured_output() as (out, err):
            search.search_for_query(self.user_input_namespace)
            actual = out.getvalue().strip()
            self.assertIn(expected, actual)

    @patch.object(search, "input", create=True)
    def test_interactive_mode(self, input):
        expected = 'Total entries found: 0'
        with captured_output() as (out, err):
            # Yeah i cannot believe that worked
            values = ['not in there', 'quit']
            input.return_value = values.pop()
            search.interactive_mode(self.user_input_namespace)
            actual = out.getvalue().strip()
            self.assertIn(expected, actual)

    def test_query_data(self):
        expected = '"Dave","Smith","123 main st.","seattle","wa","43"'
        query_generator = search.query_data(self.user_input_namespace.filename,
                                            self.user_input_namespace.query)
        for return_val in query_generator:
            self.assertEqual(expected, expected)


    def test_multiple_query_data(self):
        expected = ['"Dave","Smith","123 main st.","seattle","wa","43"',
                    '"Alice","Smith","123 Main St.","Seattle","WA","45"',
                    '"Ian","smith","123 main st ","Seattle","Wa","18"',
                    '"EvE","Smith","234 2nd Ave.","Tacoma","WA","25"',
                    '"Jane","Smith","123 Main St.","Seattle","WA","13"',
                ]

        query_generator = search.query_data(self.user_input_namespace.filename,
                                            'smith')
        for return_val in query_generator:
            self.assertIn(return_val, expected)

    def test_multiple_query_data_2(self):
        expected = ['“bOb","Williams","234 2nd Ave.","Tacoma","WA","26"',
                    '"Carol","Johnson","234 2nd Ave","Seattle","WA","67"',
                    '"EvE","Smith","234 2nd Ave.","Tacoma","WA","25"',
                    '"Frank","Jones","234 2nd Ave.","Tacoma","FL","23"'
                ]

        query_generator = search.query_data(self.user_input_namespace.filename,
                                            'avenue')
        for return_val in query_generator:
            self.assertIn(return_val, expected)

    def test_not_query_data(self):
        expected = []
        query_generator = search.query_data(self.user_input_namespace.filename,
                                            'connor')
        for return_val in query_generator:
            self.assertEqual(expected, return_val)

    def test_format_list(self):
        unformatted_list = ['H..e][l,<l{}o]', 'W0RL.D    ', '69 st, ,nam.e', 'CATS!', 'test', '69']
        actual = search.format_list(unformatted_list)
        expected = set(['hello', 'w0rld', '69', 'street', 'name', 'cats', 'test', '69'])
        self.assertEqual(expected, actual)

    def test_no_file_search(self):
        self.user_input_namespace.filename = 'not_here.vsc'
        with self.assertRaises(SystemExit):
            search.search_for_query(self.user_input_namespace)

    def test_create_parser(self):
        self.assertIsNotNone(search.create_parser())

    def test_main(self):
        with self.assertRaises(SystemExit):
            search.main()

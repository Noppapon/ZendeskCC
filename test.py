import unittest
from Main import main, menu
import sys
from contextlib import contextmanager
from io import StringIO

class TestSum(unittest.TestCase):

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_auth_error(self):
        with captured_output() as (out, err):
            main('zccwrongsubdomain', 'wrongemail', 'wrong password')
        output = out.getvalue().strip()
        self.assertEqual(output, "Authentication failed, terminating the program...\n")

    def test_auth_success(self):
        with captured_output() as (out, err):
            main('zcccorrectsubdomain', 'correctmail', 'correct password')
        output = out.getvalue().strip()
        self.assertEqual(output, "Success!\n")

if __name__ == '__main__':
    unittest.main()

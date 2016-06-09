import unittest
import os

import sys
from app.translate import execute

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())

FILE_PATH = "{}/app/strings.xml".format(os.getcwd())


class TestSuite(unittest.TestCase):
    def test_A(self):
        execute(FILE_PATH)

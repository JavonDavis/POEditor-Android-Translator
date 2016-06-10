import unittest
import os

import sys
from app.translate import execute,build_xml

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.getcwd())

FILE_PATH = "{}/app/strings.xml".format(os.getcwd())
NAME_PATH = "{}/names.csv".format(os.getcwd())
VALUES_PATH = "{}/translation.csv".format(os.getcwd())


class TestSuite(unittest.TestCase):
    def test_a_translate(self):
        execute(FILE_PATH)

    def test_b_build_xml(self):
        build_xml(NAME_PATH, VALUES_PATH)

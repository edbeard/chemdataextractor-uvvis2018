# -*- coding: utf-8 -*-
"""
chemdataextractor.tests.parse_tests.test_table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from unittest import TestCase
from chemdataextractor.parse.table import UvvisAbsHeadingParser
from chemdataextractor.doc.table import Cell, Table

class TestUvvisAbsHeadingParser(TestCase):
    ''''''
    def test_UvvisAbsHeadingParser_basic(self):
        '''Simple test case'''
        testHeading =  [('λ', 'NN'), ('abs','NN')]
        parser = UvvisAbsHeadingParser()
        result = list(parser.parse(testHeading))
        print(result)
        if result:
            exists = True
        else:
            exists=False

        self.assertTrue(exists)


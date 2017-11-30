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
    def test_UvvisAbsHeadingParser_all_uvvis_abs_title(self):
        '''Simple cases present in uvvis_abs_title field'''

        testHeadings =  [[('λ', 'NN'), ('abs','NN')],
                        [('absorption', 'NN'), ('maxima', 'NN')],
                         [('λ', 'NN'), ('solmax', 'NN')],
                         [('uv', 'NN'), ('/','NN'), ('vis')]]
        parser = UvvisAbsHeadingParser()
        failed=False
        for testHeading in testHeadings:
            result = list(parser.parse(testHeading))
            print(result)
            if not result:
                failed=True
        self.assertFalse(failed)

    def test_UvvisAbsHeadingParser_all_uvvis_units(self):
        '''Simple test cases for uvvis_units'''

        testHeadings = [[('λ', 'NN'), ('abs','NN'), ('nm', 'NN')],
                        ]
        parser = UvvisAbsHeadingParser()
        failed=False
        for testHeading in testHeadings:
            result =list(parser.parse(testHeading))
            print(result[0].serialize()['uvvis_spectra'][0]['peaks'])
            try:
                if result[0].serialize()['uvvis_spectra'][0]['peaks'][0]['units'] != 'nm':
                    failed=True
            except:
                failed=True

        self.assertFalse(failed)







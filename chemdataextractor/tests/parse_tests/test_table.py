# -*- coding: utf-8 -*-
"""
chemdataextractor.tests.parse_tests.test_table
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from unittest import TestCase
from chemdataextractor.parse.table import UvvisAbsHeadingParser, uvvis_abs_title, uvvis_units, uvvis_abs_heading, \
uvvis_value
from chemdataextractor.parse.common import delim
from chemdataextractor.parse.elements import Optional
from chemdataextractor.parse.base import BaseParser
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
            try:
                if result[0].serialize()['uvvis_spectra'][0]['peaks'][0]['units'] != 'nm':
                    failed=True
            except:
                failed=True

        self.assertFalse(failed)


class Test_uvvis_abs_title(TestCase):
    '''Testing uvvis_abs_title BaseParserObject directly'''
    #NOTE: Use this format for all 'flagging' parsers (ie not picking up a particular value

    def test_uvvis_abs_title_passes(self):
        tagged_tokens = [[('λ', 'NN'), ('abs','NN')],
                         [('absorption', 'NN'), ('maxima', 'NN')],
                         [('λ', 'NN'), ('solmax', 'NN')],
                         [('uv', 'NN'), ('/','NN'), ('vis')]]
        failed = False
        for tokens in tagged_tokens:
            result = uvvis_abs_title.scan(tokens)
            resultNumber = len(list(*result))
            print(resultNumber)
            if resultNumber == 0:
                failed=True

        self.assertFalse(failed)

class Test_uvvis_units(TestCase):
    '''Testing uvvis_units BaseParserObject directly'''
    def test_uvvis_units_passes(self):
        tagged_tokens = [[('nm', 'NN')],
                         [('eV-1', 'NN')]]
        failed = False
        for tokens in tagged_tokens:
            result = uvvis_units.scan(tokens)
            uvvis_obj = list(*result)
            if uvvis_obj == []:
                failed=True
            #TODO: Could add this to check for specific unit types (ie 'nm' and 'eV')
            units =uvvis_obj[0].xpath('./text()')[0]
            print(units)
            if units != 'nm' and units != 'eV-1':
               failed=True
           # unitsNumber = len(unit)
           # if unitsNumber == 0:
               # failed = True
        self.assertFalse(failed)

class Test_uvvis_abs_heading(TestCase):
    '''Testing the overall uvvis_abs_heading'''

    def test_uvvis_abs_heading(self):
        tagged_tokens = [[('λ', 'NN'), ('abs','NN'), ('nm', 'NN')],
                         [('λ', 'NN'), ('abs','NN'), ('eV-1', 'NN')]]
        failed = False
        for tokens in tagged_tokens:
            result = uvvis_abs_heading.scan(tokens)
            uvvis_obj = list(*result)
            if uvvis_obj == []:
                failed=True

        self.assertFalse(failed)

class Test_uvvis_value(TestCase):
    '''Testing the uvvis value identifier, including cases of multiple values and false cells around true value'''

    def test_uvvis_values(self):
        tagged_tokens = [[('345', 'CD')],
                         [('242.37', 'CD'), ('1234','CD')],
                         [('cellfail', 'NN'), ('678', 'NN')]
                         ]
        failed=False
        multiple_values = uvvis_value + Optional(uvvis_value)
        for tokens in tagged_tokens:
            results = multiple_values.scan(tokens)
            uvvis_obj = list(*results)
            print(uvvis_obj)
            if uvvis_obj == []:
                failed=True
        self.assertFalse(failed)

    def test_uvvis_values_peakwidth(self):
        #Checking the peak width works
        tokens = [[('345sh', 'CD')], [('345br', 'CD')]]
        failed=False
        for token in tokens:
            result = uvvis_value.scan(token)
            uvvis_obj = list(*result)
            if uvvis_obj[0][1].xpath('./text()')[0] != 'sh' and uvvis_obj[0][1].xpath('./text()')[0] != 'br':
                failed=True
        self.assertFalse(failed)






# -*- coding: utf-8 -*-
"""
test_parse_table
~~~~~~~~~~~~~~~~

Test table parser

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from lxml import etree

from chemdataextractor.doc.table import Cell
from chemdataextractor.parse.table import UvvisAbsHeadingParser, UvvisAbsCellParser, ExtinctionCellParser, ExtinctionHeadingParser


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestParseTableUvvisAbsHeading(unittest.TestCase):
    """ Test parsing of uvvis abs headings"""

    def do_parse(self, input, expected):
        h = Cell(input)
        log.debug(h)
        log.debug(h.tagged_tokens)
        result = next(UvvisAbsHeadingParser().root.scan(h.tagged_tokens))[0]
        log.debug(etree.tostring(result, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

    def test_just_heading(self):
        expected = '<uvvis_abs_heading/>'
        self.do_parse('λ abs', expected)
        self.do_parse('absorption maxima', expected)
        self.do_parse('λ solmax', expected)
        self.do_parse('uv/vis', expected)

    def test_heading_with_units(self):
        expected = '<uvvis_abs_heading><uvvis_units>nm</uvvis_units></uvvis_abs_heading>'
        self.do_parse('λ abs nm', expected)

    def test_just_units(self):
        self.do_parse('λmax [cm-1]', '<uvvis_abs_heading><uvvis_units>cm-1</uvvis_units></uvvis_abs_heading>')

    def test_excitation_spectra_disallowed_ex(self):
        h = Cell('λex')
        output = list(UvvisAbsHeadingParser().root.scan(h.tagged_tokens))
        self.assertEqual(output, [])

    def test_excitation_spectra_disallowed_exc(self):
        h = Cell('λ exc')
        output = list(UvvisAbsHeadingParser().root.scan(h.tagged_tokens))
        self.assertEqual(output, [])

class TestParseTableUvvisAbs(unittest.TestCase):
    """ Test parsing of uvvis abs values"""

    def do_parse(self, input, expected):
        c = Cell(input)
        log.debug(c)
        log.debug(c.tagged_tokens)
        result = next(UvvisAbsCellParser().root.scan(c.tagged_tokens))[0]
        log.debug(etree.tostring(result, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

    def test_just_value(self):
        self.do_parse('345', '<uvvis_abs_cell><uvvis_abs_peak><value>345</value></uvvis_abs_peak></uvvis_abs_cell>')
        self.do_parse('123 nm', '<uvvis_abs_cell><uvvis_abs_peak><value>123</value></uvvis_abs_peak></uvvis_abs_cell>')
        self.do_parse('22 676', '<uvvis_abs_cell><uvvis_abs_peak><value>22676</value></uvvis_abs_peak></uvvis_abs_cell>')



class TestParseTableExtinctionCell(unittest.TestCase):
    """ Testing parsing of extinction coefficients"""

    def do_parse(self, input, expected):
        c = Cell(input)
        log.debug(c)
        log.debug(c.tagged_tokens)
        result = next(ExtinctionCellParser().root.scan(c.tagged_tokens))[0]
        log.debug(etree.tostring(result, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

    def test_extinction_6_digits(self):
        self.do_parse('102000', '<extinction_cell><extinction>102000</extinction></extinction_cell>')

    def test_extinction_value_with_multiplier(self):
        self.do_parse('2.2×10 4', '<extinction_cell><extinction>2.2×104</extinction></extinction_cell>' )

class TestParseTableExtinctionHeading(unittest.TestCase):
    """ Testing parsing of extinction coefficient heading"""

    def do_parse(self, input, expected):
        c = Cell(input)
        log.debug(c)
        log.debug(c.tagged_tokens)
        result = next(ExtinctionHeadingParser().root.scan(c.tagged_tokens))[0]
        log.debug(etree.tostring(result, encoding='unicode'))
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

    def test_just_heading(self):
        expected = '<extinction_heading/>'
        self.do_parse('ε', expected)
        self.do_parse('ε max', expected)

    def test_extinction_units(self):
        self.do_parse('ε (M -1 cm -1) ', '<extinction_heading><extinction_units>M-1cm-1</extinction_units></extinction_heading>')
        self.do_parse('ε (mM -1 cm -1)', '<extinction_heading><extinction_units>mM-1cm-1</extinction_units></extinction_heading>')
        self.do_parse('ε ( L M -1 cm -1)', '<extinction_heading><extinction_units>LM-1cm-1</extinction_units></extinction_heading>')

if __name__ == '__main__':
    unittest.main()

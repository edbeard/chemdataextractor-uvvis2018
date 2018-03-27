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
from chemdataextractor.parse.table import UvvisAbsHeadingParser, UvvisAbsCellParser


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

class TestParseTableUvvisAbsValue(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()

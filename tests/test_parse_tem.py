# -*- coding: utf-8 -*-
"""
test_parse_tem
~~~~~~~~~~~~~



"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from lxml import etree

from chemdataextractor.doc.text import Sentence
from chemdataextractor.parse.microscopy import TemParser

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestParseTem(unittest.TestCase):

    def do_parse(self, input, expected):
        s = Sentence(input)
        log.debug(s)
        log.debug(s.tagged_tokens)
        result = [ c.serialize() for c in TemParser().parse(s.tagged_tokens)]
        if len(result) == 0:
            result = ['']
        self.assertEqual(expected, result[0])

    def test_tem1(self):
        s = 'electron micrograph'
        expected = {'microscopy': ['tem']}
        self.do_parse(s,expected)

    def test_tem2(self):
        s = 'Transmission electron microscopy'
        expected = {'microscopy': ['tem']}
        self.do_parse(s, expected)

    def test_tem3(self):
        s = 'fail'
        expected = ''
        self.do_parse(s, expected)

    def test_tem4(self):
        s = 'TEM was performed here to...'
        expected = {'microscopy': ['tem']}
        self.do_parse(s,expected)

    def test_tem5(self):
        s = 'Electron micrographs'
        expected = {'microscopy': ['tem']}
        self.do_parse(s,expected)

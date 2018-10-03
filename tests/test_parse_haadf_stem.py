# -*- coding: utf-8 -*-
"""
test_parse_haadf_stem
~~~~~~~~~~~~~

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from chemdataextractor.doc.text import Sentence
from chemdataextractor.parse.microscopy import HaadfStemParser

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestParseHaadfStem(unittest.TestCase):

    def do_parse(self, input, expected):
        s = Sentence(input)
        log.debug(s)
        log.debug(s.tagged_tokens)
        result = [ c.serialize() for c in HaadfStemParser().parse(s.tagged_tokens)]
        if len(result) == 0:
            result = ['']
        self.assertEqual(expected, result[0])

    def test_haadf_stem1(self):
        s = 'HAADF-STEM'
        expected = {'microscopy': ['haadf_stem']}
        self.do_parse(s,expected)

    def test_haadf_stem2(self):
        s = 'HAADF)STEM'
        expected = ''
        self.do_parse(s, expected)

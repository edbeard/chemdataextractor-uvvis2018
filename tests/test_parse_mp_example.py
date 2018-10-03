# -*- coding: utf-8 -*-
"""
test_parse_haadf_stem
~~~~~~~~~~~~~

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from lxml import etree

from chemdataextractor.doc.text import Sentence
from chemdataextractor.parse.mp import mp_phrase

class TestParseMp(unittest.TestCase):

    def test_mp1(self):

        # Declaration
        s = Sentence('Colorless solid (81% yield, 74.8 mg, 0.22 mmol); mp 77.2–77.5 °C.')
        expected = '<mp_phrase><mp><value>77.2–77.5</value><units>°C</units></mp></mp_phrase>'

        # Testing
        result = next(mp_phrase.scan(s.tagged_tokens))[0]

        #Assertion
        self.assertEqual(expected, etree.tostring(result, encoding='unicode'))

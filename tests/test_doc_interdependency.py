# -*- coding: utf-8 -*-
"""
test_doc_document
~~~~~~~~~~~~~~~~~

Test the interdependency class.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from chemdataextractor.doc.document import Document
from chemdataextractor.doc.interdependency import merge_all_uvvis
from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestUvvisMerging(unittest.TestCase):
    """Test merging of interdependency functions"""

    def test_merge_all_uvvis(self):
        uvvis1 = UvvisSpectrum(peaks=[UvvisPeak(value='345')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(value='123')])
        comp = Compound(uvvis_spectra=[uvvis1, uvvis2])
        gold = Compound(uvvis_spectra=[UvvisSpectrum(peaks=[UvvisPeak(value='345'), UvvisPeak(value='123')])])

        self.assertEqual(merge_all_uvvis(comp), gold)

if __name__ == '__main__':
    unittest.main

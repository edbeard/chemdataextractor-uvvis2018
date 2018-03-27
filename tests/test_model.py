# -*- coding: utf-8 -*-
"""
test_model
~~~~~~~~~~

Test extracted data model.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

from chemdataextractor.model import Compound, MeltingPoint, UvvisSpectrum, UvvisPeak


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestModel(unittest.TestCase):

    maxDiff = None

    def test_serialize(self):
        """Test model serializes as expected."""
        self.assertEqual(Compound(names=['Coumarin 343']).serialize(), {'names': ['Coumarin 343']})

    def test_is_unidentified(self):
        """Test is_unidentified method returns expected result."""
        self.assertEqual(Compound().is_unidentified, True)
        self.assertEqual(Compound(names=['Coumarin 343']).is_unidentified, False)
        self.assertEqual(Compound(labels=['3a']).is_unidentified, False)
        self.assertEqual(Compound(names=['Coumarin 343'], labels=['3a']).is_unidentified, False)
        self.assertEqual(Compound(melting_points=[MeltingPoint(value='250')]).is_unidentified, True)

    def test_is_contextual(self):
        """Test is_contextual method returns expected result."""
        self.assertEqual(Compound(names=['Coumarin 343']).is_contextual, False)
        self.assertEqual(Compound(melting_points=[MeltingPoint(value='240')]).is_contextual, False)
        self.assertEqual(Compound(melting_points=[MeltingPoint(units='K')]).is_contextual, True)
        self.assertEqual(Compound(melting_points=[MeltingPoint(apparatus='Some apparatus')]).is_contextual, True)
        self.assertEqual(Compound(labels=['3a'], melting_points=[MeltingPoint(apparatus='Some apparatus')]).is_contextual, False)
        self.assertEqual(Compound(uvvis_spectra=[UvvisSpectrum(apparatus='Some apparatus')]).is_contextual, True)
        self.assertEqual(Compound(uvvis_spectra=[UvvisSpectrum(peaks=[UvvisPeak(value='378')])]).is_contextual, False)
        self.assertEqual(Compound(uvvis_spectra=[UvvisSpectrum(peaks=[UvvisPeak(units='nm')])]).is_contextual, True)

class TestUvvisSpectrum(unittest.TestCase):

    def test_justValue(self):
        """Test justValue returns true appropriately"""
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467')]).justValue(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(value='234'), UvvisPeak(value='123')]).justValue(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value=None)]).justValue(), False)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(value='234'), UvvisPeak(extinction='12000')]).justValue(), False)

    def test_justExtinction(self):
        """ test justExtinction returns true appropriately"""
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')]).justExtinction(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction='35000'), UvvisPeak(extinction='1.6'), UvvisPeak(extinction='24000')]).justExtinction(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction=None)]).justExtinction(), False)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(extinction='24000'), UvvisPeak(extinction='12000')]).justValue(), False)


if __name__ == '__main__':
    unittest.main()

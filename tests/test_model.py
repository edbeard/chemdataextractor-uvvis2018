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
from chemdataextractor.doc.interdependency import get_indices


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

    def test_just_value(self):
        """Test just_value returns true appropriately"""
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467')]).just_value(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(value='234'), UvvisPeak(value='123')]).just_value(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value=None)]).just_value(), False)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(value='234'), UvvisPeak(extinction='12000')]).just_value(), False)

    def test_just_extinction(self):
        """ test just_extinction returns true appropriately"""
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')]).just_extinction(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction='35000'), UvvisPeak(extinction='1.6'), UvvisPeak(extinction='24000')]).just_extinction(), True)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(extinction=None)]).just_extinction(), False)
        self.assertEqual(UvvisSpectrum(peaks=[UvvisPeak(value='467'), UvvisPeak(extinction='24000'), UvvisPeak(extinction='12000')]).just_value(), False)

    def test_merge_uvvis(self):

        # Case 1 : one value per extinction
        uvvis1 = UvvisSpectrum(peaks=[UvvisPeak(value='345')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis1.merge_uvvis(uvvis2)
        gold = {'peaks': [{'value': '345', 'extinction': '35000'}]}
        self.assertEqual(gold, uvvis1.serialize())

        # Case 2 : One extinction, multiple values
        uvvis1 = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis1.merge_uvvis(uvvis2)
        gold = {'peaks': [{'extinction': '35000', 'value': '123'}, {'extinction': '35000', 'value': '456'}]}
        self.assertEqual(gold, uvvis1.serialize())


    def test_merge_peaks_and_uvvis(self):
        """ Tests merge_peaks_and_uvvis correctly merges values from 1 uvvis object containing multiple peaks to
        a list of extinctions containing one peak each"""

        uvvis_value = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456')])
        uvvis_ext = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis_ext_2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])
        uvvis_value.merge_peaks_and_uvvis([uvvis_ext, uvvis_ext_2], [0, 1])
        gold = {'peaks': [{'value': '123', 'extinction': '35000'}, {'value': '456', 'extinction': '40000'}]}
        self.assertEqual(gold, uvvis_value.serialize())

    def test_merge_peaks(self):

        uvvis = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(extinction='35000')])
        uvvis.merge_peaks(0,1)
        gold = {'peaks': [{'extinction': '35000', 'value': '123'}, {'extinction': '35000'}]}
        self.assertEqual(gold, uvvis.serialize())



if __name__ == '__main__':
    unittest.main()

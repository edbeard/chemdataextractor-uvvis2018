# -*- coding: utf-8 -*-
"""
tests.test_doc_interdependency.py
~~~~~~~~~~~~~~~~~

Test the interdependency class.
:author Edward Beard

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import unittest

import chemdataextractor.doc.interdependency as indep
from chemdataextractor.model import Compound, UvvisSpectrum, UvvisPeak

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestUvvisMerging(unittest.TestCase):
    """Test merging of interdependency functions"""

    def test_get_indices(self):
        uvvis1 = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis3 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])
        comp = Compound(uvvis_spectra=[uvvis1, uvvis2, uvvis3])
        val, ext = indep.get_indices(comp)
        self.assertEqual(val, [0])
        self.assertEqual(ext, [1, 2])

    def test_get_peak_indices(self):
        peak1 = UvvisPeak(value='123')
        peak2 = UvvisPeak(extinction='35000')
        uvvis = UvvisSpectrum(peaks=[peak1, peak2])
        val, ext = indep.get_peak_indices(uvvis)
        self.assertEqual(val, [0])
        self.assertEqual(ext, [1])

    def test_merge_peak_obj(self):
        uvvis = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456'),
                                     UvvisPeak(extinction='35000'), UvvisPeak(extinction='40000')])

        comp = Compound(uvvis_spectra=[uvvis])
        resolved_comp = indep.merge_peak_obj(comp)
        gold = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'},
                                             {'value': '456', 'extinction': '40000'}]}]}

        self.assertEqual(gold, resolved_comp.serialize())

    def test_merge_peak_and_uvvis_obj(self):
        uvvis_value = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis3 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])
        comp = Compound(uvvis_spectra=[uvvis_value, uvvis2, uvvis3])
        resolved_comp = indep.merge_peak_and_uvvis_obj(comp, [0], [1, 2])
        gold = {'uvvis_spectra': [{'peaks': [{'extinction': '35000', 'value': '123'},
                                             {'extinction': '40000', 'value': '456'}]}]}
        self.assertEqual(gold, resolved_comp.serialize())

    def test_check_prev(self):
        uvvis_prev_1 = UvvisSpectrum(peaks=[UvvisPeak(value='123')])
        uvvis_prev_2 = UvvisSpectrum(peaks=[UvvisPeak(value='456')])
        uvvis_current_1 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis_current_2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])

        comp_prev = Compound(uvvis_spectra=[uvvis_prev_1, uvvis_prev_2])
        comp_current = Compound(uvvis_spectra=[uvvis_current_1, uvvis_current_2])

        table_records = [comp_prev]
        comp_current = indep.check_prev(comp_current, [], [0, 1], table_records)
        gold_prev = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'}]},
                                       {'peaks': [{'value': '456', 'extinction': '40000'}]}]}
        gold_current = {}
        self.assertEqual(gold_prev, comp_prev.serialize())
        self.assertEqual(gold_current, comp_current.serialize())

    def test_merge_all_uvvis_1(self):
        peak1 = UvvisPeak(value='123', extinction='35000')
        peak2 = UvvisPeak(value='456', extinction='40000')
        comp = Compound(uvvis_spectra=[UvvisSpectrum(peaks=[peak1]), UvvisSpectrum(peaks=[peak2])])
        comp = indep.merge_all_uvvis(comp)
        gold = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'},
                                             {'value': '456', 'extinction': '40000'}]}]}

        self.assertEqual(gold, comp.serialize())

    def test_merge_all_uvvis_2(self):
        uvvis1 = UvvisSpectrum(peaks=[UvvisPeak(value='345')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(value='123')])
        comp = Compound(uvvis_spectra=[uvvis1, uvvis2])
        gold = Compound(uvvis_spectra=[UvvisSpectrum(peaks=[UvvisPeak(value='345'), UvvisPeak(value='123')])])

        self.assertEqual(indep.merge_all_uvvis(comp), gold)

    def test_merge_uvvis_1(self):
        """Checks merge_peak_obj works in this context"""

        uvvis = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456'),
                                     UvvisPeak(extinction='35000'), UvvisPeak(extinction='40000')])

        comp = Compound(uvvis_spectra=[uvvis])
        table_records = []
        resolved_comp = indep.merge_uvvis(comp, table_records)
        gold = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'},
                                             {'value': '456', 'extinction': '40000'}]}]}
        print(resolved_comp.serialize())

        self.assertEqual(gold, resolved_comp.serialize())

    def test_merge_uvvis_2(self):
        """Checks merge_peak_and_uvvis_obj works in this context"""

        uvvis_value = UvvisSpectrum(peaks=[UvvisPeak(value='123'), UvvisPeak(value='456')])
        uvvis2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis3 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])
        comp = Compound(uvvis_spectra=[uvvis_value, uvvis2, uvvis3])
        table_records = []
        resolved_comp = indep.merge_uvvis(comp, table_records)
        gold = {'uvvis_spectra': [{'peaks': [{'extinction': '35000', 'value': '123'},
                                             {'extinction': '40000', 'value': '456'}]}]}
        self.assertEqual(gold, resolved_comp.serialize())

    def test_merge_uvvis_3(self):
        """Checks check_prev works in this context"""
        uvvis_prev_1 = UvvisSpectrum(peaks=[UvvisPeak(value='123')])
        uvvis_prev_2 = UvvisSpectrum(peaks=[UvvisPeak(value='456')])
        uvvis_current_1 = UvvisSpectrum(peaks=[UvvisPeak(extinction='35000')])
        uvvis_current_2 = UvvisSpectrum(peaks=[UvvisPeak(extinction='40000')])

        comp_prev = Compound(uvvis_spectra=[uvvis_prev_1, uvvis_prev_2])
        comp_current = Compound(uvvis_spectra=[uvvis_current_1, uvvis_current_2])

        table_records = [comp_prev]
        comp_current = indep.merge_uvvis(comp_current, table_records)
        gold_prev = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'}]},
                                       {'peaks': [{'value': '456', 'extinction': '40000'}]}]}
        gold_current = {}
        self.assertEqual(gold_prev, comp_prev.serialize())
        self.assertEqual(gold_current, comp_current.serialize())

    def test_merge_uvvis_4(self):
        """Checks merge_all_uvvis works in this context"""

        peak1 = UvvisPeak(value='123', extinction='35000')
        peak2 = UvvisPeak(value='456', extinction='40000')
        comp = Compound(uvvis_spectra=[UvvisSpectrum(peaks=[peak1]), UvvisSpectrum(peaks=[peak2])])
        row_compound = []
        comp = indep.merge_uvvis(comp, row_compound)
        gold = {'uvvis_spectra': [{'peaks': [{'value': '123', 'extinction': '35000'},
                                             {'value': '456', 'extinction': '40000'}]}]}

        self.assertEqual(gold, comp.serialize())


if __name__ == '__main__':
    unittest.main

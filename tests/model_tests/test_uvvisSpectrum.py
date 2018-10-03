import unittest
from chemdataextractor.model import UvvisSpectrum, UvvisPeak

class TestUvvisSpectrum(unittest.TestCase):
    #def test_merge_uvvis(self):
     #   self.fail()

    #def test_merge_peaks_and_uvvis(self):
     #   self.fail()

    #def test_merge_peaks(self):
     #   self.fail()

    def test_just_value_one_value(self):
        '''Tests just value for a spectrum with one value'''
        u = UvvisSpectrum()
        peak = UvvisPeak()
        peak.value = 467

        u.peaks.append(peak)

        self.assertEqual(u.just_value(), True)

    def test_just_value_one_extinction(self):
        '''Tests just value for failure case with one extinction'''
        u = UvvisSpectrum()
        peak = UvvisPeak()
        peak.extinction = 12345
        u.peaks.append(peak)
        self.assertEqual(u.just_value(), False)

    def test_just_value_multiple_values(self):
        u = UvvisSpectrum()
        peaks = [UvvisPeak(),UvvisPeak(),UvvisPeak()]
        values = [467,234,123]
        for i, peak in enumerate(peaks):
            peak.value = values[i]
            u.peaks.append(peak)

        self.assertEqual(u.just_value(), True)

    #def test_just_extinction(self):
     #   self.fail()

if __name__ == '__main__':
    unittest.main()

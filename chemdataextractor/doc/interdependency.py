# -*- coding: utf-8 -*-
"""
chemdataextractor.doc.table
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interdependecy resolution functions

:author: Edward Beard
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def get_indicies(row_compound):
    '''Aquires indices of unique value/extinction objects at 'uvvis' scope '''
    value_indices, ext_indices = [], []
    for i, uvvis_obj in enumerate(row_compound.uvvis_spectra):
        if uvvis_obj.justValue():
            value_indices.append(i)
        if uvvis_obj.justExtinction():
            ext_indices.append(i)
    return value_indices, ext_indices

def get_peak_indicies(uvvis_obj):
    '''Aquires indices of unique value/extinction objects at 'peak' scope  '''

    # Identifying which peak objects are just values or extinctions
    value_peak_indices, ext_peak_indices = [], []
    for i, peak in enumerate(uvvis_obj.peaks):
        if peak.justValue():
            value_peak_indices.append(i)
        if peak.justExtinction():
            ext_peak_indices.append(i)

    return value_peak_indices, ext_peak_indices

def merge_peak_obj(row_compound):
    ''' Merging internal value peaks with extinction peaks'''

    for uvvis_obj in row_compound.uvvis_spectra:
        if uvvis_obj.peaks != None:
            # Identifying which peak objects are just values or extinctions
            value_peak_indices, ext_peak_indices = get_peak_indicies(uvvis_obj)
            # Merging these peaks if criteria are met
            if value_peak_indices != [] and ext_peak_indices != [] \
                    and len(value_peak_indices) == len(ext_peak_indices):

                for (v, e) in zip(value_peak_indices, ext_peak_indices):
                    uvvis_obj.mergePeaks(v, e)

                # Removing the contextual extinction object
                k = 0
                for e in ext_peak_indices:
                    del uvvis_obj.peaks[e - k]
                    k = k + 1

    return row_compound

def merge_peak_and_uvvis_obj(row_compound, value_indices, ext_indices):
    '''Merges all peak and uvvis objects when on different scopes'''

    # Merging value peaks with uvvis extinctions
    for index in value_indices:
        if len(row_compound.uvvis_spectra[index].peaks) == len(ext_indices) and len(ext_indices) > 1:
            row_compound.uvvis_spectra[index].mergePeaksAndUvvis(row_compound.uvvis_spectra, ext_indices)

            j = 0
            for e in ext_indices:
                del row_compound.uvvis_spectra[e - j]
                j = j + 1

    if value_indices != [] and ext_indices != [] and len(value_indices) == len(ext_indices):
        for (v, e) in zip(value_indices, ext_indices):
            row_compound.uvvis_spectra[v].mergeUvvis(row_compound.uvvis_spectra[e])

        k = 0
        for e in ext_indices:
            del row_compound.uvvis_spectra[e - k]
            k = k + 1

    return row_compound

def check_prev(row_compound, value_indices, ext_indices, table_records):
    '''Check previous row for uvvis data if this row is all extinctions'''
    value_indices_prev = []
    if value_indices == [] and ext_indices != [] and table_records:
        prev = table_records[-1]
        for i, uvvis_obj in enumerate(prev.uvvis_spectra):
            if uvvis_obj.justValue():
                value_indices_prev.append(i)

        if len(value_indices_prev) == len(ext_indices):
            for (v, e) in zip(value_indices_prev, ext_indices):
                prev.uvvis_spectra[v].mergeUvvis(row_compound.uvvis_spectra[e])

            l = 0
            for e in ext_indices:
                del row_compound.uvvis_spectra[e - l]
                l = l + 1

    return row_compound

def merge_all_uvvis(row_compound):
    '''Merges all uvvis objects on this row (after interdependcy checks)'''

    # Add all uvvis objects to a single compound
    for i, uvvis in enumerate(row_compound.uvvis_spectra):
        if i != 0:
            for peak in uvvis.peaks:
                row_compound.uvvis_spectra[0].peaks.append(peak)

    # Remove unnecessary extra peak objects
    l = 0
    for i in range(1,len(row_compound.uvvis_spectra)):
        del row_compound.uvvis_spectra[i-l]
        l += 1

    return row_compound

def merge_uvvis(row_compound, table_records):
    '''Merges uvvis peaks with uvvis extinction coefficients'''

    value_indices, ext_indices = get_indicies(row_compound)
    row_compound = merge_peak_obj(row_compound)
    row_compound = merge_peak_and_uvvis_obj(row_compound, value_indices, ext_indices)
    row_compound = check_prev(row_compound, value_indices, ext_indices, table_records)
    row_compound = merge_all_uvvis(row_compound)

    return row_compound
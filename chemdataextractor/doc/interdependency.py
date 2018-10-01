# -*- coding: utf-8 -*-
"""
chemdataextractor.doc.interdependency.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Interdependency resolution functions

:author : Edward Beard (ejb207@cam.ac.uk)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def get_indices(row_compound):
    """Finds indices of unique value/extinction objects at 'uvvis' scope

    :param chemdataextractor.model.Compound row_compound : Compound containing uvvis data

    :returns
        list value_indices : UvvisSpectrum indices pointing to objects solely containing uvvis values
        list ext_indices : UvvisSpectrum indices pointing to objects solely containing extinction coefficient values
    """

    value_indices, ext_indices = [], []
    for i, uvvis_obj in enumerate(row_compound.uvvis_spectra):
        if uvvis_obj.just_value():
            value_indices.append(i)
        if uvvis_obj.just_extinction():
            ext_indices.append(i)
    return value_indices, ext_indices


def get_peak_indices(uvvis_obj):
    """Finds indices of unique value/extinction objects at 'peak' scope

     :param chemdataextractor.model.UvvisSpectrum uvvis_obj : UvvisSpectrum containng peak data

     :returns
        list value_peak_indices : UvvisPeak indices pointing to objects solely containing uvvis values
        list ext_peak_indices : UvvisPeak indices pointing to objects solely containing extinction coefficient values

     """

    # Identifying which peak objects are just values or extinctions
    value_peak_indices, ext_peak_indices = [], []
    for i, peak in enumerate(uvvis_obj.peaks):
        if peak.just_value():
            value_peak_indices.append(i)
        if peak.just_extinction():
            ext_peak_indices.append(i)

    return value_peak_indices, ext_peak_indices


def merge_peak_obj(row_compound):
    """ Merging internal value peaks with extinction peaks

    :param chemdataextractor.model.Compound row_compound : Compound object containing unresolved peak value/ext pairs

    :return chemdataextractor.model.Compound row_compound : Compound objects with peak objects paired

    """

    for uvvis_obj in row_compound.uvvis_spectra:
        if uvvis_obj.peaks is not None:
            # Identifying which peak objects are just values or extinctions
            value_peak_indices, ext_peak_indices = get_peak_indices(uvvis_obj)
            # Merging these peaks if criteria are met
            if value_peak_indices != [] and ext_peak_indices != [] \
                    and len(value_peak_indices) == len(ext_peak_indices):

                for (v, e) in zip(value_peak_indices, ext_peak_indices):
                    uvvis_obj.merge_peaks(v, e)

                # Removing the contextual extinction object
                k = 0
                for e in ext_peak_indices:
                    del uvvis_obj.peaks[e - k]
                    k = k + 1

    return row_compound


def merge_peak_and_uvvis_obj(row_compound, value_indices, ext_indices):
    """Merges all peak and uvvis objects when on different scopes

    :param chemdataextractor.model.Compound row_compound : Compound with unresolved uvvis peaks and values
    :param list[int] value_indices : List of indices of uvvis value objects
    :param list[int] ext_indices : List of indices of uvvis extinction coefficient objects

    :returns chemdataextractor.model.Compound row_compound : Compound with resolved uvvis peaks and values
    """

    # Merging value peaks with uvvis extinctions
    for index in value_indices:
        if len(row_compound.uvvis_spectra[index].peaks) == len(ext_indices) and len(ext_indices) > 1:
            row_compound.uvvis_spectra[index].merge_peaks_and_uvvis(row_compound.uvvis_spectra, ext_indices)

            j = 0
            for e in ext_indices:
                del row_compound.uvvis_spectra[e - j]
                j = j + 1

    if value_indices != [] and ext_indices != [] and len(value_indices) == len(ext_indices):
        for (v, e) in zip(value_indices, ext_indices):
            row_compound.uvvis_spectra[v].merge_uvvis(row_compound.uvvis_spectra[e])

        k = 0
        for e in ext_indices:
            del row_compound.uvvis_spectra[e - k]
            k = k + 1

    return row_compound


def check_prev(row_compound, value_indices, ext_indices, table_records):
    """ Attempts to resolve UV/Vis data peak values when current row contains solely extinction coefficients.

    .. note ::
        This method is unusual as it also alters the previous result in table_records, not just the compound being
        returned. It is written for specific use inside chemdataextractor.doc.interdependency.merge_uvvis
        function and should not be used on it's own

    TODO : Change functionality/position in pipeline of this function - shouldn't have a check done on every loop that
        relies on previous row. Changes should be implemented via 'return' of function

    :param chemdataextractor.model.Compound row_compound : Compound object generated from current row
    :param list[int] value_indices : Indices list of solely uvvis value objects
    :param list[int] ext_indices : Indices list of solely extinction value objects
    :param list[chemdataextractor.model.compound] table_records: List of compounds resolved from
        table rows up to this one.

    :returns chemdataextractor.model.Compound row_compound : Compound object with extinction objects removed
    """

    value_indices_prev = []
    if value_indices == [] and ext_indices != [] and table_records:
        prev = table_records[-1]
        for i, uvvis_obj in enumerate(prev.uvvis_spectra):
            if uvvis_obj.just_value():
                value_indices_prev.append(i)

        if len(value_indices_prev) == len(ext_indices):
            for (v, e) in zip(value_indices_prev, ext_indices):
                prev.uvvis_spectra[v].merge_uvvis(row_compound.uvvis_spectra[e])

            j = 0
            for e in ext_indices:
                del row_compound.uvvis_spectra[e - j]
                j += 1

    return row_compound


def merge_all_uvvis(row_compound):
    """ Groups all UvvisSpectrum objects for input Compound object together

    :param chemdataextractor.model.Compound row_compound : Compound object generated from current row

    :returns chemdataextractor.model.Compound row_compound : Compound generated from current row with interdependency
        resolved where possible
    """

    # Add all uvvis objects to a single compound
    for i, uvvis in enumerate(row_compound.uvvis_spectra):
        if i != 0:
            for peak in uvvis.peaks:
                row_compound.uvvis_spectra[0].peaks.append(peak)

    # Remove unnecessary extra peak objects
    j = 0
    for i in range(1, len(row_compound.uvvis_spectra)):
        del row_compound.uvvis_spectra[i-j]
        j += 1

    return row_compound


def merge_uvvis(row_compound, table_records):
    """ Merges unpaired UV/Vis peak value data with UV/Vis peak extinction coefficient data for tables.

    .. note:
        To be used as part of the records resolution in chemdataextractor.doc.table.records.
        This should include all current developed functions for pairing UV/Vis peak values and extinction coefficients.

    :param chemdataextractor.model.compound row_compound : Compound object generated from current row
    :param list[chemdataextractor.model.compound row_compound] table_records : List of Compound objects for
        all rows until current row

    :returns chemdataextractor.model.compound row_compound : Resolved Compound object for current row
    """

    value_indices, ext_indices = get_indices(row_compound)
    row_compound = merge_peak_obj(row_compound)
    row_compound = merge_peak_and_uvvis_obj(row_compound, value_indices, ext_indices)
    row_compound = check_prev(row_compound, value_indices, ext_indices, table_records)
    row_compound = merge_all_uvvis(row_compound)

    return row_compound

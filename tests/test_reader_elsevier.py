# -*- coding: utf-8 -*-
"""
test_reader_acs
~~~~~~~~~~~~~~~

Test Elsevier reader.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import logging
import os
import unittest

from chemdataextractor import Document
from chemdataextractor.reader import ElsevierHtmlReader


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class TestElsevierHtmlReader(unittest.TestCase):
    """ Tests for Elsevier specific reader"""

    def test_detect(self):
        """ Tests that ElsevierHtmlReader can detect Elsevier docs"""

        r = ElsevierHtmlReader()
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        content = f.read()
        self.assertEqual(r.detect(content, fname=fname), True)

    def test_direct_usage(self):
        """Test ElsevierHtmlReader used directly to parse file."""
        r = ElsevierHtmlReader()
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        self.assertEqual(len(d.elements), 246)

    def test_document_usage(self):
        """Test ElsevierHtmlReader used via Document.from_file."""
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        d = Document.from_file(f, readers=[ElsevierHtmlReader()])
        self.assertEqual(len(d.elements), 246)

    def test_fig_and_fig_cation_detection(self):
        """ Tests ElsevierHtmlReader can detect the right number of figures and fig captions"""
        r = ElsevierHtmlReader()
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        figs = d.figures
        captions = [fig for fig in figs if fig.caption.text != ('\n' or '' )]
        self.assertEqual(len(figs), 10)
        self.assertEqual(len(captions), 9) # Graphical abstract has no caption

        # TODO : Add some specific \n removal for Elsevier figure captions

    def test_table_and_table_caption_detection(self):
        """ Tests ElsevierHtmlReader can detect the correct number of tables and table captions"""
        r = ElsevierHtmlReader()
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        tables = d.tables
        captions = [tab for tab in tables if tab.caption.text != None]
        self.assertEqual(len(tables), 2)
        self.assertEqual(len(captions), 2)



    def test_table_caption_compound_detection(self):
        """ Test Elsevier Reader can assign and resolve table captions, where the caption contains the compound"""

        r = ElsevierHtmlReader()
        html = '<div> <dl class="table " data-label="Table 1" data-t="t" id="t0005"> <dd class="lblCap"> <div class="caption"> <span class="label"> Table 1. </span> <p> Steady state spectral properties of HMBA in different homogeneous solvents. </p> </div> </dd> <dd class="table" title="Steady state spectral properties of HMBA in different homogeneous solvents."> <table> <colgroup> <col> </col> <col> </col> <col> </col> <col> </col> <col> </col> </colgroup> <thead> <tr> <th class="valign " colspan="1" rowspan="1" scope="col"> Solvents </th> <th class="valign " colspan="1" rowspan="1" scope="col"> <em> λ </em> <sub> <em> abs </em> </sub> <span id="btbl1fna"> <a class="intra_ref" href="#tbl1fna" id="ancbtbl1fna"> <sup> a </sup> </a> </span> (nm) </th> <th class="valign " colspan="1" rowspan="1" scope="col"> <em> λ </em> <sub> <em> fl </em> </sub> <span id="btbl1fnb"> <a class="intra_ref" href="#tbl1fnb" id="ancbtbl1fnb"> <sup> b </sup> </a> </span> (nm) </th> <th class="valign " colspan="1" rowspan="1" scope="col"> ∆ <em> ν </em> <sub> <em> SS </em> </sub> <span id="btbl1fnc"> <a class="intra_ref" href="#tbl1fnc" id="ancbtbl1fnc"> <sup> c </sup> </a> </span> (cm <sup> −1 </sup> ) </th> <th class="valign " colspan="1" rowspan="1" scope="col"> <em> ϕ </em> <sub> <em> f </em> </sub> <span id="btbl1fnd"> <a class="intra_ref" href="#tbl1fnd" id="ancbtbl1fnd"> <sup> d </sup> </a> </span> (10 <sup> −3 </sup> ) </th> </tr> </thead> <tbody> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Cyclohexane </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 355 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 398, 445 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3043, 5697 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 5.7 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Hexane </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 353 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 397, 447 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3139, 5957 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 6.5 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> 1,4-Dioxane </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 358 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 398, 445 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 2807, 5461 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 2.3 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Acetonitrile </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 360 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 414, 458 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3623, 5943 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 5.8 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Chloroform </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 355 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 398, 442 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3043, 5544 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 5.6 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Carbon tetrachloride </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 355 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 412, 445 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3897, 5697 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 5.3 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Methanol </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 358 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 403, 442 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3119, 5308 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 4.4 </td> </tr> <tr> <td class="alignTD valign " colspan="1" rowspan="1"> Water </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 360 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 408, 448 (s) </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3267, 5456 </td> <td class="alignTDchar valign " colspan="1" rowspan="1"> 3.2 </td> </tr> </tbody> </table> </dd> <dd> <dl class="tblFootnote" data-t="n" id="tbl1fna"> <dt> a </dt> <dd> <p> Absorption maxima. </p> </dd> </dl> <dl class="tblFootnote" data-t="n" id="tbl1fnb"> <dt> b </dt> <dd> <p> Fluorescence maxima. </p> </dd> </dl> <dl class="tblFootnote" data-t="n" id="tbl1fnc"> <dt> c </dt> <dd> <p> Stokes shift. </p> </dd> </dl> <dl class="tblFootnote" data-t="n" id="tbl1fnd"> <dt> d </dt> <dd> <p> Fluorescence yield. </p> </dd> </dl> </dd> <dd class="fullsizeTable"> <a class="tableAnchor" data-url="/science?_ob=MiamiCaptionURL&amp;_method=retrieve&amp;_eid=1-s2.0-S0022231313008399&amp;_image=t0005&amp;_cid=271627&amp;_explode=defaultEXP_LIST&amp;_idxType=defaultREF_WORK_INDEX_TYPE&amp;_alpha=defaultALPHA&amp;_ba=&amp;_rdoc=1&amp;_fmt=&amp;_issn=00222313&amp;_pii=S0022231313008399&amp;_isTablePopup=Y&amp;md5=720980f427cc62abd953d969ae907cab" href="#" title="Full-size table - Opens new window"> Full-size table </a> </dd> <dd class="menuButtonLinks"> <ul class="menuButton"> <li> <a class="viewWS S_C_table_view_WS" href="#t0005" title="View in workspace"> View in workspace </a> </li> <li> <div class="downloadCsv"> <a class="S_C_csv_download" href="#" title="Download as CSV"> Download as CSV </a> </div>'
        gold = [{'uvvis_spectra': [{'solvent': 'Cyclohexane', 'peaks': [{'units': 'nm', 'value': '355'}]}, {'solvent': 'Hexane', 'peaks': [{'units': 'nm', 'value': '353'}]}, {'solvent': 'Dioxane', 'peaks': [{'units': 'nm', 'value': '358'}]}, {'solvent': 'Acetonitrile', 'peaks': [{'units': 'nm', 'value': '360'}]}, {'solvent': 'Chloroform', 'peaks': [{'units': 'nm', 'value': '355'}]}, {'solvent': 'Carbon tetrachloride', 'peaks': [{'units': 'nm', 'value': '355'}]}, {'solvent': 'Methanol', 'peaks': [{'units': 'nm', 'value': '358'}]}, {'solvent': 'Water', 'peaks': [{'units': 'nm', 'value': '360'}]}], 'names': ['HMBA']}]
        self.assertEqual(r.parse(html).records.serialize(), gold)

if __name__ == '__main__':
    unittest.main()
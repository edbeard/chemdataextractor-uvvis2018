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
from chemdataextractor.reader import SpringerHtmlReader


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TestSpringerHtmlReader(unittest.TestCase):
    """ Tests for Elsevier specific reader"""

    def test_detect(self):

        """ Tests that SpringerHtmlReader can detect Springer docs"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        self.assertEqual(r.detect(content, fname=fname), True)

    def test_failed_detect(self):
        """ Tests that an Elsevier doc is not detected"""
        r = SpringerHtmlReader()
        fname = 'S0143720816310816.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'elsevier', fname), 'rb')
        content = f.read()
        self.assertEqual(r.detect(content, fname=fname), False)

    def test_direct_usage(self):
        """Test SpringerHtmlReader used directly to parse file."""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        self.assertEqual(len(d.elements), 173)

    def test_document_usage(self):
        """Test SpringerHtmlReader used via Document.from_file."""
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        d = Document.from_file(f, readers=[SpringerHtmlReader()])
        self.assertEqual(len(d.elements), 173)

    def test_fig_and_fig_cation_detection(self):
        """ Tests ElsevierHtmlReader can detect the right number of figures and fig captions"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        figs = d.figures
        captions = [fig.caption for fig in figs if fig.caption.text != ('\n' or '' )]
        self.assertEqual(len(figs), 5)
        self.assertEqual(len(captions), 5)
        self.assertEqual(len(captions[4].sentences), 6)

    def test_fig_url_detection(self):
        """ Tests ElsevierHtmlReader can detect the figure source link"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        figs = d.figures
        url = figs[0].url
        self.assertEqual(url, 'https://media.springernature.com/lw785/springer-static/image/art%3A10.1186%2F1423-0127-16-26/MediaObjects/12929_2008_Article_26_Fig1_HTML.jpg')

    def test_fig_id_detection(self):
        """ Tests the figure id is correct"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        figs = d.figures
        fig_1_id = figs[0].id
        self.assertEqual(fig_1_id, 'Fig1')

    def test_table_and_table_caption_detection(self):
        """ Tests ElsevierHtmlReader can detect the correct number of tables and table captions"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        tables = d.tables
        captions = [tab for tab in tables if tab.caption.text != None]
        self.assertEqual(len(tables), 1)
        self.assertEqual(len(captions), 1)

    def test_table_column_number(self):
        """ Tests that all the table columns have been found correctly"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        tables = d.tables
        headings = [heading for heading_row in tables[0].headings for heading in heading_row ]
        self.assertEqual(len(headings), 5)

    def test_table_row_number(self):
        """ Tests that all the table columns have been found correctly"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        tables = d.tables
        rows = tables[0].rows
        self.assertEqual(len(rows), 11) # NB they have got 'header' information in the first row here

    def test_table_captions(self):
        """ Test that caption was corretly idetified"""
        r = SpringerHtmlReader()
        fname = '1423-0127-16-26.html'
        f = io.open(os.path.join(os.path.dirname(__file__), 'data', 'springer', fname), 'rb')
        content = f.read()
        d = r.readstring(content)
        tables = d.tables
        caption = tables[0].caption
        self.assertEqual(caption.text, """
 Table 1
 Effects of genistein, EGF, 17β-estradiol and combinations of genistein with EGF or 17β-estradiol on accumulation of lysosomes containing complex storage structures in MPS IIIA fibroblasts 
 
""") # NB they have got 'header' information in the first row here
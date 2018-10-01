# -*- coding: utf-8 -*-
"""
chemdataextractor.reader.elsevier.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Readers for documents from Elsevier.

:author Edward Beard (ejb207@cam.ac.uk)
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from ..scrape.clean import clean
from .markup import HtmlReader


log = logging.getLogger(__name__)


class ElsevierHtmlReader(HtmlReader):
    """Reader for HTML documents from Elsevier."""

    cleaners = [clean]

    root_css = 'body'
    table_css = 'dl[class~=table]'
    table_caption_css = 'dl[class~=table] div[class=caption]'
    table_head_row_css = 'table thead tr'
    table_body_row_css = 'table tbody tr'
    table_footnote_css = 'dl[class~=tblFootnote]'
    figure_css = 'dl[class~=figure]'
    figure_caption_css = ' .caption'

    def detect(self, fstring, fname=None):
        """ Identifies Elsevier articles from string"""
        if fname and not (fname.endswith('.html') or fname.endswith('.htm')):
            return False
        if b'xmlns:bk="http://www.elsevier.com/xml/bk/dtd"' in fstring:
            return True
        return False

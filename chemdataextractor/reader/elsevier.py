# -*- coding: utf-8 -*-
"""
chemdataextractor.reader.elsevier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Readers for documents from Elsevier.

:copyright: Copyright 2018 by Ed Beard.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from ..doc.text import Footnote
from ..scrape.pub.rsc import replace_rsc_img_chars
from ..scrape.clean import clean
from .markup import HtmlReader


log = logging.getLogger(__name__)

class ElsevierHtmlReader(HtmlReader):
    """Reader for HTML documents from Elsevier."""

    root_css = 'body'
    table_css = 'dl[class~=table]'
    table_caption_css = 'dl[class~=table] div[class=caption]'
    table_head_row_css = 'table thead tr'
    table_body_row_css = 'table tbody tr'
    #table_footnote_css = 'table tfoot tr th .sup_inf'
    figure_css = 'dl[class~=figure]'
    figure_caption_css = ' .caption'





    def detect(self, fstring, fname=None):
        """ Identifies Elsevier articles from string"""
        if fname and not (fname.endswith('.html') or fname.endswith('.htm')):
            return False
        if b'xmlns:bk="http://www.elsevier.com/xml/bk/dtd"' in fstring:
            print('Elseiver doc detected')
            return True
        return False
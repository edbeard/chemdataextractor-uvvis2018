# -*- coding: utf-8 -*-
"""
chemdataextractor.reader.springer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Readers for documents from Sringer.

:author: Ed Beard
:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from ..doc.text import Footnote
from ..scrape.clean import clean
from .markup import HtmlReader


log = logging.getLogger(__name__)


class SpringerHtmlReader(HtmlReader):
    """Reader for HTML documents from Springer."""

    cleaners = [clean]

    root_css = '.main-body__content'
    table_css = 'div.Table'
    table_caption_css = 'div[class~=Table] div[class=Caption]'
    table_head_row_css = 'table thead tr'
    table_footnote_css = '.TableFooter'
    figure_css = 'figure'
    figure_caption_css = 'figcaption'

    def detect(self, fstring, fname=None):
        """"""
        if fname and not (fname.endswith('.html') or fname.endswith('.htm')):
            return False
        if b'https://link.springer.com/article/' in fstring:
            return True
        return False

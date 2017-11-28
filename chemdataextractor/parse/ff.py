# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.ff
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser test for 'fill factor'

:copyright: Copyright 2016 by Matt Swain.
:license: MIT, see LICENSE file for more details.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import re

from lxml.builder import E

from .common import lbrct, rbrct
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name
from ..utils import first
from .actions import merge, join
from ..model import Compound, FillFactor
from .base import BaseParser
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

log = logging.getLogger(__name__)

acronym = (Optional(lbrct) + R('^FF$',re.I) + Optional(rbrct)).add_action(merge)
joiner = Optional((I('and')) + (I('a') | (I('the'))))

ff_phrase = (Optional(I('and')) + I('the') + I('fill') + I('factor') + Optional(acronym) + I('is')).hide()
ff_short = (acronym | (I('fill') + I('factor'))) + ( I('is') | (Optional(I('value')) + I('of'))| I('=')) 

ff = (R('^0+(\.\d+)?'))('fill_factor').add_action(merge)

rootTest = ((ff_phrase | ff_short) + ff)('rootTest')

#pv = prefix + fill_factor_id + fill_factor
class FfParser(BaseParser):
    """Test class for obtaining Pv attributes"""
    root = rootTest
        
    def interpret(self, result, start, end):
        c = Compound() 
        for cem_el in result.xpath('./cem'):
            c.names=cem_el.xpath('./name/text()'),
            c.labels=cem_el.xpath('./label/text()'),
            #c.roles=[standardize_role(r) for r in cem_el.xpath('./role/text()')]
        f = FillFactor(
            fill_factor=first(result.xpath('./fill_factor/text()'))
            )
        c.fill_factor.append(f)
        yield c
        

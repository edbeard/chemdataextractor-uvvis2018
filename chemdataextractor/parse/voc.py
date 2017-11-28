# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.voc
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser test for 'open circuit potential'

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

from ..utils import first
from .common import lbrct, rbrct, comma
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name
from .actions import merge, join
from ..model import Compound, Voc
from .base import BaseParser
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

log = logging.getLogger(__name__)


number = R('^\d+(\.\d+)?$', re.I)

acronym = (Optional(lbrct) + (R('^Voc(,)?$', re.I)| R('^V$', re.I) + R('^oc(,)?$', re.I)) + Optional(rbrct)).add_action(merge) # Sets up the acronym identifier

oc_potential_phrase = (Optional(I('the')) + I('open') + I('circuit') + (I('potential') | I('voltage')) + Optional(acronym) + I('is')).hide()
oc_short = (acronym + Optional(comma)) + Optional(I('is') |(Optional(I('value')) + I('of')) | (I('value') + I('up') + I('to'))| I('='))




#oc_value = number('value').add_action(merge)
oc_unit = (R('^m?V$') | (Optional(R('^m$')) + R('^V$')))('units').add_action(merge)

testValue = (number)('value')
#testUnit = (R('V'))('units').add_action(merge)

voc = (testValue + oc_unit)('voc')

vocRoot = ((oc_potential_phrase|oc_short) + voc)('testPhrase')

#pv = prefix + fill_factor_id + fill_factor
class VocParser(BaseParser):
    """Test class for obtaining Pv attributes"""
    root = vocRoot
        
    def interpret(self, result, start, end):
        c = Compound()
        for cem_el in result.xpath('./cem'):
            c.names=cem_el.xpath('./name/text()'),
          #  c.labels=cem_el.xpath('./label/text()')
                #c.roles=[standardize_role(r) for r in cem_el.xpath('./role/text()')]
        v = Voc(
            voc_value=first(result.xpath('./voc/value/text()')),
            voc_units=first(result.xpath('./voc/units/text()'))
        )

        c.voc.append(v)     
        yield c
        

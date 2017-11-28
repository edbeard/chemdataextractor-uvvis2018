# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.pce
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser test for 'performance conversion efficiency'

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
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name, chemical_name
from ..utils import first
from .actions import merge, join
from ..model import Compound, Pce
from .base import BaseParser
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

log = logging.getLogger(__name__)

number = R('^\d+(\.\d+)?$', re.I)

dblAcronym = (Optional(lbrct) + (I('PCE,') +  R('^η(s)?$')) + Optional(rbrct)).add_action(merge) # For cases when both abbreviations specified
singAcronym = (Optional(lbrct) + (R('^PCE(s)?$') | R('^pce(s)?$') | R('^η(s)?$')) + Optional(rbrct)).add_action(merge)
acronym = singAcronym | dblAcronym

delim = R('^[:;\.,]$')

#chem_name = (chemical_name)('name')

#name = (Optional(lbrct) + (cem | solvent_name) + Optional(rbrct))('cem')

#cem_phrase = I('with') + I('the') + name + Optional(delim)+ Optional(I('dye'))
pce_phrase = ( Optional(I('which')) + Optional(I('yielded'))+ Optional(I('a')) + I('conversion') + I('efficiency') + Optional(acronym) + Optional(I('a') +  I('value')) + I('of')).hide()
pce_filler = ((Optional(I('of')) + Optional(I('up')) + I('to') + Optional('about')) | I('=')| (Optional(I('has')) + I('reached') + Optional(I('a') + I('record'))) | (I('achieved') + I('was')))
pce_filler2 = (Optional(I('value')) + I('of'))

pce_short = (acronym | I('efficiency')) + (pce_filler | pce_filler2)

pce = (Optional(R('^[~∼]$')) + number + Optional(R('^\%$')))('pce').add_action(merge)
       # | number('value') + R('^\%$')('units')) 
#(number('value') + R('^m?V$')('units'))('pce')

total = ((pce_phrase |pce_short) + pce)('total')

#pv = prefix + fill_factor_id + fill_factor
class PceParser(BaseParser):
    """Test class for obtaining Pv attributes"""
    root = total
        
    def interpret(self, result, start, end):
        c = Compound()
        for cem_el in result.xpath('./cem'):
                c.names=cem_el.xpath('./name/text()'),
                c.labels=cem_el.xpath('./label/text()'),
                #c.roles=[standardize_role(r) for r in cem_el.xpath('./role/text()')]
        p = Pce(
                pce=first(result.xpath('./pce/text()'))
            )
        c.pce.append(p)  
        yield c
        

 # -*- coding: utf-8 -*-
"""
chemdataextractor.parse.jsc
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser test for 'short circuit current density'

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

from .common import lbrct, rbrct, comma
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name
from ..utils import first
from .actions import merge, join
from ..model import Compound, Jsc
from .base import BaseParser
from .elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore

log = logging.getLogger(__name__)

#performance_conv_eff = R('PCE' | 'η')

number = R('^\d+(\.\d+)?$')
acronym = (Optional(lbrct) + (R('^Jsc$', re.I)) + Optional(rbrct)).add_action(merge)
#cems_phrase = I('obtained') + I('with') + (cem | solvent_name | I('N749')) + I('are') + Optional(I('in') +  I('the') + I('range') +  I('of'))

#sc_current_phrase = (Optional(I('the')) + Optional(I('short') + I('circuit')) + R('^(photo)?current$') + Optional(I('density')) + Optional(acronym) + (I('is')|I('of'))).hide()
sc_short = (acronym | I('photocurrent')) + ((Optional(I('value')) + I('of')) |I('is') | I('=')| I('to') + I('about')| comma)

sc = (number)('value')
#sc_value = (Optional(R('^[~∼]$')) + sc)

sc_units = ((R('^m?Acm[-‐‑⁃‒–—―−－⁻]2$')) | (R('^m?A$') + R('^cm[-‐‑⁃‒–—―−－⁻]2$')))('units')
#))('units').add_action(merge)

#sc_current = (sc_value + sc_units)('jsc')

#total = ((sc_short|sc_current_phrase) + sc_current)('total')

sc_total = (sc + sc_units)('jsc')

testTotal = (sc_short + sc_total)('testTotal')

#pv = prefix + fill_factor_id + fill_factor
class JscParser(BaseParser):
    """Test class for obtaining Pv attributes"""
    root = testTotal
        
    def interpret(self, result, start, end):
        c = Compound()
        for cem_el in result.xpath('./cem'):
                c.names=cem_el.xpath('./name/text()'),
                c.labels=cem_el.xpath('./label/text()'),
                #c.roles=[standardize_role(r) for r in cem_el.xpath('./role/text()')]

        j = Jsc(
                jsc_value=first(result.xpath('./jsc/value/text()')),
                jsc_units=first(result.xpath('./jsc/units/text()'))
        )
        c.jsc.append(j)
        #cem_el = first(result.xpath('./cem'))
        yield c
        

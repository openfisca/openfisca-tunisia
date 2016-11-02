# -*- coding: utf-8 -*-

# from openfisca_core.reforms import Reform, compose_reforms
from openfisca_core.tools import assert_near

from .. import TunisiaTaxBenefitSystem


__all__ = [
    'assert_near',
    'tax_benefit_system',
    ]


tax_benefit_system = TunisiaTaxBenefitSystem()

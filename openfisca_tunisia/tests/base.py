# -*- coding: utf-8 -*-

from openfisca_core.tools import assert_near
from .. import TunisiaTaxBenefitSystem
from ..reforms import (
    plf_2017,
    )

import logging
log = logging.getLogger(__name__)

__all__ = [
    'assert_near',
    'get_cached_composed_reform',
    'get_cached_reform',
    'tax_benefit_system',
    ]

# Initialize a tax_benefit_system
tax_benefit_system = TunisiaTaxBenefitSystem()


# Reforms cache, used by long scripts like test_yaml.py
# The reforms commented haven't been adapted to the new core API yet.
reform_list = {
    'plf_2017': plf_2017.plf_2017,
    }


# Only use the following reform if scipy can be imported
try:
    import scipy
except ImportError as e:
    log.warn(u'Failed to import "scipy" library. {}'.format(e.error))
    scipy = None

if scipy is not None:
    from ..reforms import de_net_a_brut
    reform_list['de_net_a_brut'] = de_net_a_brut.de_net_a_brut


def get_cached_composed_reform(reform_keys, tax_benefit_system):
    if reform_keys:
        for reform in reform_keys:
            reform_path = "openfisca_tunisia.reforms." + reform + "." + reform
            tax_benefit_system = tax_benefit_system.apply_reform(reform_path)

    return tax_benefit_system


def get_cached_reform(reform_key, tax_benefit_system):
    return get_cached_composed_reform([reform_key], tax_benefit_system)

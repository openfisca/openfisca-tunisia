# -*- coding: utf-8 -*-

import datetime


from openfisca_tunisia import TunisiaTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = TunisiaTaxBenefitSystem()


def check_legislation_file(year):
    compact_legislation = tax_benefit_system.get_parameters_at_instant(year)
    assert compact_legislation is not None


def test_legislation_file():
    for year in range(2006, datetime.date.today().year + 1):
        check_legislation_file(year)

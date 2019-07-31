import pytest
import datetime

from openfisca_tunisia import TunisiaTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = TunisiaTaxBenefitSystem()


@pytest.mark.parametrize('year', range(2006, datetime.date.today().year + 1))
def test_legislation_xml_file(year):
    compact_legislation = tax_benefit_system.get_parameters_at_instant(year)
    assert compact_legislation is not None

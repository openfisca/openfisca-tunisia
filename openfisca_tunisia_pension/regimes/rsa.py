"""Régime des salariés agricoles."""

# Third Party
from numpy import apply_along_axis
from numpy import maximum as max_
from numpy import vstack
from openfisca_core import periods
from openfisca_core.model_api import YEAR, Variable, max_

# First Party
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from openfisca_tunisia_pension.tools import make_mean_over_largest
from openfisca_tunisia_pension.variables.helpers import pension_generique


class RegimeRSA(AbstractRegimeEnAnnuites):
    name = "Régime des salariés agricoles"
    variable_prefix = "rsa"
    parameters_prefix = "rsa"

    class salaire_reference(Variable):
        value_type = float
        entity = Individu
        label = "Salaires de référence du régime des salariés agricoles"
        definition_period = YEAR

        def formula(individu, period):
            # TODO: gérer le nombre d'année
            # TODO: plafonner les salaires à 2 fois le smag de l'année d'encaissement
            base_declaration_rsa = 180
            base_liquidation_rsa = 300

            k = 3
            mean_over_largest = make_mean_over_largest(k)
            salaire = apply_along_axis(
                mean_over_largest,
                axis=0,
                arr=vstack(
                    [
                        individu("salaire", period=periods.period("year", year))
                        for year in range(period.start.year, period.start.year - n, -1)
                    ]
                ),
            )
            salaire_refererence = salaire * base_liquidation_rsa / base_declaration_rsa
            return salaire_refererence

    class pension(Variable):
        value_type = float
        entity = Individu
        label = "Salaires de référence du régime des salariés agricoles"
        definition_period = YEAR

        def formula(individu, period, parameters):
            rsa = parameters(period).retraite.regime_name
            taux_annuite_base = rsa.taux_annuite_base
            taux_annuite_supplementaire = rsa.taux_annuite_supplementaire
            duree_stage = rsa.stage_requis
            age_elig = rsa.age_legal
            periode_remplacement_base = rsa.periode_remplacement_base
            plaf_taux_pension = rsa.plaf_taux_pension
            smag = parameters(period).marche_travail.smag * 25
            duree_stage_validee = duree_assurance > 4 * duree_stage
            pension_min = rsa.pension_min
            salaire_reference = individu("regime_name_salaire_reference", period)

            montant = pension_generique(
                duree_assurance,
                sal_ref,
                taux_annuite_base,
                taux_annuite_supplementaire,
                duree_stage,
                age_elig,
                periode_remplacement_base,
                plaf_taux_pension,
            )

            elig_age = age > age_elig
            elig = duree_stage_validee * elig_age * (salaire_reference > 0)
            montant_percu = max_(montant, pension_min * smag)
            pension = elig * montant_percu
            return pension

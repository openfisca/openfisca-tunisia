"""Abstract regimes definition."""

# Third Party
import numpy as np
from openfisca_core.errors.variable_not_found_error import VariableNotFoundError
from openfisca_core.model_api import (
    ETERNITY,
    MONTH,
    YEAR,
    Variable,
    date,
    max_,
    min_,
    set_input_divide_by_period,
)

# First Party
# Import the Entities specifically defined for this tax and benefit system
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.tools import revalorise


class AbstractRegime(object):
    name = None
    variable_prefix = None
    parameters = None

    class cotisation(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "cotisation retraite employeur"

        def formula(individu, period, parameters):
            NotImplementedError

    class duree_assurance(Variable):
        value_type = int
        entity = Individu
        definition_period = YEAR
        label = "Durée d'assurance (trimestres validés)"

        # def formula(individu, period, parameters):
        #     duree_assurance_validee = individu("regime_name_duree_assurance_validee", period)
        #     annee_de_liquidation = individu('regime_name_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        #     majoration_duree_assurance = individu('regime_name_majoration_duree_assurance', period)
        #     return where(
        #         annee_de_liquidation == period.start.year,
        #         round_(duree_assurance_validee + majoration_duree_assurance),  # On arrondi l'année de la liquidation
        #         duree_assurance_validee
        #         )

    class liquidation_date(Variable):
        value_type = date
        entity = Individu
        definition_period = ETERNITY
        label = "Date de liquidation"
        default_value = date(2250, 12, 31)

    class majoration_pension(Variable):
        value_type = int
        entity = Individu
        definition_period = MONTH
        label = "Majoration de pension"

        def formula(individu, period, parameters):
            NotImplementedError

    class pension(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension"

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_brute(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension brute"

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_servie(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension servie"

        def formula(individu, period, parameters):
            NotImplementedError


class AbstractRegimeEnAnnuites(AbstractRegime):
    name = "Régime en annuités"
    variable_prefix = "regime_en_annuites"
    parameters = "regime_en_annuites"

    class duree_assurance_annuelle(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Durée d'assurance (en trimestres validés l'année considérée)"

    class eligible(Variable):
        value_type = bool
        entity = Individu
        label = "L'individu est éligible à une pension"
        definition_period = YEAR

        def formula(individu, period, parameters):
            NotImplementedError

    class pension(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension"

        def formula(individu, period):
            pension_brute = individu("regime_name_pension_brute", period)
            eligible = individu("regime_name_eligible", period)
            try:
                pension_minimale = individu("regime_name_pension_minimale", period)
            except VariableNotFoundError:
                pension_minimale = 0
            try:
                pension_maximale = individu("regime_name_pension_maximale", period)
            except (VariableNotFoundError, NotImplementedError):
                return max_(pension_brute, pension_minimale)
            return eligible * min_(
                pension_maximale, max_(pension_brute, pension_minimale)
            )

    class pension_brute(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension brute"

        def formula(individu, period, parameters):
            taux_de_liquidation = individu("regime_name_taux_de_liquidation", period)
            salaire_de_reference = individu("regime_name_salaire_de_reference", period)
            return (taux_de_liquidation * salaire_de_reference,)

    class pension_maximale(Variable):
        value_type = float
        default_value = np.inf  # Pas de pension maximale par défaut
        entity = Individu
        definition_period = YEAR
        label = "Pension maximale"

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_minimale(Variable):
        value_type = float
        # default_value = 0  # Pas de pension minimale par défaut, elle est à zéro
        entity = Individu
        definition_period = YEAR
        label = "Pension minimale"

        def formula(individu, period, parameters):
            NotImplementedError

    class pension_servie(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension servie"

        def formula(individu, period, parameters):
            annee_de_liquidation = (
                individu("regime_name_liquidation_date", period)
                .astype("datetime64[Y]")
                .astype(int)
                + 1970
            )
            # Raccouci pour arrêter les calculs dans le passé quand toutes les liquidations ont lieu dans le futur
            if all(annee_de_liquidation > period.start.year):
                return individu.empty_array()
            last_year = period.last_year
            pension_au_31_decembre_annee_precedente = individu(
                "regime_name_pension_au_31_decembre", last_year
            )
            revalorisation = parameters(
                period
            ).regime_name.revalarisation_pension_servie
            pension = individu("regime_name_pension_au_31_decembre", period)
            return revalorise(
                pension_au_31_decembre_annee_precedente,
                pension,
                annee_de_liquidation,
                revalorisation,
                period,
            )

    class salaire_de_base(Variable):
        value_type = float
        entity = Individu
        definition_period = MONTH
        label = "Salaire de base (salaire brut)"
        set_input = set_input_divide_by_period

    class salaire_de_reference(Variable):
        value_type = float
        entity = Individu
        definition_period = ETERNITY
        label = "Salaire de référence"

    class taux_de_liquidation(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Taux de liquidation de la pension"

        def formula(individu, period, parameters):
            bareme_annuite = parameters(period).retraite.regime_name.bareme_annuite
            duree_assurance = individu("regime_name_duree_assurance", period)
            taux_annuite = bareme_annuite.calc(duree_assurance)
            return taux_annuite

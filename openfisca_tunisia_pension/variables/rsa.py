"""Abstract regimes definition."""
import numpy as np
from openfisca_core.errors.variable_not_found_error import VariableNotFoundError
from openfisca_core.model_api import ETERNITY, MONTH, YEAR, Variable, date, max_, min_, set_input_divide_by_period
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.tools import revalorise
'Régime des salariés agricoles.'
from numpy import apply_along_axis
from numpy import maximum as max_
from numpy import vstack
from openfisca_core import periods
from openfisca_core.model_api import YEAR, Variable, max_
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from openfisca_tunisia_pension.tools import make_mean_over_largest
from openfisca_tunisia_pension.variables.helpers import pension_generique

class rsa_cotisation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'cotisation retraite employeur'

    def formula(individu, period, parameters):
        NotImplementedError

class rsa_duree_assurance(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (trimestres validés)"

class rsa_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (en trimestres validés l'année considérée)"

class rsa_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est éligible à une pension"
    definition_period = YEAR

    def formula(individu, period, parameters):
        NotImplementedError

class rsa_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class rsa_majoration_pension(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH
    label = 'Majoration de pension'

    def formula(individu, period, parameters):
        NotImplementedError

class rsa_pension(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés agricoles'
    definition_period = YEAR

    def formula(individu, period, parameters):
        rsa = parameters(period).retraite.rsa
        taux_annuite_base = rsa.taux_annuite_base
        taux_annuite_supplementaire = rsa.taux_annuite_supplementaire
        duree_stage = rsa.stage_requis
        age_elig = rsa.age_legal
        periode_remplacement_base = rsa.periode_remplacement_base
        plaf_taux_pension = rsa.plaf_taux_pension
        smag = parameters(period).marche_travail.smag * 25
        duree_stage_validee = duree_assurance > 4 * duree_stage
        pension_min = rsa.pension_min
        salaire_reference = individu('rsa_salaire_reference', period)
        montant = pension_generique(duree_assurance, sal_ref, taux_annuite_base, taux_annuite_supplementaire, duree_stage, age_elig, periode_remplacement_base, plaf_taux_pension)
        elig_age = age > age_elig
        elig = duree_stage_validee * elig_age * (salaire_reference > 0)
        montant_percu = max_(montant, pension_min * smag)
        pension = elig * montant_percu
        return pension

class rsa_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        taux_de_liquidation = individu('rsa_taux_de_liquidation', period)
        salaire_de_reference = individu('rsa_salaire_de_reference', period)
        return (taux_de_liquidation * salaire_de_reference,)

class rsa_pension_maximale(Variable):
    value_type = float
    default_value = np.inf
    entity = Individu
    definition_period = YEAR
    label = 'Pension maximale'

    def formula(individu, period, parameters):
        NotImplementedError

class rsa_pension_minimale(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension minimale'

    def formula(individu, period, parameters):
        NotImplementedError

class rsa_pension_servie(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension servie'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsa_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        pension_au_31_decembre_annee_precedente = individu('rsa_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).rsa.revalarisation_pension_servie
        pension = individu('rsa_pension_au_31_decembre', period)
        return revalorise(pension_au_31_decembre_annee_precedente, pension, annee_de_liquidation, revalorisation, period)

class rsa_salaire_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = 'Salaire de base (salaire brut)'
    set_input = set_input_divide_by_period

class rsa_salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    definition_period = ETERNITY
    label = 'Salaire de référence'

class rsa_salaire_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés agricoles'
    definition_period = YEAR

    def formula(individu, period):
        base_declaration_rsa = 180
        base_liquidation_rsa = 300
        k = 3
        mean_over_largest = make_mean_over_largest(k)
        salaire = apply_along_axis(mean_over_largest, axis=0, arr=vstack([individu('salaire', period=periods.period('year', year)) for year in range(period.start.year, period.start.year - n, -1)]))
        salaire_refererence = salaire * base_liquidation_rsa / base_declaration_rsa
        return salaire_refererence

class rsa_taux_de_liquidation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Taux de liquidation de la pension'

    def formula(individu, period, parameters):
        bareme_annuite = parameters(period).retraite.rsa.bareme_annuite
        duree_assurance = individu('rsa_duree_assurance', period)
        taux_annuite = bareme_annuite.calc(duree_assurance)
        return taux_annuite
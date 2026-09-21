"""Abstract regimes definition."""
import numpy as np
from openfisca_core.errors.variable_not_found_error import VariableNotFoundError
from openfisca_core.model_api import ETERNITY, MONTH, YEAR, Variable, date, max_, min_, set_input_divide_by_period
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.tools import revalorise
'Régime des salariés non agricoles.'
from numpy import apply_along_axis, vstack
from openfisca_core.model_api import ADD, YEAR, Enum, Variable, apply_thresholds
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from openfisca_tunisia_pension.tools import make_mean_over_largest

class rsna_RSNATypesRaisonDepartAnticipe(Enum):
    __order__ = 'non_concerne licenciement_economique usure_prematuree_organisme mere_3_enfants convenance_personnelle'
    non_concerne = 'Non concerné'
    licenciement_economique = 'Licenciement économique avec au minimum 60 mois de cotisations (20 trimestres)'
    usure_prematuree_organisme = "Usure prématurée de l'organisme médicalement constatée avec au minimum 60 mois de cotisations (20 trimestres)"
    mere_3_enfants = "Femme salariée, mère de 3 enfants en vie, justifiant d'au moins 180 mois de cotisations (60 trimestres)"
    convenance_personnelle = 'Convenance personnelle, avec 360 mois de cotisations (120 trimestres)'

class rsna_cotisation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'cotisation retraite employeur'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_duree_assurance(Variable):
    value_type = int
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (trimestres validés)"

class rsna_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Durée d'assurance (en trimestres validés l'année considérée)"

class rsna_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu est éligible à une pension CNRPS"
    definition_period = YEAR

    def formula(individu, period, parameters):
        duree_assurance = individu('rsna_duree_assurance', period=period)
        salaire_de_reference = individu('rsna_salaire_de_reference', period=period)
        age = individu('age', period=period)
        rsna = parameters(period).retraite.rsna
        duree_stage_accomplie = duree_assurance > 4 * rsna.stage_requis
        critere_age_verifie = age >= rsna.age_legal
        return duree_stage_accomplie * critere_age_verifie * (salaire_de_reference > 0)

class rsna_liquidation_date(Variable):
    value_type = date
    entity = Individu
    definition_period = ETERNITY
    label = 'Date de liquidation'
    default_value = date(2250, 12, 31)

class rsna_majoration_pension(Variable):
    value_type = int
    entity = Individu
    definition_period = MONTH
    label = 'Majoration de pension'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_pension(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension'

    def formula(individu, period):
        pension_brute = individu('rsna_pension_brute', period)
        eligible = individu('rsna_eligible', period)
        try:
            pension_minimale = individu('rsna_pension_minimale', period)
        except VariableNotFoundError:
            pension_minimale = 0
        try:
            pension_maximale = individu('rsna_pension_maximale', period)
        except (VariableNotFoundError, NotImplementedError):
            return max_(pension_brute, pension_minimale)
        return eligible * min_(pension_maximale, max_(pension_brute, pension_minimale))

class rsna_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension brute'

    def formula(individu, period, parameters):
        taux_de_liquidation = individu('rsna_taux_de_liquidation', period)
        salaire_de_reference = individu('rsna_salaire_de_reference', period)
        return (taux_de_liquidation * salaire_de_reference,)

class rsna_pension_maximale(Variable):
    value_type = float
    default_value = np.inf
    entity = Individu
    definition_period = YEAR
    label = 'Pension maximale'

    def formula(individu, period, parameters):
        NotImplementedError

class rsna_pension_minimale(Variable):
    value_type = float
    default_value = 0
    entity = Individu
    definition_period = YEAR
    label = 'Pension minimale'

    def formula(individu, period, parameters):
        rsna = parameters(period).retraite.rsna
        pension_minimale = rsna.pension_minimale
        smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
        duree_assurance = individu('rsna_duree_assurance', period)
        return apply_thresholds(duree_assurance / 4, [rsna.stage_derog, rsna.stage_requis], [0, pension_minimale.inf * smig_annuel, pension_minimale.sup * smig_annuel])

class rsna_pension_servie(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Pension servie'

    def formula(individu, period, parameters):
        annee_de_liquidation = individu('rsna_liquidation_date', period).astype('datetime64[Y]').astype(int) + 1970
        if all(annee_de_liquidation > period.start.year):
            return individu.empty_array()
        last_year = period.last_year
        pension_au_31_decembre_annee_precedente = individu('rsna_pension_au_31_decembre', last_year)
        revalorisation = parameters(period).rsna.revalarisation_pension_servie
        pension = individu('rsna_pension_au_31_decembre', period)
        return revalorise(pension_au_31_decembre_annee_precedente, pension, annee_de_liquidation, revalorisation, period)

class rsna_salaire_de_base(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = 'Salaire de base (salaire brut)'
    set_input = set_input_divide_by_period

class rsna_salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires de référence du régime des salariés non agricoles'
    definition_period = YEAR

    def formula(individu, period):
        k = 10
        mean_over_largest = make_mean_over_largest(k=k)
        n = 40
        salaire_refererence = apply_along_axis(mean_over_largest, axis=0, arr=vstack([individu('rsna_salaire_de_base', period=year, options=[ADD]) for year in range(period.start.year, period.start.year - n, -1)]))
        return salaire_refererence

class rsna_taux_de_liquidation(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = 'Taux de liquidation de la pension'

    def formula(individu, period, parameters):
        bareme_annuite = parameters(period).retraite.rsna.bareme_annuite
        duree_assurance = individu('rsna_duree_assurance', period)
        taux_annuite = bareme_annuite.calc(duree_assurance)
        return taux_annuite
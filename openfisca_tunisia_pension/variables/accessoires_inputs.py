# Third Party
from openfisca_core.model_api import MONTH, Variable, set_input_dispatch_by_period

# First Party
from openfisca_tunisia_pension.entities import Individu


class nombre_enfants_charge(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants à charge pour les indemnités familiales"
    set_input = set_input_dispatch_by_period


class nombre_enfants_indemnite_familiale_droit_acquis(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants au-delà du troisième rang ayant acquis le droit à l'indemnité familiale avant le 1er janvier 1989"
    set_input = set_input_dispatch_by_period
    documentation = """
    La loi n° 88-39 du 6 mai 1988 limite l'indemnité familiale aux trois premiers enfants
    à compter du 1er janvier 1989, mais « ne s'applique pas aux droits acquis
    antérieurement » à cette date. Le décret n° 96-1906, article 2, fixe encore en 1996 le
    taux du « quatrième enfant ayant acquis ce droit antérieurement au 1er janvier 1989 ».

    La valeur par défaut est 0 : sans déclaration, aucun enfant au-delà du troisième
    n'ouvre droit depuis 1989. Elle est sans effet sur les périodes antérieures, où la
    limitation ne s'applique pas.
    """


class nombre_enfants_handicapes_au_dela_du_troisieme_rang(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants handicapés venant après le troisième rang"
    set_input = set_input_dispatch_by_period
    documentation = """
    L'enfant handicapé ouvre droit à l'indemnité familiale quel que soit son rang
    (loi n° 81-46 du 29 mai 1981, article 18 ; décret n° 96-1906, article 3, qui fixe son
    taux à celui du quatrième enfant). La limitation aux trois premiers enfants ne lui est
    donc pas opposable.

    La valeur par défaut est 0.
    """


class mere_divorcee_garde_enfants(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Mère divorcée ayant obtenu la garde de ses enfants"
    set_input = set_input_dispatch_by_period


class conjoint_sans_revenu(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Conjoint sans aucun revenu (activité, retraite, ou invalidité)"
    set_input = set_input_dispatch_by_period

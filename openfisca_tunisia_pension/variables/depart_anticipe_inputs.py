# Third Party
from openfisca_core.model_api import YEAR, Variable, set_input_dispatch_by_period

# First Party
from openfisca_tunisia_pension.entities import Individu


class mere_3_enfants(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Mère de 3 enfants remplissant les conditions de limite d'âge"
    set_input = set_input_dispatch_by_period


class depart_anticipe_sur_demande(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Départ anticipé sur demande"
    set_input = set_input_dispatch_by_period


class invalidite_physique(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Mise à la retraite pour invalidité physique"
    set_input = set_input_dispatch_by_period


class fonction_astreignante(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Occupe une fonction astreignante"
    set_input = set_input_dispatch_by_period


class cadre_actif(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Appartient au cadre actif"
    set_input = set_input_dispatch_by_period


class militaire_ou_douane(Variable):
    value_type = bool
    entity = Individu
    definition_period = YEAR
    label = "Est de corps militaire ou douanier"
    set_input = set_input_dispatch_by_period


class duree_service_cadre_actif(Variable):
    value_type = int
    default_value = 0
    entity = Individu
    definition_period = YEAR
    label = "Durée de service dans le cadre actif ou travaux pénibles (en années)"
    set_input = set_input_dispatch_by_period


class duree_service_militaire(Variable):
    value_type = int
    default_value = 0
    entity = Individu
    definition_period = YEAR
    label = "Durée de service militaire (en années)"
    set_input = set_input_dispatch_by_period

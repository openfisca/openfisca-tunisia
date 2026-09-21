# Third Party
from openfisca_core.model_api import YEAR, Variable

# First Party
from openfisca_tunisia_pension.entities import Individu


class cnss_duree_assurance_annuelle(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = YEAR
    label = "Durée d'assurance CNSS (en trimestres validés l'année considérée)"


class cnss_duree_assurance(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = YEAR
    label = "Durée d'assurance totale à la CNSS (trimestres validés)"

    def formula(individu, period):
        duree_effective = individu("cnss_duree_assurance_annuelle", period)
        return duree_effective

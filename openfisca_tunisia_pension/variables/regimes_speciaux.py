# Third Party
from openfisca_core.model_api import (
    ADD,
    MONTH,
    YEAR,
    Variable,
    min_,
    set_input_dispatch_by_period,
)

# First Party
from openfisca_tunisia_pension.entities import Individu


class gouverneur_duree_service(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = YEAR
    label = "Durée de service en tant que Gouverneur (en trimestres)"


class gouverneur_remuneration(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Eléments permanents de la rémunération de gouverneur"
    set_input = set_input_dispatch_by_period


class gouverneur_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Pension brute servie au titre du régime des Gouverneurs"

    def formula(individu, period, parameters):
        duree_trimestres = individu("gouverneur_duree_service", period)
        remuneration_annuelle = individu(
            "gouverneur_remuneration", period, options=[ADD]
        )

        # "Le droit à la pension dans ce régime s’acquiert sans condition d’âge après au moins deux années"
        # 2 années = 8 trimestres
        eligible = duree_trimestres >= 8

        # "Chaque période de trois mois de service en qualité de gouverneur donne droit à 1,5%"
        # Max limit is 90% -> "le montant de la pension accordée ne peut excéder 90%"
        taux = min_(duree_trimestres * 0.015, 0.90)

        return eligible * remuneration_annuelle * taux


class depute_nombre_legislatures(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = YEAR
    label = "Nombre de législatures accomplies en tant que Député ou membre de la Chambre des conseillers"


class depute_indemnite(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Indemnité parlementaire permanente"
    set_input = set_input_dispatch_by_period


class depute_pension_brute(Variable):
    value_type = float
    entity = Individu
    definition_period = YEAR
    label = "Pension brute servie au titre du régime des Députés et Conseillers"

    def formula(individu, period, parameters):
        legislatures = individu("depute_nombre_legislatures", period)
        indemnite_annuelle = individu("depute_indemnite", period, options=[ADD])

        # "Le droit d’un député à une pension [...] est acquis après accomplissement d’une législature complète"
        eligible = legislatures >= 1

        # 1 leg = 30%, 2 leg = 60%, 3+ = 90%
        # "le montant de la pension accordée ne peut excéder 90%"
        taux = min_(legislatures * 0.30, 0.90)

        return eligible * indemnite_annuelle * taux

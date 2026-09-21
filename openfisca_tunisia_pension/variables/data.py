# Third Party
from openfisca_core.model_api import ETERNITY, YEAR, Enum, Variable, date

# First Party
from openfisca_tunisia_pension.entities import Individu


class age(Variable):
    value_type = int
    entity = Individu
    label = "Âge"
    definition_period = YEAR


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = "Date de naissance"
    definition_period = ETERNITY


class TypesRegimeSecuriteSociale(Enum):
    __order__ = "rsna rsa rsaa rtns rtte re rtfr raci salarie_cnrps pensionne_cnrps"
    # Needed to preserve the enum order in Python 2

    rsna = "Régime des Salariés Non Agricoles"
    rsa = "Régime des Salariés Agricoles"
    rsaa = "Régime des Salariés Agricoles Amélioré"
    rtns = "Régime des Travailleurs Non Salariés (secteurs agricole et non agricole)"
    rtte = "Régime des Travailleurs Tunisiens à l'Etranger"
    re = "Régime des Etudiants, diplômés de l'enseignement supérieur et stagiaires"
    rtfr = "Régime des Travailleurs à Faibles Revenus (gens de maisons, travailleurs de chantiers, et artisans travaillant à la pièce)"
    raci = "Régime des Artistes, Créateurs et Intellectuels"
    salarie_cnrps = "Régime des salariés affiliés à la Caisse Nationale de Retraite et de Prévoyance Sociale"
    pensionne_cnrps = "Régime des salariés des pensionnés de la Caisse Nationale de Retraite et de Prévoyance Sociale"
    # references :
    # http://www.social.gov.tn/index.php?id=49&L=0
    # http://www.paie-tunisie.com/412/fr/83/reglementations/regimes-de-securite-sociale.aspx


class regime_securite_sociale(Variable):
    value_type = Enum
    possible_values = TypesRegimeSecuriteSociale
    default_value = TypesRegimeSecuriteSociale.rsna
    entity = Individu
    label = "Régime de sécurité sociale du retraité"
    definition_period = YEAR

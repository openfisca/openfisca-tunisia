"""Prélèvements patronaux sur les salaires autres que les cotisations sociales.

- taxe de formation professionnelle (TFP) ;
- contribution au fonds de promotion du logement pour les salariés (FOPROLOS).

Les deux sont à la charge de l'employeur et assises sur les salaires qu'il verse. Elles ne
sont pas des cotisations de sécurité sociale et restent hors de `cotisations_employeur` ;
elles entrent dans le coût du travail (`salaire_super_brut`).
"""

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore
from openfisca_tunisia.variables.prelevements_obligatoires.cotisations_sociales import (
    TypesRegimeSecuriteSocialeCotisant,
)


class employeur_industrie_manufacturiere(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "L'employeur relève des industries manufacturières (taux réduit de la taxe de formation professionnelle)"
    reference = "Loi n° 88-145 du 31 décembre 1988, portant loi de finances pour la gestion 1989, article 30 ; liste du décret n° 94-492"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class employeur_redevable_tfp(Variable):
    value_type = bool
    entity = Individu
    label = "L'employeur est redevable de la taxe de formation professionnelle"
    reference = "Décret du 12 janvier 1956, article 27 ; code du travail, article 364"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Valeur par défaut déduite du régime de sécurité sociale du salarié, à saisir pour tout
    autre cas. La taxe est due par les employeurs passibles de la patente, puis de l'impôt
    sur les bénéfices industriels et commerciaux ou de l'impôt sur les sociétés (et sur les
    bénéfices non commerciaux depuis la loi de finances pour 2003, articles 35-36), hors
    régime forfaitaire. L'État, les collectivités locales et les établissements publics
    administratifs sont hors de ce champ : aucun texte ne les exonère, leur sortie se déduit
    du critère. Par défaut :
    - salarié du régime des salariés non agricoles (CNSS) : redevable ;
    - salarié affilié à la CNRPS : non redevable (employeur public) ;
    - autres régimes, dont les régimes agricoles : non redevable.
    Les cas particuliers se saisissent : entreprise publique affiliée à la CNRPS,
    exonération des caisses sociales (CNSS, CNRPS, CNAM) depuis le 1er janvier 2008 (loi
    n° 2007-70, article 40), exonérations des régimes d'incitation.
    """

    def formula(individu, period):
        regime = individu("regime_securite_sociale_cotisant", period)
        return regime == TypesRegimeSecuriteSocialeCotisant.rsna


class employeur_redevable_foprolos(Variable):
    value_type = bool
    entity = Individu
    label = "L'employeur est redevable de la contribution au FOPROLOS"
    reference = "Loi n° 77-54 du 3 août 1977, article premier"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Valeur par défaut déduite du régime de sécurité sociale du salarié, à saisir pour tout
    autre cas. La contribution est due par tout employeur public ou privé, à l'exception des
    exploitants agricoles privés. Par défaut :
    - salarié du régime des salariés non agricoles (CNSS) : redevable ;
    - salarié affilié à la CNRPS : redevable (l'État l'est expressément) ;
    - autres régimes, dont les régimes agricoles : non redevable.
    """

    def formula(individu, period):
        regime = individu("regime_securite_sociale_cotisant", period)
        return (regime == TypesRegimeSecuriteSocialeCotisant.rsna) + (
            regime == TypesRegimeSecuriteSocialeCotisant.salarie_cnrps
        )


class taxe_formation_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = "Taxe de formation professionnelle (employeur)"
    reference = "https://www.pist.tn/jort/1988/1988F/Jo08788.pdf"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_1967_01_01(individu, period, parameters):
        # Avant le 1er janvier 1967, le taux n'est pas établi : la variable vaut zéro.
        tfp = parameters(period.start).prelevements_sociaux.autres.tfp
        assiette = individu("assiette_cotisations_sociales", period)
        redevable = individu("employeur_redevable_tfp", period)
        industrie = individu("employeur_industrie_manufacturiere", period)
        taux = where(
            industrie, tfp.taux_industries_manufacturieres, tfp.taux_autres_secteurs
        )
        return redevable * taux * assiette


class contribution_foprolos(Variable):
    value_type = float
    entity = Individu
    label = "Contribution au fonds de promotion du logement pour les salariés (FOPROLOS, employeur)"
    reference = "https://www.pist.tn/jort/1977/1977F/Jo05377.pdf"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_1977_08_01(individu, period, parameters):
        taux = parameters(period.start).prelevements_sociaux.autres.foprolos.taux
        assiette = individu("assiette_cotisations_sociales", period)
        redevable = individu("employeur_redevable_foprolos", period)
        return redevable * taux * assiette


class autres_prelevements_employeur(Variable):
    value_type = float
    entity = Individu
    label = "Prélèvements patronaux sur les salaires autres que les cotisations sociales (TFP et FOPROLOS)"
    definition_period = MONTH

    def formula(individu, period):
        return individu("taxe_formation_professionnelle", period) + individu(
            "contribution_foprolos", period
        )

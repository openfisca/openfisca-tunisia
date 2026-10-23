"""Allocations aux personnes allergiques au gluten et atteintes de xeroderma pigmentosum.

Loi de finances pour 2025, article 26 ; loi de finances pour 2026, article 35 ; arrêtés
conjoints du 30 juillet 2025 et du 14 juillet 2026.
"""

from openfisca_tunisia.variables.base import *


class allergie_gluten(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Allergie au gluten attestée selon la procédure de l'allocation pour dépenses alimentaires"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class xeroderma_pigmentosum(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Maladie xeroderma pigmentosum attestée selon la procédure de l'allocation pour équipements de protection"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class couverture_sociale_legale(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Bénéficie d'un régime légal de couverture sociale, à titre d'assuré ou d'ayant droit"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.pist.tn/jort/2026/2026F/Jo0702026.pdf"


class menage_amen_social_pauvre_ou_revenu_limite(Variable):
    value_type = bool
    entity = Menage
    label = "Famille pauvre ou à revenu limité inscrite au programme Amen social"
    definition_period = MONTH

    def formula(menage, period):
        # Correspondance retenue, à valider : familles pauvres → carte AMG1, familles à
        # revenu limité → carte AMG2, comme pour l'allocation familiale non contributive.
        return menage("amg_1", period) + menage("amg_2", period)


class allocation_allergie_gluten(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle pour les dépenses alimentaires des personnes allergiques au gluten"
    definition_period = MONTH
    reference = [
        "https://www.pist.tn/jort/2024/2024A/Ja1492024.pdf",
        "https://www.pist.tn/jort/2025/2025A/Ja1482025.pdf",
    ]

    def formula_2025_01(individu, period, parameters):
        # Montant de l'article 26 de la loi de finances pour 2025, puis, au 1er janvier 2026,
        # de l'article 35 de la loi de finances pour 2026 : la série du paramètre suppose que
        # le second remplace le premier (articulation non tranchée par les textes).
        eligible = individu.menage("menage_amen_social_pauvre_ou_revenu_limite", period)
        montant = parameters(period).prestations.non_contributives.allergie_gluten
        return individu("allergie_gluten", period) * eligible * montant


class allocation_xeroderma_pigmentosum(Variable):
    value_type = float
    entity = Individu
    label = "Allocation mensuelle pour les équipements de protection des personnes atteintes de xeroderma pigmentosum"
    definition_period = MONTH
    reference = [
        "https://www.pist.tn/jort/2025/2025A/Ja1482025.pdf",
        "https://www.pist.tn/jort/2026/2026F/Jo0702026.pdf",
    ]

    def formula_2026_07_19(individu, period, parameters):
        # Arrêté conjoint du 14 juillet 2026, article premier, exécutoire le 19 juillet 2026 :
        # réservée aux personnes sans régime légal de couverture sociale. Un mois ne bascule
        # sur cette formule que s'il commence le 19 juillet 2026 ou après : juillet 2026 reste
        # sous la règle de la loi seule, la condition s'applique à partir d'août 2026.
        montant = parameters(period).prestations.non_contributives.xeroderma_pigmentosum
        sans_couverture = not_(individu("couverture_sociale_legale", period))
        return individu("xeroderma_pigmentosum", period) * sans_couverture * montant

    def formula_2026_01(individu, period, parameters):
        # Loi de finances pour 2026, article 35 : sans condition de ressources ni de couverture.
        montant = parameters(period).prestations.non_contributives.xeroderma_pigmentosum
        return individu("xeroderma_pigmentosum", period) * montant

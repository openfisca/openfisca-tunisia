"""Rémunération minimale effectivement servie, indemnités spéciales comprises."""

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


# Du 1er août 1989 au 30 avril 1992, le salaire minimum légal ne dit pas tout ce qui était
# servi : une indemnité spéciale s'y ajoute, sans en faire partie. Les décrets n° 89-1551
# (art. 4 et 5), n° 89-1552, n° 91-1316 et n° 91-1317 l'excluent expressément de l'assiette
# des cotisations, de celle des prestations de sécurité sociale et de l'impôt. Le décret
# n° 92-1299 (art. 3) l'intègre au SMIG au 1er mai 1992, et le décret n° 92-1300 (art. 3) fait
# de même pour le SMAG ; les paramètres tombent alors à zéro.
#
# Ces variables exposent donc la rémunération minimale SERVIE, distincte du salaire minimum
# LÉGAL que portent `marche_travail.smig_*` et `marche_travail.smag_journalier`. Elles ne sont
# consommées par aucune assiette : les y brancher contredirait les textes qui les en excluent.
# C'est précisément ce que demande l'issue #406 — rendre la grandeur lisible sans toucher aux
# assiettes.
#
# Les formules commencent au 1er août 1989 parce que les paramètres d'indemnité n'existent pas
# avant : les lire plus tôt lèverait une ParameterNotFoundError.


class remuneration_minimale_servie_48h_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Rémunération minimale mensuelle servie au régime de 48 heures, indemnité spéciale comprise"
    definition_period = MONTH
    reference = "https://www.pist.tn/jort/1989/1989F/Jo06989.pdf"

    def formula_1989_08_01(individu, period, parameters):
        marche_travail = parameters(period.start).marche_travail
        return (
            marche_travail.smig_48h_mensuel + marche_travail.indemnite_speciale_smig
        ) * individu.filled_array(1.0)


class remuneration_minimale_servie_40h_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Rémunération minimale mensuelle servie au régime de 40 heures, indemnité spéciale comprise"
    definition_period = MONTH
    reference = "https://www.pist.tn/jort/1989/1989F/Jo06989.pdf"

    def formula_1989_08_01(individu, period, parameters):
        marche_travail = parameters(period.start).marche_travail
        return (
            marche_travail.smig_40h_mensuel + marche_travail.indemnite_speciale_smig
        ) * individu.filled_array(1.0)


class remuneration_minimale_servie_agricole_journaliere(Variable):
    value_type = float
    entity = Individu
    label = "Rémunération minimale journalière servie dans l'agriculture, indemnité spéciale comprise"
    definition_period = MONTH
    reference = "https://www.pist.tn/jort/1989/1989F/Jo06989.pdf"

    def formula_1989_08_01(individu, period, parameters):
        marche_travail = parameters(period.start).marche_travail
        return (
            marche_travail.smag_journalier + marche_travail.indemnite_speciale_smag
        ) * individu.filled_array(1.0)

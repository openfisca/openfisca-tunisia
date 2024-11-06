from __future__ import division

from numpy import zeros

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class TypesRegimeSecuriteSociale(Enum):
    __order__ = 'rsna rsa rsaa rtns rtte re rtfr raci salarie_cnrps pensionne_cnrps'
    # Needed to preserve the enum order in Python 2

    rsna = 'Régime des Salariés Non Agricoles'
    rsa = 'Régime des Salariés Agricoles'
    rsaa = 'Régime des Salariés Agricoles Amélioré'
    rtns = 'Régime des Travailleurs Non Salariés (secteurs agricole et non agricole)'
    rtte = "Régime des Travailleurs Tunisiens à l'Etranger"
    re = "Régime des Etudiants, diplômés de l'enseignement supérieur et stagiaires"
    rtfr = 'Régime des Travailleurs à Faibles Revenus (gens de maisons, travailleurs de chantiers, et artisans travaillant à la pièce)'
    raci = 'Régime des Artistes, Créateurs et Intellectuels'
    salarie_cnrps = 'Régime des salariés affilés à la Caisse Nationale de Retraite et de Prévoyance Sociale'
    pensionne_cnrps = 'Régime des salariés des pensionnés de la Caisse Nationale de Retraite et de Prévoyance Sociale'
    # references :
    # http://www.social.gov.tn/index.php?id=49&L=0
    # http://www.paie-tunisie.com/412/fr/83/reglementations/regimes-de-securite-sociale.aspx


def compute_cotisation(individu, period, cotisation_type = None, bareme_name = None, parameters = None):
    assert cotisation_type in ['employeur', 'salarie']

    assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
    regime_securite_sociale = individu('regime_securite_sociale', period)
    baremes_by_regime = parameters(period.start).cotisations_sociales
    cotisation = zeros(len(assiette_cotisations_sociales))
    types_regime_securite_sociale = regime_securite_sociale.possible_values

    for regime in types_regime_securite_sociale:
        if 'cotisations_{}'.format(cotisation_type) not in baremes_by_regime[regime.name]._children:
            continue
        baremes_by_name = getattr(
            baremes_by_regime[regime.name],
            'cotisations_{}'.format(cotisation_type),
            )

        if bareme_name in ['maladie', 'maternite', 'deces']:
            if 'assurances_sociales' in baremes_by_name._children:
                baremes_assurances_sociales = getattr(baremes_by_name, 'assurances_sociales')
                bareme = getattr(baremes_assurances_sociales, bareme_name)

            else:
                if bareme_name not in baremes_by_name._children:
                    continue
                bareme = getattr(baremes_by_name, bareme_name)

        else:
            if bareme_name not in baremes_by_name._children:
                continue
            bareme = getattr(baremes_by_name, bareme_name)

        if bareme is not None:
            cotisation += bareme.calc(
                assiette_cotisations_sociales * (regime_securite_sociale == regime),
                )

    return - cotisation


class assiette_cotisations_sociales(Variable):
    value_type = float
    entity = Individu
    label = 'Assiette des cotisations sociales'
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu('salaire_de_base', period)
            + individu('primes', period)
            )


class regime_securite_sociale(Variable):
    value_type = Enum
    possible_values = TypesRegimeSecuriteSociale
    default_value = TypesRegimeSecuriteSociale.rsna
    entity = Individu
    label = 'Régime de sécurité sociale du salarié'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class cotisations_sociales(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisations sociales'
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu('cotisations_employeur', period)
            + individu('cotisations_salarie', period)
            )


class cotisations_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation sociales employeur'
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu('accident_du_travail_employeur', period)
            + individu('deces_employeur', period)
            + individu('fonds_special_etat', period)
            + individu('famille_employeur', period)
            + individu('maladie_employeur', period)
            + individu('maternite_employeur', period)
            + individu('protection_sociale_travailleurs_employeur', period)
            + individu('retraite_employeur', period)
            )


class cotisations_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation sociales salarié'
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu('accident_du_travail_salarie', period)
            + individu('deces_salarie', period)
            + individu('famille_salarie', period)
            + individu('maladie_salarie', period)
            + individu('maternite_salarie', period)
            + individu('protection_sociale_travailleurs_salarie', period)
            + individu('retraite_salarie', period)
            + individu('ugtt', period)
            )


class accident_du_travail_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation accidents du travail et maladies professionnelles (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'accident_du_travail',
            parameters = parameters
            )


class accident_du_travail_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation accidents du travail et maladies professionnelles (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'accident_du_travail',
            parameters = parameters
            )


class deces_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales: décès (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'deces',
            parameters = parameters
            )


class deces_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales: décès (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'deces',
            parameters = parameters
            )


class famille_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation sociale allocations familiales (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'famille',
            parameters = parameters
            )


class famille_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation sociale allocations familiales (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'famille',
            parameters = parameters
            )


class fonds_special_etat(Variable):
    value_type = float
    entity = Individu
    label = "Fonds spécial de l'Etat"
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fonds_special_etat',
            parameters = parameters
            )


class maladie_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales: maladie (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            parameters = parameters
            )


class maladie_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales: maladie (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maladie',
            parameters = parameters
            )


class maternite_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales : maternité (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maternite',
            parameters = parameters
            )


class maternite_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation assurances sociales : maternité (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maternite',
            parameters = parameters
            )


class protection_sociale_travailleurs_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation protection sociale des travailleurs (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'protection_sociale_travailleurs',
            parameters = parameters
            )


class protection_sociale_travailleurs_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation protection sociale des travailleurs (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'protection_sociale_travailleurs',
            parameters = parameters
            )


class retraite_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation pensions de retraite (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'retraite',
            parameters = parameters
            )


class retraite_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation pensions de retraite (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'retraite',
            parameters = parameters
            )


class salaire_imposable(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire imposable'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return (
            individu('assiette_cotisations_sociales', period)
            + individu('cotisations_salarie', period)
            )


class salaire_net_a_payer(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire net à payer (fiche de paie)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return (
            individu('salaire_imposable', period)
            + individu('irpp_mensuel_salarie', period)
            )


class salaire_super_brut(Variable):
    value_type = float
    entity = Individu
    label = 'Salaires super bruts'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        return (
            individu('salaire_de_base', period = period)
            + individu('primes', period = period)
            - individu('cotisations_employeur', period = period)  # Cotisations employeur sont négatives
            )


class ugtt(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation syndicale UGTT'
    definition_period = MONTH

    def formula(individu, period):
        # TODO put this value (3) in parameters
        return -3 * (individu('regime_securite_sociale', period) == TypesRegimeSecuriteSociale.salarie_cnrps)

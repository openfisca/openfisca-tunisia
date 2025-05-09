
from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class TypesRegimeSecuriteSocialeCotisant(Enum):
    __order__ = 'neant rsna rsa rsaa rtns rtte re rtfr raci salarie_cnrps pensionne_cnrps'
    # Needed to preserve the enum order in Python 2
    neant = 'Néant'
    rsna = 'Régime des salariés non agricoles'
    rsa = 'Régime des salariés agricoles'
    rsaa = 'Régime des salariés agricoles amélioré'
    rtns = 'Régime des travailleurs non salariés (secteurs agricole et non agricole)'
    rtte = "Régime des travailleurs tunisiens à l'étranger"
    re = "Régime des étudiants, diplômés de l'enseignement supérieur et stagiaires"
    rtfr = 'Régime des travailleurs à faibles revenus (gens de maisons, travailleurs de chantiers, et artisans travaillant à la pièce)'
    raci = 'Régime des artistes, créateurs et intellectuels'
    salarie_cnrps = 'Régime des salariés affilés à la Caisse nationale de retraite et de prévoyance sociale (CNRPS)'
    pensionne_cnrps = 'Régime des pensionnés affilés à la Caisse nationale de retraite et de prévoyance sociale (CNRPS)'
    # references :
    # http://www.social.gov.tn/index.php?id=49&L=0
    # http://www.paie-tunisie.com/412/fr/83/reglementations/regimes-de-securite-sociale.aspx


class TypesRegimeSecuriteSocialeRetraite(Enum):
    __order__ = 'neant rsna rtte raci rtns_na rtns_a rtc rsa rsaa cnrps'
    # Needed to preserve the enum order in Python 2
    neant = 'Néant'
    rsna = 'Régime des salariés non agricoles'
    rtte = "Régime des travailleurs tunisiens à l'étranger"
    raci = 'Régime des artistes, créateurs etiIntellectuels'
    rtns_na = 'Régime des travailleurs non salariés des secteurs non agricoles'
    rtns_a = 'Régime des travailleurs non salariés des secteurs agricoles'
    rtc = 'Régime des travailleurs de chantiers'
    rsa = 'Régime des salariés agricoles'
    rsaa = 'Régime des salariés agricoles amélioré'
    cnrps = 'Régime des pensionnés affilés à la Caisse Nationale de Retraite et de Prévoyance Sociale'
    # references :
    # http://www.social.gov.tn/index.php?id=49&L=0
    # http://www.paie-tunisie.com/412/fr/83/reglementations/regimes-de-securite-sociale.aspx


def compute_cotisation(individu, period, cotisation_type = None, bareme_name = None, parameters = None):
    assert cotisation_type in ['employeur', 'salarie']

    assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
    regime_securite_sociale_cotisant = individu('regime_securite_sociale_cotisant', period)
    baremes_by_regime = parameters(period.start).prelevements_sociaux.cotisations_sociales
    cotisation = individu.empty_array()
    types_regime_securite_sociale_cotisant = regime_securite_sociale_cotisant.possible_values

    for regime in types_regime_securite_sociale_cotisant:
        if regime.name == 'neant':
            continue
        if f'cotisations_{cotisation_type}' not in baremes_by_regime[regime.name]._children:
            continue
        baremes_by_name = getattr(
            baremes_by_regime[regime.name],
            f'cotisations_{cotisation_type}',
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
            if regime.name == 'rtfr':
                smic = parameters(period.start).marche_travail.smig_48h_mensuel
                bareme = bareme.copy()
                bareme = bareme.multiply_thresholds(smic)

            cotisation += bareme.calc(
                assiette_cotisations_sociales * (regime_securite_sociale_cotisant == regime),
                )

    return cotisation


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


class regime_securite_sociale_cotisant(Variable):
    value_type = Enum
    possible_values = TypesRegimeSecuriteSocialeCotisant
    default_value = TypesRegimeSecuriteSocialeCotisant.neant
    entity = Individu
    label = 'Régime de sécurité sociale du salarié'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class regime_securite_sociale_retraite(Variable):
    value_type = Enum
    possible_values = TypesRegimeSecuriteSocialeRetraite
    default_value = TypesRegimeSecuriteSocialeRetraite.neant
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
        cotisations_employeur = [
            'accident_du_travail_employeur',
            'deces_employeur',
            'fonds_special_etat',
            'famille_employeur',
            'maladie_employeur',
            'maternite_employeur',
            'protection_sociale_travailleurs_employeur',
            'retraite_employeur',
            ]
        return sum(individu(f'{cotisation}', period) for cotisation in cotisations_employeur)


class cotisations_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation sociales salarié'
    definition_period = MONTH

    def formula(individu, period):
        cotisations_salarie = [
            'accident_du_travail_salarie',
            'deces_salarie',
            'famille_salarie',
            'maladie_salarie',
            'maternite_salarie',
            'protection_sociale_travailleurs_salarie',
            'retraite_salarie',
            'soin_salarie',
            'ugtt',
            ]
        return sum(individu(f'{cotisation}', period) for cotisation in cotisations_salarie)


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


class soin_employeur(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation soin (employeur)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'soin',
            parameters = parameters
            )


class soin_salarie(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation soin (salarié)'
    definition_period = MONTH

    def formula(individu, period, parameters):
        return compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'soin',
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
            - individu('cotisations_salarie', period)
            )


class salaire_net_a_payer(Variable):
    value_type = float
    entity = Individu
    label = 'Salaire net à payer (fiche de paie)'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2018_01_01(individu, period):
        return (
            individu('salaire_imposable', period)
            - individu('irpp_salarie_preleve_a_la_source', period)
            - individu('contribution_sociale_solidarite_prelevee_a_la_source', period)
            )

    def formula(individu, period):
        return (
            individu('salaire_imposable', period)
            - individu('irpp_salarie_preleve_a_la_source', period)
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
            + individu('cotisations_employeur', period = period)  # Cotisations employeur sont négatives
            )


class ugtt(Variable):
    value_type = float
    entity = Individu
    label = 'Cotisation syndicale UGTT'
    definition_period = MONTH

    def formula(individu, period):
        # TODO put this value (3) in parameters
        return 3 * (individu('regime_securite_sociale_cotisant', period) == TypesRegimeSecuriteSocialeCotisant.salarie_cnrps)

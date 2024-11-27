from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class nb_enf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        TODO: fixme
        '''
        age = foyer_fiscal.members('age', period = period.first_month)
        famille = parameters(period.start).impot_revenu.deductions.fam
        # res =+ (
        #    (ag < 20) +
        #    (ag < 25)*not_(boursier)*()
        #    )
        condition = (age >= 0) * (age <= famille.age)
        return foyer_fiscal.sum(condition, role = FoyerFiscal.PERSONNE_A_CHARGE)


class nb_enf_sup(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants étudiants du supérieur non boursiers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants étudiants du supérieur non boursiers
        '''
        # age = foyer_fiscal.members('age', period = period)
        etudiant = foyer_fiscal.members('etudiant', period = period)
        boursier = foyer_fiscal.members('boursier', period = period)

        return foyer_fiscal.sum(etudiant * not_(boursier))


class nb_infirme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants infirmes"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre d'enfants infirmes
        '''
        age = foyer_fiscal.members('age', period = period)
        invalide = foyer_fiscal.members('invalide', period = period)

        return 0 * age * invalide


class nb_parents(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Nombre de parents'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        TODO: Nombre de parents
        '''
        return (
            (foyer_fiscal.declarant_principal('age', period) > 20)
            + (foyer_fiscal.declarant_principal('age', period) > 20)
            )


class chef_de_famille(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Indicatrice de chef de famille'
    definition_period = YEAR
    set_input = set_input_dispatch_by_period

    # Du point de vue fiscal, est considéré chef de famille :
    # - L’époux ;
    # - Le divorcé ou la divorcée qui a la garde des enfants (divorce & enfnats);
    # - Le veuf ou la veuve même sans enfants à charge;
    # - L’adoptant ou l’adoptante (adoptant). TODO
    # Cependant, l’épouse a la qualité de chef de famille dans les deux cas suivants :
    # - Lorsqu’elle justifie que le mari ne dispose d’aucune source de revenu durant l’année de réalisation du
    #   revenu. Tel est le cas d’une femme qui dispose d’un revenu et dont le mari, poursuivant des études, ne dispose
    #   d’aucun revenu propre. (marie & sexe & revenu_epoux == 0 & revenu_individu > 0) TODO
    # - Lorsque remariée, elle a la garde d’enfants issus d’un précédent mariage. TODO
    # Compte tenu de ce qui précède, n’est pas considéré comme chef de famille et ne bénéficie d’aucune déduction :
    # - Le célibataire ou la célibataire ;
    # - Le divorcé ou la divorcée qui n’a pas la garde des enfants ;
    # - La femme durant le mariage (sauf si elle dispose d’un revenu alors que son mari ne dispose d’aucun revenu) ;
    # - L’époux qui ne dispose pas d’une source de revenu. Dans ce cas, l’épouse acquiert la qualité de chef de famille
    #   au cas où elle réalise des revenus.

    def formula(foyer_fiscal, period):
        male = foyer_fiscal.declarant_principal('male', period = period)
        marie = foyer_fiscal.declarant_principal('marie', period = period)
        divorce = foyer_fiscal.declarant_principal('divorce', period = period)
        veuf = foyer_fiscal.declarant_principal('veuf', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        chef_de_famille = (
            veuf | (marie & male) | (divorce & (nb_enf > 0))  # | (marie & (not male)) |
            )
        return chef_de_famille

# Revenus catégoriels (voir répertoire idoine)
# 1. Bénéfices industriels et commerciaux  bic.py
# 2. Bénéfices des professions non commerciales  bnc.py
# 3. Bénéfices de l'exploitation agricole et de pêche beap.py
# 4. Revenus fonciers foncier.py
# 5. Traitements, salaires, indemnités, pensions et rentes viagères  tspr.py
# 6. Revenus de valeurs mobilières et de capitaux mobiliers  rvcm.py
# 7. revenus de source étrangère

# Déroulé du calcul de l'irpp


class rng(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net global'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal('bic', period = period)
            + foyer_fiscal('bnc', period = period)
            + foyer_fiscal('beap', period = period)
            + foyer_fiscal('revenus_fonciers', period = period)
            + foyer_fiscal('tspr', period = period)
            + foyer_fiscal('rvcm', period = period)
            + foyer_fiscal('revenus_source_etrangere', period = period)
            )


#############################
#    Déductions
#############################

# # 1/ Au titre des revenus et bénéfices provenant de l’activité

# # 2/ Autres déductions


class deduction_interets(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déductions intérêts issus de comptes spéciaux ou d'obligations"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        compte_special_epargne_banque = foyer_fiscal('compte_special_epargne_banque')
        compte_special_epargne_cent = foyer_fiscal('compte_special_epargne_cent')
        emprunt_obligataire = foyer_fiscal('emprunt_obligataire')
        deductions = parameters(period).impot_revenu.deductions
        return max_(
            max_(
                (
                    max_(compte_special_epargne_banque, deductions.banq.plaf)
                    + max_(compte_special_epargne_cent, deductions.cent.plaf)
                    ),
                deductions.banq.plaf,
                )
            + max_(emprunt_obligataire, deductions.oblig.plaf),
            deductions.oblig.plaf,
            )


class deduction_famille(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déductions pour situation et charges de famille'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        # rng = foyer_fiscal('rng', period = period)
        chef_de_famille = foyer_fiscal('chef_de_famille', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        # nb_parents = foyer_fiscal('nb_parents', period = period)
        fam = parameters(period.start).impot_revenu.deductions.fam
        #  chef de famille
        chef_de_famille = fam.chef_de_famille * chef_de_famille

        enf = (nb_enf >= 1) * fam.enf1 + (nb_enf >= 2) * fam.enf2 + (nb_enf >= 3) * fam.enf3 + (nb_enf >= 4) * fam.enf4

        #    sup = P.enf_sup * nb_enf_sup
        #    infirme = P.infirme * nb_infirme
        #    parent = min_(P.parent_taux * rng, P.parent_max)

        #    return chef_de_famille + enf + sup + infirme + parent
        res = chef_de_famille + enf
        return res


class deduction_rente(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Arrérages et rentes payées à titre obligatoire et gratuit'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        rente = foyer_fiscal('rente', period = period)

        return rente  # TODO:


class deduction_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Primes afférentes aux contrats d'assurance-vie collectifs ou individuels"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        primes_assurance_vie = foyer_fiscal.members('prime_assurance_vie', period = period)
        somme_primes_assurance_vie = foyer_fiscal.sum(primes_assurance_vie)
        marie = foyer_fiscal.declarant_principal('statut_marital', period = period)
        nb_enf = foyer_fiscal('nb_enf', period = period)
        assurance_vie = parameters(period.start).impot_revenu.deductions.assurance_vie
        deduction = min_(
            somme_primes_assurance_vie,
            assurance_vie.plaf + marie * assurance_vie.conj_plaf + nb_enf * assurance_vie.enf_plaf)
        return deduction


#     - Les remboursements des prêts universitaires en principal et en intérêts
#    - Revenus et bénéfices réinvestis dans les conditions et limites
#    prévues par la législation en vigueur dont notamment :
#     les revenus provenant de l'exportation, totalement pendant 10
#    ans à partir de la première opération d'exportation;
#     les revenus provenant de l’hébergement et de la restauration
#    des étudiants pendant dix ans ;
#     les revenus provenant du courtage international dans la limite
#    de 50% pendant 10 ans à partir de la première opération de courtage
#    international;
#     les montants déposés dans les comptes-épargne pour
#    l’investissement et dans les comptes-épargne en actions dans la
#    limite de 20.000D par an et sous réserve du minimum d’IR ;
#     la plus-value provenant des opérations de transmission des
#    entreprises en difficultés économiques ou des entreprises sous
#    forme de participations ou d’actifs pour départ du propriétaire à la
#    retraite ou pour incapacité de poursuivre la gestion et ce, sous
#    certaines conditions,
#     la plus-value provenant de l’apport d’une entreprise individuelle
#    au capital d’une société ;
#     les revenus réinvestis dans la souscription au capital des
#    entreprises dans les conditions prévues par la législation relative aux
#    incitations fiscales;
#     les revenus réinvestis dans la réalisation de projets
#    d’hébergement et de restauration universitaires sous réserve du
#    minimum d’IR.
#     Les revenus provenant de la location des terres agricoles
#    réservées aux grandes cultures objet de contrat de location conclus
#    pour une période minimale de trois ans.


class deduction_smig(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Déduction supplémentaire pour les salariés payés au SMIG et SMAG'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        chef = foyer_fiscal('chef_de_famille', period = period)

        return 0 * chef  # TODO: voir avec tspr


class deductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net imposable'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal('deduction_famille', period = period)
            + foyer_fiscal.declarant_principal('rente', period = period)
            + foyer_fiscal('deduction_assurance_vie', period = period)
            + foyer_fiscal.sum(foyer_fiscal.members('plus_value_cession_actifs_cotes_bourse', period = period))
            + foyer_fiscal.sum(foyer_fiscal.members('interets_acquisition_logement', period = period))
            )


class revenu_net_imposable(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net imposable'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses
        et charges professionnelles et des revenus non soumis à l'impôt
        '''
        return max_(
            foyer_fiscal('rng', period) - foyer_fiscal('deductions', period),
            0
            )


class impot_revenu_brut(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt brut avant non-imposabilité'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_net_imposable = foyer_fiscal('revenu_net_imposable', period = period)
        bareme = parameters(period.start).impot_revenu.bareme
        impot_revenu_brut = bareme.calc(revenu_net_imposable)
        return impot_revenu_brut


class exoneration(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = "Exoneration de l'impôt sur le revenu des personnes physiques"
    definition_period = YEAR
    end = '2016-12-31'

    def formula_2014(foyer_fiscal, period, parameters):
        # Les éligibles ne doivent percevoir que des salaires et des pensions
        rng = foyer_fiscal('rng', period = period)
        tspr = foyer_fiscal('tspr', period = period)
        eligble = (rng == tspr)
        # Condition de revenu
        deduction_famille = foyer_fiscal('deduction_famille', period = period)
        condition_de_revenu = (
            rng - deduction_famille
            ) <= parameters(period.start).impot_revenu.exoneration.seuil
        return eligble * condition_de_revenu


class irpp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt sur le revenu des personnes physiques'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        impot_revenu_brut = foyer_fiscal('impot_revenu_brut', period = period)
        exoneration = foyer_fiscal('exoneration', period = period)
        return impot_revenu_brut * not_(exoneration)


class revenu_mensuel_assimile_salaire_apres_abattement(Variable):
    value_type = float
    entity = Individu
    label = 'Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés'
    definition_period = MONTH

    def formula_2011(foyer_fiscal, period):
        revenu_assimile_salaire = individu('salaire_imposable', period = period)
        smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        smig = revenu_assimile_salaire <= smig_40h_mensuel
        tspr = parameters(period.start).impot_revenu.tspr

        abattement_frais_professionnels = min_(revenu_assimile_salaire * tspr.abat_sal, tspr.max_abat_sal)
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - min_(
                smig * tspr.abattement_pour_salaire_minimum,
                (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum
                ),
            0)
        return revenu_assimile_salaire_apres_abattement

    def formula(foyer_fiscal, period):
        revenu_assimile_salaire = individu('salaire_imposable', period = period)
        smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        smig = revenu_assimile_salaire <= smig_40h_mensuel
        tspr = parameters(period.start).impot_revenu.tspr
        abattement_frais_professionnels = min_(revenu_assimile_salaire * tspr.abat_sal, tspr.max_abat_sal)
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - smig * tspr.abattement_pour_salaire_minimum,
            0
            )
        return revenu_assimile_salaire_apres_abattement


class irpp_salarie_preleve_a_la_source(Variable):
    value_type = float
    entity = Individu
    label = 'Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés'
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_imposable = individu('salaire_imposable', period = period)
        deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)

        return calcule_impot_revenu_brut(
            salaire_imposable, deduction_famille_annuelle, period, parameters,
            )


class irpp_net_a_payer(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'IRPP net des prélèvements à la source'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        return (
            foyer_fiscal('irpp', period)
            - foyer_fiscal.sum(foyer_fiscal.members('irpp_salarie_preleve_a_la_source', period, options = [ADD]))
            )


# Utils

def calcule_base_imposable(salaire_mensuel, deduction_famille_annuelle, period, parameters):
    revenu_assimile_salaire = salaire_mensuel
    smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
    smig = revenu_assimile_salaire <= smig_40h_mensuel
    tspr = parameters(period.start).impot_revenu.tspr
    abattement_frais_professionnels = min_(
        tspr.abat_sal * revenu_assimile_salaire,
        tspr.max_abat_sal / 12
        )

    if period.start.year >= 2011:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - max_(
                smig * tspr.abattement_pour_salaire_minimum,
                (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum),
            0
            )
    else:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - smig * tspr.abattement_pour_salaire_minimum,
            0)

    non_exonere = revenu_assimile_salaire_apres_abattement >= 0
    if 2014 <= period.start.year <= 2016:
        non_exonere = (
            (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
            ) > parameters(period.start).impot_revenu.exoneration.seuil

    return non_exonere, revenu_assimile_salaire_apres_abattement


def calcule_impot_revenu_brut(salaire_mensuel, deduction_famille_annuelle, period, parameters):
    non_exonere, revenu_assimile_salaire_apres_abattement = calcule_base_imposable(
        salaire_mensuel, deduction_famille_annuelle, period, parameters)
    bareme = parameters(period.start).impot_revenu.bareme
    return (
        non_exonere * bareme.calc(
            12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle
            )
        ) / 12

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
        age = foyer_fiscal.members('age', period = period)
        P = parameters(period.start).impot_revenu.deductions.fam
        # res =+ (
        #    (ag < 20) +
        #    (ag < 25)*not_(boursier)*()
        #    )
        condition = (age >= 0) * (age <= P.age)
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
        age = foyer_fiscal.members('age', period = period)
        boursier = foyer_fiscal.members('boursier', period = period)

        return 0 * age * not_(boursier)


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

## 1. BIC
## 2. BNC
## 3. BEAP
## 4. Foncier

# 5. Traitements, salaires, indemnités, pensions et rentes viagères

class tspr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Traitements, salaires, indemnités, pensions et rentes viagères'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        revenu_assimile_salaire_apres_abattements = foyer_fiscal(
            'revenu_assimile_salaire_apres_abattements', period = period)
        revenu_assimile_pension_apres_abattements = foyer_fiscal(
            'revenu_assimile_pension_apres_abattements', period = period)

        return revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements


class revenu_assimile_salaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu assimilé à des salaires'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        salaire_imposable = foyer_fiscal.declarant_principal('salaire_imposable', period = period, options = [ADD])
        salaire_en_nature = foyer_fiscal.declarant_principal('salaire_en_nature', period = period, options = [ADD])
        return (salaire_imposable + salaire_en_nature)


class smig(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Indicatrice de SMIG ou SMAG déduite du montant des salaires'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        salarie_declarant_percevoir_smig = foyer_fiscal.declarant_principal('salarie_declarant_percevoir_smig', period = period.first_month)
        smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        smig = (
            salarie_declarant_percevoir_smig
            + (revenu_assimile_salaire <= 12 * smig_40h_mensuel)
            )
        return smig


class revenu_assimile_salaire_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu imposé comme des salaires net des abatements'
    definition_period = YEAR

    def formula_2011(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        revenu_assimile_salaire_apres_abattements = max_(
            (
                revenu_assimile_salaire * (1 - tspr.abat_sal)
                - max_(
                    smig * tspr.abattement_pour_salaire_minimum,
                    (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum
                    )
                ),
            0
            )
        return revenu_assimile_salaire_apres_abattements

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        return max_(revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.abattement_pour_salaire_minimum, 0)


class revenu_assimile_pension_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu assimilé à des pensions après abattements'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_pension = foyer_fiscal.declarant_principal('revenu_assimile_pension', period = period)
        avantages_nature_assimile_pension = foyer_fiscal.declarant_principal(
            'avantages_nature_assimile_pension', period = period)
        tspr = parameters(period.start).impot_revenu.tspr
        return (revenu_assimile_pension + avantages_nature_assimile_pension) * (1 - tspr.abat_pen)


# 6. Revenus de valeurs mobilières et de capitaux mobiliers

class rvcm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus de valeurs mobilières et de capitaux mobiliers'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        capm_banq = foyer_fiscal.declarant_principal('capm_banq', period = period)
        capm_cent = foyer_fiscal.declarant_principal('capm_cent', period = period)
        capm_caut = foyer_fiscal.declarant_principal('capm_caut', period = period)
        capm_part = foyer_fiscal.declarant_principal('capm_part', period = period)
        capm_oblig = foyer_fiscal.declarant_principal('capm_oblig', period = period)
        capm_caisse = foyer_fiscal.declarant_principal('capm_caisse', period = period)
        capm_plfcc = foyer_fiscal.declarant_principal('capm_plfcc', period = period)
        capm_epinv = foyer_fiscal.declarant_principal('capm_epinv', period = period)
        capm_aut = foyer_fiscal.declarant_principal('capm_aut', period = period)

        return (
            capm_banq
            + capm_cent
            + capm_caut
            + capm_part
            + capm_oblig
            + capm_caisse
            + capm_plfcc
            + capm_epinv
            + capm_aut
            )


# 7. revenus de source étrangère

class revenus_source_etrangere(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Autres revenus (revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        salaire_etranger = foyer_fiscal.declarant_principal('salaire_etranger', period = period)
        pension_etranger_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_transferee', period = period)
        pension_etranger_non_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_non_transferee', period = period)
        autres_revenus_etranger = foyer_fiscal.declarant_principal(
            'autres_revenus_etranger', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        return (
            salaire_etranger * (1 - tspr.abat_sal)
            + pension_etranger_non_transferee * (1 - tspr.abat_pen)
            + pension_etranger_transferee * (1 - tspr.abat_pen_etr)
            + autres_revenus_etranger
            )


###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


class rng(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu net global'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bnc = foyer_fiscal('bnc', period = period)
        tspr = foyer_fiscal('tspr', period = period)
        revenus_fonciers = foyer_fiscal('revenus_fonciers', period = period)
        retr = foyer_fiscal('revenus_source_etrangere', period = period)
        rvcm = foyer_fiscal('rvcm', period = period)

        return bnc + tspr + revenus_fonciers + +rvcm + retr


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
        rng = foyer_fiscal('rng', period = period)
        deduction_famille = foyer_fiscal('deduction_famille', period = period)
        deduction_rente = foyer_fiscal.declarant_principal('rente', period = period)
        deduction_assurance_vie = foyer_fiscal('deduction_assurance_vie', period = period)
        return rng - (deduction_famille + deduction_rente + deduction_assurance_vie)


class impot_revenu_brut(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Impôt brut avant non-imposabilité'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_net_imposable = foyer_fiscal('revenu_net_imposable', period = period)
        bareme = parameters(period.start).impot_revenu.bareme
        impot_revenu_brut = - bareme.calc(revenu_net_imposable)
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


def revenu_mensuel_assimile_salaire_apres_abattement(Variable):
    value_type = float
    entity = Individu
    label = 'Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés'
    definition_period = MONTH

    def formula_2011(foyer_fiscal, period):

        revenu_assimile_salaire = individu('salaire_imposable', period = period)
        smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        smig = revenu_assimile_salaire <= smig_40h_mensuel
        tspr = parameters(period.start).impot_revenu.tspr

        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal)
            - max_(
                smig * tspr.abattement_pour_salaire_minimum,
                (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum
                ),
            0)
        return revenu_assimile_salaire_apres_abattement

    def formula(foyer_fiscal, period):
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.abattement_pour_salaire_minimum,
            0
            )
        return revenu_assimile_salaire_apres_abattement



class irpp_mensuel_salarie(Variable):
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


# Utils

def calcule_impot_revenu_brut(salaire_mensuel, deduction_famille_annuelle, period, parameters):
    revenu_assimile_salaire = salaire_mensuel
    smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
    smig = revenu_assimile_salaire <= smig_40h_mensuel
    tspr = parameters(period.start).impot_revenu.tspr

    if period.start.year >= 2011:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal) - max_(smig * tspr.abattement_pour_salaire_minimum,
                (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum), 0)
    else:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.abattement_pour_salaire_minimum, 0)

    bareme = parameters(period.start).impot_revenu.bareme

    non_exonere = revenu_assimile_salaire_apres_abattement >= 0
    if 2014 <= period.start.year <= 2016:
        non_exonere = (
            (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
            ) > parameters(period.start).impot_revenu.exoneration.seuil

    return - 1.0 * non_exonere * bareme.calc(
        (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
        ) / 12

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class nb_enf(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        """
        TODO: fixme
        """
        age = foyer_fiscal.members("age", period=period.this_year.first_month)
        famille = parameters(period.start).impot_revenu.deductions.famille

        condition = (age >= 0) * (age <= famille.age)
        return foyer_fiscal.sum(condition, role=FoyerFiscal.PERSONNE_A_CHARGE)


class nb_enf_sup(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants étudiants du supérieur non boursiers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        age = foyer_fiscal.members("age", period=period.this_year.first_month)
        etudiant = foyer_fiscal.members("etudiant", period=period.this_year)
        boursier = foyer_fiscal.members("boursier", period=period.this_year)

        # Article 40 III: Enfant poursuivant des études supérieures sans bénéfice de bourse
        # et âgé de moins de 25 ans au 1er janvier de l'année d'imposition
        est_etudiant_eligible = etudiant * not_(boursier) * (age < 25)
        return foyer_fiscal.sum(
            est_etudiant_eligible, role=FoyerFiscal.PERSONNE_A_CHARGE
        )


class nb_infirme(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Nombre d'enfants infirmes"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        """
        Nombre d'enfants infirmes
        """
        infirme = foyer_fiscal.members("handicap", period=period) >= 3

        return foyer_fiscal.sum(1 * infirme, role=FoyerFiscal.PERSONNE_A_CHARGE)


class nb_parents(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Nombre de parents à charge"
    definition_period = YEAR


class chef_de_famille(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = "Indicatrice de chef de famille"
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
        male = foyer_fiscal.declarant_principal("male", period=period)
        marie = foyer_fiscal.declarant_principal("marie", period=period)
        divorce = foyer_fiscal.declarant_principal("divorce", period=period)
        veuf = foyer_fiscal.declarant_principal("veuf", period=period)
        nb_enf = foyer_fiscal("nb_enf", period=period)
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
    label = "Revenu net global"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal("bic", period=period)
            + foyer_fiscal("bnc", period=period)
            + foyer_fiscal("beap", period=period)
            + foyer_fiscal("revenus_fonciers", period=period)
            + foyer_fiscal("tspr", period=period)
            + foyer_fiscal("rvcm", period=period)
            + foyer_fiscal("revenus_source_etrangere", period=period)
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
        compte_special_epargne_banque = foyer_fiscal.sum(
            foyer_fiscal.members("compte_special_epargne_banque", period=period)
        )
        compte_special_epargne_cent = foyer_fiscal.sum(
            foyer_fiscal.members("compte_special_epargne_cent", period=period)
        )
        emprunt_obligataire = foyer_fiscal.sum(
            foyer_fiscal.members("emprunt_obligataire", period=period)
        )
        deductions = parameters(period.start).impot_revenu.deductions

        interets_bancaires = min_(
            compte_special_epargne_banque + compte_special_epargne_cent,
            deductions.interets_comptes_speciaux_epargne_bancaires.plaf,
        )

        return min_(
            interets_bancaires + emprunt_obligataire,
            deductions.interets_emprunts_obligataires.plaf,
        )


class deduction_famille(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déductions pour situation et charges de famille"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        rng = foyer_fiscal("rng", period=period)
        chef_de_famille = foyer_fiscal("chef_de_famille", period=period)
        nb_enf = foyer_fiscal("nb_enf", period=period)
        nb_infirme = foyer_fiscal("nb_infirme", period=period)
        nb_enf_sup = foyer_fiscal("nb_enf_sup", period=period)
        nb_parents = foyer_fiscal("nb_parents", period=period)

        famille = parameters(period.start).impot_revenu.deductions.famille

        #  chef de famille
        chef_de_famille = famille.chef_de_famille * chef_de_famille

        infirme = famille.infirme * nb_infirme
        nb_enf = max_(nb_enf - nb_infirme - nb_enf_sup, 0)
        enf = (
            (nb_enf >= 1) * famille.enf1
            + (nb_enf >= 2) * famille.enf2
            + (nb_enf >= 3) * famille.enf3
            + (nb_enf >= 4) * famille.enf4
        )

        sup = famille.enf_sup * nb_enf_sup

        parent = min_(famille.parent_taux * rng, famille.parent_max) * nb_parents

        res = chef_de_famille + enf + sup + infirme + parent
        return res


class deduction_rente(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Arrérages et rentes payées à titre obligatoire et gratuit"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        rente = foyer_fiscal("rente", period=period)

        return rente  # TODO:


class deduction_assurance_vie(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Primes afférentes aux contrats d'assurance-vie collectifs ou individuels"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        primes_assurance_vie = foyer_fiscal.members(
            "prime_assurance_vie", period=period
        )
        somme_primes_assurance_vie = foyer_fiscal.sum(primes_assurance_vie)
        marie = foyer_fiscal.declarant_principal("statut_marital", period=period)
        nb_enf = foyer_fiscal("nb_enf", period=period)
        assurance_vie = parameters(period.start).impot_revenu.deductions.assurance_vie
        deduction = min_(
            somme_primes_assurance_vie,
            assurance_vie.plaf
            + marie * assurance_vie.conj_plaf
            + nb_enf * assurance_vie.enf_plaf,
        )
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
    label = "Déduction supplémentaire pour les salariés payés au SMIG et SMAG"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        chef = foyer_fiscal("chef_de_famille", period=period)

        return 0 * chef  # TODO: voir avec tspr


class deduction_cea(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déduction pour Compte Épargne en Actions (CEA)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        cea = foyer_fiscal.sum(
            foyer_fiscal.members("compte_epargne_en_actions", period=period)
        )
        plafond = parameters(period.start).impot_revenu.deductions.cea_cei.cea
        return min_(cea, plafond)


class deduction_cei(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déduction pour Compte Épargne Investissement (CEI)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        cei = foyer_fiscal.sum(
            foyer_fiscal.members("compte_epargne_investissement", period=period)
        )
        plafond = parameters(period.start).impot_revenu.deductions.cea_cei.cei
        return min_(cei, plafond)


class interets_acquisition_logement_deductible(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Intérêts d'acquisition de l'habitation principale déductibles (plafonnés selon le coût)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        interets = foyer_fiscal.sum(
            foyer_fiscal.members("interets_acquisition_logement", period=period)
        )
        cout = foyer_fiscal.sum(
            foyer_fiscal.members("cout_acquisition_logement", period=period)
        )
        plafond_cout = parameters(
            period.start
        ).impot_revenu.deductions.logement.prix_max
        # Si le plafond_cout est 0, c'est qu'il n'y a pas de plafond applicable (ex: avant 2016)
        # S'il y a un plafond, la déduction saute si le coût dépasse le plafond.
        condition = (plafond_cout == 0) + (cout <= plafond_cout)
        return interets * condition


class deficits_anterieurs_reportables(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Déficits antérieurs reportables (Article 11)"
    definition_period = YEAR


class deductions_base(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déductions communes (hors investissement et assurance-vie)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal("deficits_anterieurs_reportables", period=period)
            + foyer_fiscal("deduction_famille", period=period)
            + foyer_fiscal.declarant_principal("rente", period=period)
            + foyer_fiscal("deduction_interets", period=period)
            + foyer_fiscal.sum(
                foyer_fiscal.members(
                    "plus_value_cession_actifs_cotes_bourse", period=period
                )
            )
            + foyer_fiscal("interets_acquisition_logement_deductible", period=period)
            + foyer_fiscal.sum(
                foyer_fiscal.members("pret_universitaire", period=period)
            )
            + foyer_fiscal.sum(foyer_fiscal.members("dons", period=period))
            + foyer_fiscal.sum(
                foyer_fiscal.members("cotisations_non_affilie", period=period)
            )
        )


class assiette_avant_avantages(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Assiette imposable avant déductions soumises au minimum d'impôt"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return max_(
            foyer_fiscal("rng", period) - foyer_fiscal("deductions_base", period), 0
        )


class impot_avant_avantages(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt dû avant avantages fiscaux"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        base = foyer_fiscal("assiette_avant_avantages", period=period)
        bareme = parameters(period.start).impot_revenu.bareme
        return bareme.calc(base)


class minimum_impot(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Minimum d'impôt exigible (Article 12 bis)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        impot_theorique = foyer_fiscal("impot_avant_avantages", period=period)
        taux = parameters(period.start).impot_revenu.minimum_impot.taux
        return impot_theorique * taux


class investissement_deductible_integralement(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Investissements donnant droit à une déduction intégrale des revenus (Développement régional, Agriculture, etc.)"
    definition_period = YEAR


class investissement_deductible_partiellement(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Investissements donnant droit à une déduction partielle (limités par un % du revenu imposable)"
    definition_period = YEAR


class deduction_investissement_autre(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déduction totale au titre des investissements physiques et financiers (hors CEA/CEI/Assurance Vie)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        taux_plafond = parameters(period.start).impot_revenu.deductions.investissements.taux_plafond_partiel
        # L'assiette de plafonnement est classiquement le revenu net après déductions communes
        revenu_plafonnable = foyer_fiscal("assiette_avant_avantages", period=period)

        plafond = revenu_plafonnable * taux_plafond

        integral = foyer_fiscal("investissement_deductible_integralement", period=period)
        partiel = foyer_fiscal("investissement_deductible_partiellement", period=period)

        return integral + min_(partiel, plafond)


class deductions_investissement(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Déductions pour investissement et épargne longue"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal("deduction_assurance_vie", period=period)
            + foyer_fiscal("deduction_cea", period=period)
            + foyer_fiscal("deduction_cei", period=period)
            + foyer_fiscal("deduction_investissement_autre", period=period)
        )


class deductions(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Total des déductions"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal("deductions_base", period) + foyer_fiscal(
            "deductions_investissement", period
        )


class revenu_net_imposable(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenu net imposable"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        """
        Revenu net imposable ie soumis à au barême de l'impôt après déduction des dépenses
        et charges professionnelles et des revenus non soumis à l'impôt
        """
        return max_(
            foyer_fiscal("assiette_avant_avantages", period)
            - foyer_fiscal("deductions_investissement", period),
            0,
        )


class impot_revenu_brut(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt brut avant non-imposabilité (Barème IRPP)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_net_imposable = foyer_fiscal("revenu_net_imposable", period=period)
        bareme = parameters(period.start).impot_revenu.bareme
        impot_calcule = bareme.calc(revenu_net_imposable)
        impot_min = foyer_fiscal("minimum_impot", period=period)
        return max_(impot_calcule, impot_min)


class chiffre_affaires_soumis_au_forfait(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Chiffre d'Affaires soumis au régime forfaitaire (exclus de l'IRPP classique)"
    definition_period = YEAR


class impot_regime_forfaitaire_du(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt dû au titre du Régime Forfaitaire"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        ca = foyer_fiscal("chiffre_affaires_soumis_au_forfait", period=period)
        taux = parameters(period.start).impot_revenu.regimes_speciaux.forfaitaire.taux_imposition
        return ca * taux


class revenu_soumis_retenue_liberatoire(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Revenus soumis à retenue à la source libératoire (exclus de l'IRPP classique)"
    definition_period = YEAR


class impot_sur_retenue_liberatoire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt (Retenue) dû sur revenus libératoires"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu = foyer_fiscal("revenu_soumis_retenue_liberatoire", period=period)
        taux = parameters(period.start).impot_revenu.regimes_speciaux.retenue_liberatoire.taux
        return revenu * taux


class impot_total_du(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt Total Dû (IRPP au barème + Forfaitaire + Retenues Libératoires)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return (
            foyer_fiscal("irpp", period=period)
            + foyer_fiscal("impot_regime_forfaitaire_du", period=period)
            + foyer_fiscal("impot_sur_retenue_liberatoire", period=period)
        )


class exoneration(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = "Exoneration de l'impôt sur le revenu des personnes physiques"
    definition_period = YEAR
    end = "2016-12-31"

    def formula_2014(foyer_fiscal, period, parameters):
        # Les éligibles ne doivent percevoir que des salaires et des pensions
        rng = foyer_fiscal("rng", period=period)
        tspr = foyer_fiscal("tspr", period=period)
        eligble = rng == tspr
        # Condition de revenu
        deduction_famille = foyer_fiscal("deduction_famille", period=period)
        condition_de_revenu = (rng - deduction_famille) <= parameters(
            period.start
        ).impot_revenu.exoneration.seuil
        return eligble * condition_de_revenu


class irpp(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Impôt sur le revenu des personnes physiques"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        impot_revenu_brut = foyer_fiscal("impot_revenu_brut", period=period)
        exoneration = foyer_fiscal("exoneration", period=period)
        return impot_revenu_brut * not_(exoneration)


class credit_impot_etranger(Variable):
    value_type = float
    default_value = 0.0
    entity = FoyerFiscal
    label = "Crédit d'impôt imputable sur les revenus de source étrangère"
    definition_period = YEAR





class irpp_salarie_preleve_a_la_source(Variable):
    value_type = float
    entity = Individu
    label = "Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés"
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_imposable = individu("salaire_imposable", period=period)
        deduction_famille_annuelle = individu.foyer_fiscal(
            "deduction_famille", period=period.this_year
        )

        return calcule_impot_revenu_brut(
            salaire_imposable,
            deduction_famille_annuelle,
            period,
            parameters,
        )


class acomptes_provisionnels(Variable):
    value_type = float
    entity = Individu
    label = "Acomptes provisionnels versés durant l'année"
    definition_period = YEAR


class retenues_source_non_salariales(Variable):
    value_type = float
    entity = Individu
    label = (
        "Retenues à la source subies sur les autres revenus (loyers, honoraires, etc.)"
    )
    definition_period = YEAR


class irpp_net_a_payer(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "IRPP net des acomptes et prélèvements à la source"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        impot_total = foyer_fiscal("impot_total_du", period)
        ras_salaires = foyer_fiscal.sum(
            foyer_fiscal.members(
                "irpp_salarie_preleve_a_la_source", period, options=[ADD]
            )
        )
        acomptes = foyer_fiscal.sum(
            foyer_fiscal.members("acomptes_provisionnels", period)
        )
        ras_autres = foyer_fiscal.sum(
            foyer_fiscal.members("retenues_source_non_salariales", period)
        )
        credits_etranger = foyer_fiscal("credit_impot_etranger", period)
        net = impot_total - ras_salaires - acomptes - ras_autres - credits_etranger
        return net


# Utils


def calcule_base_imposable(
    salaire_mensuel, deduction_famille_annuelle, period, parameters
):
    revenu_assimile_salaire = salaire_mensuel
    smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
    smig = revenu_assimile_salaire <= smig_40h_mensuel
    tspr = parameters(period.start).impot_revenu.tspr
    abattement_frais_professionnels = min_(
        tspr.abat_sal * revenu_assimile_salaire, tspr.max_abat_sal / 12
    )

    if period.start.year >= 2011:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - max_(
                smig * tspr.abattement_pour_salaire_minimum,
                (revenu_assimile_salaire <= tspr.smig_ext)
                * tspr.abattement_pour_salaire_minimum,
            ),
            0,
        )
    else:
        revenu_assimile_salaire_apres_abattement = max_(
            revenu_assimile_salaire
            - abattement_frais_professionnels
            - smig * tspr.abattement_pour_salaire_minimum,
            0,
        )

    non_exonere = revenu_assimile_salaire_apres_abattement >= 0
    if 2014 <= period.start.year <= 2016:
        non_exonere = (
            12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle
        ) > parameters(period.start).impot_revenu.exoneration.seuil

    return non_exonere, revenu_assimile_salaire_apres_abattement


def calcule_impot_revenu_brut(
    salaire_mensuel, deduction_famille_annuelle, period, parameters
):
    non_exonere, revenu_assimile_salaire_apres_abattement = calcule_base_imposable(
        salaire_mensuel, deduction_famille_annuelle, period, parameters
    )
    bareme = parameters(period.start).impot_revenu.bareme
    return (
        non_exonere
        * bareme.calc(
            12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle
        )
    ) / 12

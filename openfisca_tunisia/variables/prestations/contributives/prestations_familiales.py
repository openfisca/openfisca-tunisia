from numpy import (
    maximum as max_,
    minimum as min_,
    round,
    )


from openfisca_tunisia.variables.base import * # noqa F401


class salaire_unique(Variable):
    value_type = bool
    entity = Menage
    label = 'Indicatrice de salaire unique'
    definition_period = YEAR

    def formula(menage, period):
        salaire_imposable_personne_de_reference = menage.personne_de_reference('salaire_imposable', period = period)
        salaire_imposable_conjoint = menage.conjoint('salaire_imposable', period = period)
        return xor_(salaire_imposable_personne_de_reference > 0, salaire_imposable_conjoint > 0)


# Allocations familiales

class prestations_familiales_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = 'Enfant considéré à charge au sens des prestations familiales'
    definition_period = MONTH
    reference = 'http://www.cleiss.fr/docs/regimes/regime_tunisie_salaries.html'

    #    Jusqu'à l'âge de 16 ans sans conditions.
    #    Jusqu'à l'âge de 18 ans pour les enfants en apprentissage qui ne perçoivent pas une rémunération
    # supérieure à 75 % du SMIG.
    #    Jusqu'à l'âge de 21 ans pour les enfants qui fréquentent régulièrement un établissement secondaire,
    # supérieur, technique ou professionnel, à condition que les enfants n'occupent pas d'emplois salariés.
    #    Jusqu'à l'âge de 21 ans pour la jeune fille qui remplace sa mère auprès de ses frères et sœurs. TODO
    #    Sans limite d'âge et quelque soit leur rang pour les enfants atteints d'une infirmité ou d'une maladie
    # incurable et se trouvant, de ce fait, dans l'impossibilité permanente et absolue d'exercer un travail
    # lucratif, et pour les handicapés titulaires d'une carte d'handicapé qui ne sont pas pris en charge
    # intégralement par un organisme public ou privé benéficiant de l'aide de l'Etat ou des collectivités
    # locales.

    def formula(individu, period, parameters):
        # TODO à retravailler
        # age = individu('age', period)
        handicap = individu('handicap', period)
        est_enfant = individu.has_role(Menage.ENFANT)

        condition_enfant = (
            (age_individu <= 16)
            + (age_individu <= 18) * (salaire_individu <= .75 * smig_48h_mensuel)
            )
        condition_jeune_etudiant = (
            # (age_individu <= 21) * etudiant ou soeur au foyer
            )

        return (condition_enfant + condition_jeune_etudiant + handicap) * est_enfant


class af_nbenf(Variable):
    value_type = float
    entity = Menage
    label = "Nombre d'enfants au sens des allocations familiales"
    definition_period = YEAR

    def formula(menage, period, parameters):
        prestations_familiales_enfant_a_charge = menage.members(
            'prestations_familiales_enfant_a_charge', period)
        af_nbenf = max_(
            menage.sum(prestations_familiales_enfant_a_charge),
            3
            )
        return af_nbenf


class af(Variable):
    value_type = float
    entity = Menage
    label = 'Allocations familiales'
    definition_period = YEAR

    def formula(menage, period, parameters):
        af_nbenf = menage('af_nbenf', period = period)
        # Le montant trimestriel est calculé en pourcentage de la rémunération globale trimestrielle palfonnée
        # à 122 dinars
        # TODO: ajouter éligibilité des parents aux allocations familiales
        pf = parameters.prestations.contributives.prestations_familiales
        bm = min_(
            max_(
                menage.personne_de_reference('salaire_imposable', period),
                menage.conjoint('salaire_imposable', period),
                ) / 4,
            pf.af.plaf_trim
            )  # base trimestrielle
        # prestations familliales  # Règle d'arrondi ?
        af_1enf = round(bm * parameters.af.taux.enf1, 2)
        af_2enf = round(bm * parameters.af.taux.enf2, 2)
        af_3enf = round(bm * parameters.af.taux.enf3, 2)
        af_base = (
            (af_nbenf >= 1) * af_1enf
            + (af_nbenf >= 2) * af_2enf
            + (af_nbenf >= 3) * af_3enf
            )
        return 4 * af_base  # annualisé


class majoration_salaire_unique(Variable):
    value_type = float
    entity = Menage
    label = 'Majoration du salaire unique'
    definition_period = YEAR  # TODO trimestrialiser

    def formula(menage, period, parameters):
        salaire_unique = menage('salaire_unique', period = period)
        af_nbenf = menage('af_nbenf', period = period)
        P = parameters(period.start).prestations.contributives.prestations_familiales
        af_1enf = round(P.salaire_unique.enf1, 3)  # trimestrielle
        af_2enf = round(P.salaire_unique.enf2, 3)  # trimestrielle
        af_3enf = round(P.salaire_unique.enf3, 3)  # trimestrielle
        af = (
            (af_nbenf >= 1) * af_1enf
            + (af_nbenf >= 2) * af_2enf
            + (af_nbenf >= 3) * af_3enf
            )
        return 4 * af * salaire_unique  # annualisé


def _af_cong_naiss(age, _P):
    # _option={'age': ENFS}
    return 0


def _af_cong_jeun_trav(age, _P):
    #    Les salariés de moins de 18 ans du régime non agricole bénéficient de
    #    2 jours de congés par mois et au maximum 24 jours ouvrables,
    #    l'employeur se fera rembourser par la CNSS 12 jours de congés. Les
    #    salariés âgés de 18 à 20 ans bénéficient de 18 jours de congés
    #    ouvrables par an soit 6 jours remboursés à l'employeur par la CNSS.
    #    Le remboursement à l'employeur est effectué par la Caisse Nationale
    #    de Sécurité Sociale de l'avance faite en exécution de l'article 113
    #    alinéa 2 du Code du Travail.
    # , _option = {'age': ENFS}
    return 0


class contribution_frais_creche(Variable):
    value_type = float
    entity = Menage
    label = 'Contribution aux frais de crêche'
    definition_period = YEAR

    def formula(menage, period, parameters):
        month = period.last_month
        smig48 = parameters(period.start).marche_travail.smig_48h_mensuel  # TODO: smig 48H
        # TODO rework and test
        # Une prise en charge peut être accordée à la mère exerçant une
        # activité salariée et dont le salaire ne dépasse pas deux fois et demie
        # le SMIG pour 48 heures de travail par semaine. Cette contribution est
        # versée pour les enfants ouvrant droit aux prestations familiales et
        # dont l'âge est compris entre 2 et 36 mois. Elle s'élève à 15 dinars par
        # enfant et par mois pendant 11 mois.
        # , _option = {'age_en_mois': ENFS, 'sal': [CHEF, PART]}
        somme_salaire_imposable = (
            menage.personne_de_reference('salaire_imposable', period = month)
            + menage.conjoint('salaire_imposable', period = month)
            )
        age_en_mois = menage.members('age_en_mois', period = month)
        creche = parameters(period).prestations.contributives.prestations_familiales.creche
        age_en_mois_benjamin = menage.min(age_en_mois)[0]

        elig_age = (age_en_mois_benjamin <= creche.age_max) * (age_en_mois_benjamin >= creche.age_min)
        elig_sal = somme_salaire_imposable < creche.plaf * smig48
        return creche.montant * elig_age * elig_sal * min_(creche.duree, 12 - age_en_mois_benjamin)


class prestations_familiales(Variable):  # TODO add _af_cong_naiss, af_cong_jeun_trav
    value_type = float
    entity = Menage
    label = 'Prestations familales'
    definition_period = YEAR

    def formula(menage, period):
        af = menage('af', period = period)
        majoration_salaire_unique = menage('majoration_salaire_unique', period = period)
        contribution_frais_creche = menage('contribution_frais_creche', period = period)
        return af + majoration_salaire_unique + contribution_frais_creche


#
# Assurances sociales   Maladie
#

def prestationl(age, sal, parameters):
    '''
    Assurance sociale - prestation en espèces TODO: à compléter
    '''
    # , _option = {'age': ENFS}
    #    P = _P.as.maladie
    P = 0
    mal = 0
    smig = parameters.marche_travail.smig
    return mal * P.part * max(P.plaf_mult * smig, sal) * P.duree


def _as_maternite(age, sal, parameters):
    '''
    Assurance sociale - maternité  TODO: à compléter
    '''
    # P = parameters.as.maternite
    # smig = parameters.marche_travail.smig
    # return P.part*max(P.plaf_mult*smig,sal)*P.duree
    return 0


def _as_deces(sal, paramters):
    '''
    Assurance sociale - décès   # TODO: à compléter
    '''
    # P = _P.as.deces
    return 0

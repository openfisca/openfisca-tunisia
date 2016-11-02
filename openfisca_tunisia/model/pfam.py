# -*- coding: utf-8 -*-


from __future__ import division

from numpy import (round, zeros, maximum as max_, minimum as min_, logical_xor as xor_, logical_not as not_,
    asanyarray, amin, amax, arange)

from openfisca_tunisia.model.base import *  # noqa analysis:ignore


CHEF = QUIFOY['vous']
PART = QUIFOY['conj']

PACS = [QUIMEN['enf' + str(i)] for i in range(1, 10)]
ENFS = [QUIMEN['enf' + str(i)] for i in range(1, 10)]


def age_en_mois_benjamin(agems):
    '''
    Renvoi un vecteur (une entree pour chaque famille) avec l'age du benjamin.
    '''
    agem_benjamin = 12 * 9999
    for agem in agems.itervalues():
        isbenjamin = (agem < agem_benjamin) * (agem >= 0)
        agem_benjamin = isbenjamin * agem + not_(isbenjamin) * agem_benjamin
    return agem_benjamin


def age_min(age, minimal_age = None):
    '''
    Returns minimal age higher than or equal to a
    '''
    if minimal_age is None:
        minimal_age = 0
    ages = asanyarray(age)
    ages = ages + (ages < minimal_age) * 9999
    return amin(ages, axis = 1)


def age_max(age):
    '''
    Returns minimal age higher than or equal to a
    '''
    ages = asanyarray(age)
    return amax(ages, axis = 1)


def ages_first_kids(age, nb = None):
    '''
    Returns the ages of the nb first born kids according to age
    '''
    ages = asanyarray(age.values())

    ages = (ages.T + .00001 * arange(ages.shape[0])).T  # To deal with twins

    if nb is None:
        nb = 3  # TODO: 4e enfant qui en bénéficiait en 1989
    i = 0
    age_list = []

    while i < 4:
        from numpy import putmask
        maximas = amax(ages, axis = 0)
        age_list.append(round(maximas))
        putmask(ages, ages == maximas, -99999)
        i += 1
    return age_list


def _nb_par(self, quifoy_holder):
    '''
    Nombre d'adultes (parents) dans la famille
    'fam'
    '''
    quifoy = self.split_by_roles(quifoy_holder, roles = PART)
    return period, 1 + 1 * (quifoy[PART] == 1)


def _maries(statmarit):
    '''
    couple = 1 si couple marié sinon 0 TODO: faire un choix avec couple ?
    '''
    return period, statmarit == 1


def _isol(nb_par):
    '''
    Parent (s'il y a lieu) isolé
    '''
    return period, nb_par == 1


def _etu(activite):
    '''
    Indicatrice individuelle etudiant
    '''
    return period, activite == 2


class smig75(Variable):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Indicatrice de salaire supérieur à 75% du smig"

    def function(self, simulation, period):
        '''
        Indicatrice de rémunération inférieur à 75% du smic
        '''
        period = period.start.offset('first-of', 'month').period('year')
        sali = simulation.calculate('sali', period = period)
        sal_nat = simulation.calculate('sal_nat', period = period)
        _P = simulation.legislation_at(period.start)

        return period, (sali + sal_nat) < _P.cotsoc.gen.smig


class sal_uniq(Variable):
    column = BoolCol(default = False)
    entity_class = Menages
    label = u"Indicatrice de salaire unique"

    def function(self, simulation, period):
        '''
        Indicatrice de salaire unique
        '''
        period = period.start.offset('first-of', 'month').period('year')
        sali_holder = simulation.compute('sali', period = period)
        _P = simulation.legislation_at(period.start)

        sali = self.split_by_roles(sali_holder, roles = [CHEF, PART])
        uniq = xor_(sali[CHEF] > 0, sali[PART] > 0)
        return period, uniq


############################################################################
# Allocations familiales
############################################################################


class af_nbenf(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Nombre d'enfants au sens des allocations familiales"

    def function(self, simulation, period):
        '''
        Nombre d'enfants au titre des allocations familiales
        'foy'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        age_holder = simulation.compute('age', period = period)
        smig75_holder = simulation.compute('smig75', period = period)
        activite = simulation.calculate('activite', period = period)
        inv_holder = simulation.compute('inv', period = period)
        _P = simulation.legislation_at(period.start)

        #    From http://www.allocationfamiliale.com/allocationsfamiliales/allocationsfamilialestunisie.htm
    #    Jusqu'à l'âge de 16 ans sans conditions.
    #    Jusqu'à l'âge de 18 ans pour les enfants en apprentissage qui ne perçoivent pas une rémunération supérieure à 75 % du SMIG.
    #    Jusqu'à l'âge de 21 ans pour les enfants qui fréquentent régulièrement un établissement secondaire, supérieur,
    #      technique ou professionnel, à condition que les enfants n'occupent pas d'emplois salariés.
    #    Jusqu'à l'âge de 21 ans pour la jeune fille qui remplace sa mère auprès de ses frères et sœurs. TODO: code this
    #    Sans limite d'âge et quelque soit leur rang pour les enfants atteints d'une infirmité ou d'une maladie incurable et se trouvant,
    #    de ce fait, dans l'impossibilité permanente et absolue d'exercer un travail lucratif, et pour les handicapés titulaires d'une carte d'handicapé
    #    qui ne sont pas pris en charge intégralement par un organisme public ou privé benéficiant de l'aide de l'Etat ou des collectivités locales.

        age = self.split_by_roles(age_holder, roles = ENFS)
        smig75 = self.split_by_roles(smig75_holder, roles = ENFS)
        inv = self.split_by_roles(inv_holder, roles = ENFS)

        ages = ages_first_kids(age, nb = 3)
        res = zeros(ages[0].shape)

        for ag in ages:
            res += (ag >= 0) * ((1 * (ag < 16) + 1 * (ag < 18) + 1 * (ag < 21)) >= 1)
    #                 (ag < 18) + # *smig75[key]*(activite[key] =='aprenti')  + # TODO apprenti
    #                 (ag < 21) # *(or_(activite[key]=='eleve', activite[key]=='etudiant'))
    #                 )  > 1

        return period, res


class af(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Allocations familiales"

    def function(self, simulation, period):
        '''
        Allocations familiales
        'foy'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        af_nbenf = simulation.calculate('af_nbenf', period = period)
        sali_holder = simulation.compute('sali', period = period)
        _P = simulation.legislation_at(period.start)

        # Le montant trimestriel est calculé en pourcentage de la rémunération globale trimestrielle palfonnée à 122 dinars
        # TODO: ajouter éligibilité des parents aux allocations familiales
        print 'sal'
        print sali_holder
        sali = self.split_by_roles(sali_holder, roles = [CHEF, PART])
        P = _P.pfam
        bm = min_(max_(sali[CHEF], sali[PART]) / 4, P.af.plaf_trim)  # base trimestrielle
        # prestations familliales  # Règle d'arrondi ?
        af_1enf = round(bm * P.af.taux.enf1, 2)
        af_2enf = round(bm * P.af.taux.enf2, 2)
        af_3enf = round(bm * P.af.taux.enf3, 2)
        af_base = (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + (af_nbenf >= 3) * af_3enf
        return period, 4 * af_base  # annualisé


class maj_sal_uniq(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Majoration du salaire unique"

    def function(self, simulation, period):
        '''
        Majoration salaire unique
        'fam'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        sal_uniq = simulation.calculate('sal_uniq', period = period)
        af_nbenf = simulation.calculate('af_nbenf', period = period)
        _P = simulation.legislation_at(period.start)

        P = _P.pfam
        af_1enf = round(P.sal_uniq.enf1, 3)
        af_2enf = round(P.sal_uniq.enf2, 3)
        af_3enf = round(P.sal_uniq.enf3, 3)
        af = (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + (af_nbenf >= 3) * af_3enf
        return period, 4 * af  # annualisé


def _af_cong_naiss(age, _P):
    # _option={'age': ENFS}
    return period, 0


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
    return period, 0


class contr_creche(Variable):
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Contribution aux frais de crêche"

    def function(self, simulation, period):
        '''
        Contribution aux frais de crêche
        'fam'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        sali_holder = simulation.compute('sali', period = period)
        agem_holder = simulation.compute('agem', period = period)
        _P = simulation.legislation_at(period.start)

        # Une prise en charge peut être accordée à la mère exerçant une
        # activité salariée et dont le salaire ne dépasse pas deux fois et demie
        # le SMIG pour 48 heures de travail par semaine. Cette contribution est
        # versée pour les enfants ouvrant droit aux prestations familiales et
        # dont l'âge est compris entre 2 et 36 mois. Elle s'élève à 15 dinars par
        # enfant et par mois pendant 11 mois.

        # , _option = {'agem': ENFS, 'sal': [CHEF, PART]}

        sali = self.split_by_roles(sali_holder, roles = [PART])
        agem = self.split_by_roles(agem_holder, roles = ENFS)
        smig48 = _P.cotsoc.gen.smig  # TODO: smig 48H
        P = _P.pfam.creche
        age_m_benj = age_en_mois_benjamin(agem)
        elig_age = (age_m_benj <= P.age_max) * (age_m_benj >= P.age_min)
        elig_sal = sali < P.plaf * smig48
        return period, P.montant * elig_age * elig_sal * min_(P.duree, 12 - age_m_benj)


class pfam(Variable):  # , _af_cong_naiss, af_cong_jeun_trav
    column = FloatCol(default = 0)
    entity_class = Menages
    label = u"Prestations familales"

    def function(self, simulation, period):
        '''
        Prestations familiales
        'fam'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        af = simulation.calculate('af', period = period)
        maj_sal_uniq = simulation.calculate('maj_sal_uniq', period = period)
        contr_creche = simulation.calculate('contr_creche', period = period)

        return period, af + maj_sal_uniq + contr_creche


############################################################################
# Assurances sociales   Maladie
############################################################################

def _as_mal(age, sal, _P):
    '''
    Assurance sociale - prestation en espèces TODO: à compléter
    '''
    # , _option = {'age': ENFS}
    #    P = _P.as.mal
    P = 0
    mal = 0
    smig = _P.gen.smig
    return period, mal * P.part * max(P.plaf_mult * smig, sal) * P.duree


def _as_maternite(age, sal, _P):
    '''
    Assurance sociale - maternité  TODO: à compléter
    '''
    # P = _P.as.mat
    smig = _P.gen.smig
    # return period, P.part*max(P.plaf_mult*smig,sal)*P.duree
    return period, 0


def _as_deces(sal, _P):
    '''
    Assurance sociale - décès   # TODO: à compléter
    '''
    # P = _P.as.dec
    return period, 0

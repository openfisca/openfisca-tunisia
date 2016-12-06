# -*- coding: utf-8 -*-


from __future__ import division

from numpy import zeros
from openfisca_core.taxscales import MarginalRateTaxScale

from openfisca_tunisia.model.base import *  # noqa analysis:ignore
from openfisca_tunisia.model.data import CAT


def compute_cotisation(individu, period, cotisation_type = None, bareme_name = None, legislation = None):
    assert cotisation_type in ['employeur', 'salarie']
    assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period)
    categorie_salarie = individu('categorie_salarie', period)  # TODO change to regime_salarie
    baremes_by_regime = legislation(period.start).cotisations_sociales
    cotisation = zeros(len(assiette_cotisations_sociales))
    for regime_name, regime_index in CAT:
        bareme_by_name = baremes_by_regime[regime_name].get(
            'cotisations_{}'.format(cotisation_type))
        if bareme_by_name is not None:
            if bareme_name in ['maladie', 'maternite', 'deces']:
                baremes_assurances_sociales = bareme_by_name.get('assurances_sociales')
                if baremes_assurances_sociales is not None:
                    bareme = baremes_assurances_sociales.get(bareme_name)
            else:
                bareme = bareme_by_name.get(bareme_name)

            if bareme is not None:
                cotisation += bareme.calc(
                    assiette_cotisations_sociales * (categorie_salarie == regime_index),
                    )
    return cotisation


class assiette_cotisations_sociales(Variable):
    column = FloatCol
    entity = Individu
    label = u"Assiette des cotisations sociales"

    def function(individu, period):
        return period, individu('salaire_imposable', period)


class cotisations_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation sociales employeur"

    def function(individu, period):
        return period, (
            cotisation_deces_employeur +
            cotisation_famille_employeur +
            cotisation_maladie_employeur +
            cotisation_maternite_employeur
            )

class cotisations_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation sociales salarie"

    def function(individu, period):
        return period, (
            cotisation_deces_salarie +
            cotisation_famille_salarie +
            cotisation_maladie_salarie +
            cotisation_maternite_salarie
            )


class cotisation_deces_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: décès (employeur)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'deces',
            legislation = legislation
            )


class cotisation_deces_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: décès (salarié)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'deces',
            legislation = legislation
            )


class cotisation_famille_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation sociale allocations familiales (employeur)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'famille',
            legislation = legislation
            )


class cotisation_famille_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation sociale allocations familiales (salarie)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'famille',
            legislation = legislation
            )


class cotisation_maladie_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: maladie (employeur)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            legislation = legislation
            )


class cotisation_maladie_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: maladie (salarie)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maladie',
            legislation = legislation
            )


class cotisation_maternite_employeur(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: maternité (employeur)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maternite',
            legislation = legislation
            )


class cotisation_maternite_salarie(Variable):
    column = FloatCol
    entity = Individu
    label = u"Cotisation assurances sociales: maternité (salarié)"

    def function(individu, period, legislation):
        return period, compute_cotisation(
            individu,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maternite',
            legislation = legislation
            )


class salaire_brut(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaires bruts"

    def function(individu, period, legislation):
        '''
        Calcule le salaire brut à partir du salaire net
        '''
        period = period.this_year
        salaire_imposable = individu('salaire_imposable', period = period)
        categorie_salarie = individu('categorie_salarie', period = period)
        cotisations_sociales = legislation(period.start, reference = True).cotisations_sociales

        smig = cotisations_sociales.gen.smig_40h_mensuel
        cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', cotisations_sociales)
        plafond_securite_sociale = 12 * smig

        n = len(salaire_imposable)
        salaire_brut = zeros(n)
        # TODO améliorer tout cela !!
        for categ in CAT:
            iscat = (categorie_salarie == categ[1])
            if categ[0] == 're':
                return period, salaire_imposable  # on retourne le salaire_imposable pour les étudiants
            else:
                continue

            if 'sal' in cotisations_sociales[categ[0]]:
                sal = cotisations_sociales[categ[0]]['sal']
                baremes = sal.scale_tax_scales(plafond_securite_sociale)
                bar = combine_bracket(baremes)
                invbar = bar.inverse()
                temp = iscat * invbar.calc(salaire_imposable)
                salaire_brut += temp
        return period, salaire_brut


class salaire_super_brut(Variable):
    column = FloatCol
    entity = Individu
    label = u"Salaires super bruts"

    def function(individu, period):
        period = period.this_year
        salaire_brut = individu('salaire_brut', period = period)
        cotisations_employeur = individu('cotisations_employeur', period = period)

        return period, salaire_brut - cotisations_employeur


# class cotisations_employeur(Variable):
#     column = FloatCol
#     entity = Individu
#     label = u"Cotisations sociales employeur"

#     def function(individu, period, legislation):
#         period = period.this_year
#         salaire_brut = individu('salaire_brut', period = period)
#         categorie_salarie = individu('categorie_salarie', period = period)
#         _P = legislation(period.start)

#         # TODO traiter les différents régimes séparément ?

#         smig = _P.cotisations_sociales.gen.smig_40h_mensuel
#         cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)

#         plafond_securite_sociale = 12 * smig
#         # TODO: clean all this
#         n = len(salaire_brut)
#         cotisations_employeur = zeros(n)
#         for categ in CAT:
#             iscat = (categorie_salarie == categ[1])
#             if categ[0] == 're':
#                 return period, salaire_brut  # on retounre le salaire_brut pour les étudiants
#             else:
#                 continue
#             if 'cotisations_employeur' in cotisations_sociales[categ[0]]:
#                 bareme_employeur = cotisations_sociales[categ[0]]['cotisations_employeur']
#                 baremes = scale_tax_scales(bareme_employeur, plafond_securite_sociale)
#                 bareme_agrege = combine_tax_scales(baremes)
#                 temp = - iscat * bareme_agrege.calc(salaire_brut)
#                 cotisations_employeur += temp
#         return period, cotisations_employeur


# class cotisations_salarie(Variable):
#     column = FloatCol
#     entity = Individu
#     label = u"Cotisations sociales salariés"

#     def function(individu, period, legislation):
#         period = period.this_year
#         salaire_brut = individu('salaire_brut', period = period)
#         categorie_salarie = individu('categorie_salarie', period = period)
#         _P = legislation(period.start)
#         # TODO traiter les différents régimes
#         smig = _P.cotisations_sociales.gen.smig
#         cotisations_sociales = MarginalRateTaxScale('cotisations_sociales', _P.cotisations_sociales)
#         plafond_securite_sociale = 12 * smig

#         n = len(salaire_brut)
#         cotisations_salarie = zeros(n)

#         for categ in CAT:
#             iscat = (categorie_salarie == categ[1])

#             if categ[0] == 're':
#                 return period, 0 * salaire_brut  # TODO: doit retounrer la bonne valeur les étudiants
#             else:
#                 continue

#             if 'sal' in cotisations_sociales[categ[0]]:
#                 pat = cotisations_sociales[categ[0]]['sal']
#                 baremes = scale_tax_scales(pat, plafond_securite_sociale)
#                 bar = combine_tax_scales(baremes)
#                 temp = - iscat * bar.calc(salaire_brut)
#                 cotisations_salarie += temp

#         return period, cotisations_salarie

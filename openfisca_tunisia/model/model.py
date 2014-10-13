# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import collections
from functools import partial

from openfisca_core.columns import AgeCol, BoolCol, FloatCol
from openfisca_core.formulas import (
    build_alternative_formula_couple,
    build_dated_formula_couple,
    build_select_formula_couple,
    build_simple_formula_couple,
    )

from .. import entities
from .base import prestation_by_name  # Must be defined before importing other modules from model package.

# Import model modules.
from . import common as cm
from . import cotsoc as cs
from . import irpp as ir
from . import pfam as pf


build_alternative_formula_couple = partial(
    build_alternative_formula_couple,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_dated_formula_couple = partial(
    build_dated_formula_couple,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_select_formula_couple = partial(
    build_select_formula_couple,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_simple_formula_couple = partial(
    build_simple_formula_couple,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


prestation_by_name.update(collections.OrderedDict((
    build_alternative_formula_couple(
        'age',
        [
            ir._age_from_birth,
            ir._age_from_agem,
            ],
        AgeCol(label = u"Âge (en années)", val_type = "age"),
        ),
    build_alternative_formula_couple(
        'agem',
        [
            ir._agem_from_birth,
            ir._agem_from_age,
            ],
        AgeCol(label = u"Âge (en mois)", val_type = "months"),
        ),

    ############################################################
    # Cotisations sociales
    ############################################################

    # Salaires
    build_simple_formula_couple('salbrut', FloatCol(function = cs._salbrut, label = u"Salaires bruts")),
    build_simple_formula_couple('cotpat', FloatCol(function = cs._cotpat)),
    build_simple_formula_couple('cotsal', FloatCol(function = cs._cotsal)),
    build_simple_formula_couple('salsuperbrut', FloatCol(function = cs._salsuperbrut, label = u"Salaires super bruts")),
#    build_simple_formula_couple('sal', FloatCol(function = cs._sal)),


    # Pension

    ############################################################
    # Prestation familiales
    ############################################################

    build_simple_formula_couple('smig75', BoolCol(function = pf._smig75, label = u"Indicatrice de salaire supérieur à 75% du smig")),
    build_simple_formula_couple('af_nbenf', FloatCol(function = pf._af_nbenf, entity = 'men',
        label = u"Nombre d'enfants au sens des allocations familiales")),
    build_simple_formula_couple('af', FloatCol(function = pf._af, entity = 'men', label = u"Allocations familiales")),
    build_simple_formula_couple('sal_uniq', BoolCol(function = pf._sal_uniq, entity = 'men', label = u"Indicatrice de salaire unique")),
    build_simple_formula_couple('maj_sal_uniq', FloatCol(function = pf._maj_sal_uniq, entity = 'men', label = u"Majoration du salaire unique")),
    build_simple_formula_couple('contr_creche', FloatCol(function = pf._contr_creche, entity = 'men', label = u"Contribution aux frais de crêche")),
    build_simple_formula_couple('pfam', FloatCol(function = pf._pfam, entity = 'men', label = u"Prestations familales")),

    ############################################################
    # Impôt sur le revenu
    ############################################################

    build_simple_formula_couple('marie', BoolCol(function = ir._marie, entity = 'foy')),
    build_simple_formula_couple('celdiv', BoolCol(function = ir._celib, entity = 'foy')),
    build_simple_formula_couple('divor', BoolCol(function = ir._divor, entity = 'foy')),
    build_simple_formula_couple('veuf', BoolCol(function = ir._veuf, entity = 'foy')),

    build_simple_formula_couple('nb_enf', FloatCol(function = ir._nb_enf, entity = 'foy')),
    build_simple_formula_couple('nb_enf_sup', FloatCol(function = ir._nb_enf_sup, entity = 'foy')),
    build_simple_formula_couple('nb_par', FloatCol(function = ir._nb_par, entity = 'foy')),
    build_simple_formula_couple('nb_infirme', FloatCol(function = ir._nb_infirme, entity = 'foy')),

#    build_simple_formula_couple('rbg', FloatCol(function = ir._rbg, entity = 'foy', label = u"Revenu brut global")),

    # Bénéfices industriels et commerciaux
    build_simple_formula_couple('bic', FloatCol(function = ir._bic, entity = 'foy')),

    build_simple_formula_couple('bic_ca_global', FloatCol(function = ir._bic_ca_global,
        label = u"Chiffre d’affaires global (BIC, cession de fond de commerce")),
    build_simple_formula_couple('bic_res_cession', FloatCol(function = ir._bic_res_cession, label = u"Résultat (BIC, cession de fond de commerce)")),
    build_simple_formula_couple('bic_benef_fiscal_cession', FloatCol(function = ir._bic_benef_fiscal_cession,
        label = u"Bénéfice fiscal (BIC, cession de fond de commerce)")),

    build_simple_formula_couple('bnc', FloatCol(function = ir._bnc, entity = 'foy')),

    build_simple_formula_couple('bnc_forf_benef_fiscal', FloatCol(function = ir._bnc_forf_benef_fiscal,
        label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)")),

    build_simple_formula_couple('beap', FloatCol(function = ir._beap, entity = 'foy')),
    build_simple_formula_couple('rvcm', FloatCol(function = ir._rvcm, entity = 'foy')),
    build_simple_formula_couple('fon_forf_bati', FloatCol(function = ir._fon_forf_bati, entity = 'foy')),
    build_simple_formula_couple('fon_forf_nbat', FloatCol(function = ir._fon_forf_nbat, entity = 'foy')),
    build_simple_formula_couple('rfon', FloatCol(function = ir._rfon, entity = 'foy')),

    build_simple_formula_couple('sal', FloatCol(function = ir._sal, entity = 'foy', label = u"Salaires y compris salaires en nature")),
    build_simple_formula_couple('sal_net', FloatCol(function = ir._sal_net, entity = 'foy', label = u"Salaires nets")),
    build_simple_formula_couple('pen_net', FloatCol(function = ir._pen_net, entity = 'foy')),
    build_simple_formula_couple('tspr', FloatCol(function = ir._tspr, entity = 'foy')),
    build_simple_formula_couple('retr', FloatCol(function = ir._retr, entity = 'foy')),
    build_simple_formula_couple('rng', FloatCol(function = ir._rng, entity = 'foy', label = u"Revenu net global")),

    # Déductions

    build_simple_formula_couple('deduc_fam', FloatCol(function = ir._deduc_fam, entity = 'foy',
        label = u"Déductions pour situation et charges de famille")),
    build_simple_formula_couple('deduc_rente', FloatCol(function = ir._deduc_rente, entity = 'foy',
        label = u"Arrérages et rentes payées à titre obligatoire et gratuit")),
    build_simple_formula_couple('ass_vie', FloatCol(function = ir._ass_vie, entity = 'foy', label = u"Primes afférentes aux contrats d'assurance-vie")),

    build_simple_formula_couple('smig', FloatCol(function = ir._smig, entity = 'foy',
        label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires")),

    build_simple_formula_couple('deduc_smig', FloatCol(function = ir._deduc_smig, entity = 'foy',
        label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG")),

    # Réductions d'impots

    build_simple_formula_couple('rni', FloatCol(function = ir._rni, entity = 'foy', label = u"Revenu net imposable")),
    build_simple_formula_couple('ir_brut', FloatCol(function = ir._ir_brut, entity = 'foy', label = u"Impôt avant non-imposabilité")),
    build_simple_formula_couple('irpp', FloatCol(function = ir._irpp, entity = 'foy', label = u"Impôt sur le revenu des personnes physiques")),

    ############################################################
    # Unité de consommation du ménage
    ############################################################
#    build_simple_formula_couple('uc', FloatCol(function = cm._uc, entity = 'men', label = u"Unités de consommation")),

#    ############################################################
#    # Catégories
#    ############################################################

#    build_simple_formula_couple('typ_men', IntPresta(cm._typ_men, entity = 'men', label = u"Type de ménage")),
#    build_simple_formula_couple('nb_ageq0', IntPresta(cl._nb_ageq0, entity = 'men', label = u"Effectifs des tranches d'âge quiquennal")),
#    build_simple_formula_couple('nbinde2', IntPresta(cl._nbinde2, entity = 'men', label = u"Nombre d'individus dans le ménage")),

    ############################################################
    # Totaux
    ############################################################

    build_simple_formula_couple('revdisp_i', FloatCol(function = cm._revdisp_i, label = u"Revenu disponible individuel")),
    build_simple_formula_couple('revdisp', FloatCol(function = cm._revdisp, entity = 'men', label = u"Revenu disponible du ménage")),
#    build_simple_formula_couple('nivvie', FloatCol(function = cm._nivvie, entity = 'men', label = u"Niveau de vie du ménage")),
    build_simple_formula_couple('rev_trav', FloatCol(function = cm._rev_trav)),
#    build_simple_formula_couple('pen', FloatCol(function = cm._pen)),

#    build_simple_formula_couple('rstnet', FloatCol(function = cm._rstnet)),
    build_simple_formula_couple('rev_cap', FloatCol(function = cm._rev_cap)),

    build_simple_formula_couple('impo', FloatCol(function = cm._impo)),
    )))

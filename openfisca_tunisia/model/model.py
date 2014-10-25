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


from functools import partial

from openfisca_core.columns import AgeCol, BoolCol, FloatCol
from openfisca_core.formulas import (
    build_alternative_formula,
    build_dated_formula,
    build_select_formula,
    build_simple_formula,
    )

from .. import entities

# Import model modules.
from . import common as cm
from . import cotsoc as cs
from . import irpp as ir
from . import pfam as pf


build_alternative_formula = partial(
    build_alternative_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_dated_formula = partial(
    build_dated_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_select_formula = partial(
    build_select_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )
build_simple_formula = partial(
    build_simple_formula,
    entity_class_by_symbol = entities.entity_class_by_symbol,
    )


build_alternative_formula(
    'age',
    [
        ir._age_from_birth,
        ir._age_from_agem,
        ],
    AgeCol(label = u"Âge (en années)", val_type = "age"),
    )
build_alternative_formula(
    'agem',
    [
        ir._agem_from_birth,
        ir._agem_from_age,
        ],
    AgeCol(label = u"Âge (en mois)", val_type = "months"),
    )

############################################################
# Cotisations sociales
############################################################

# Salaires
build_simple_formula('salbrut', FloatCol(function = cs._salbrut, label = u"Salaires bruts"))
build_simple_formula('cotpat', FloatCol(function = cs._cotpat))
build_simple_formula('cotsal', FloatCol(function = cs._cotsal))
build_simple_formula('salsuperbrut', FloatCol(function = cs._salsuperbrut, label = u"Salaires super bruts"))
#    build_simple_formula('sal', FloatCol(function = cs._sal))


# Pension

############################################################
# Prestation familiales
############################################################

build_simple_formula('smig75', BoolCol(function = pf._smig75,
    label = u"Indicatrice de salaire supérieur à 75% du smig"))
build_simple_formula('af_nbenf', FloatCol(function = pf._af_nbenf, entity = 'men',
    label = u"Nombre d'enfants au sens des allocations familiales"))
build_simple_formula('af', FloatCol(function = pf._af, entity = 'men', label = u"Allocations familiales"))
build_simple_formula('sal_uniq', BoolCol(function = pf._sal_uniq, entity = 'men',
    label = u"Indicatrice de salaire unique"))
build_simple_formula('maj_sal_uniq', FloatCol(function = pf._maj_sal_uniq, entity = 'men',
    label = u"Majoration du salaire unique"))
build_simple_formula('contr_creche', FloatCol(function = pf._contr_creche, entity = 'men',
    label = u"Contribution aux frais de crêche"))
build_simple_formula('pfam', FloatCol(function = pf._pfam, entity = 'men', label = u"Prestations familales"))

############################################################
# Impôt sur le revenu
############################################################

build_simple_formula('marie', BoolCol(function = ir._marie, entity = 'foy'))
build_simple_formula('celdiv', BoolCol(function = ir._celib, entity = 'foy'))
build_simple_formula('divor', BoolCol(function = ir._divor, entity = 'foy'))
build_simple_formula('veuf', BoolCol(function = ir._veuf, entity = 'foy'))

build_simple_formula('nb_enf', FloatCol(function = ir._nb_enf, entity = 'foy'))
build_simple_formula('nb_enf_sup', FloatCol(function = ir._nb_enf_sup, entity = 'foy'))
build_simple_formula('nb_par', FloatCol(function = ir._nb_par, entity = 'foy'))
build_simple_formula('nb_infirme', FloatCol(function = ir._nb_infirme, entity = 'foy'))

#    build_simple_formula('rbg', FloatCol(function = ir._rbg, entity = 'foy', label = u"Revenu brut global"))

# Bénéfices industriels et commerciaux
build_simple_formula('bic', FloatCol(function = ir._bic, entity = 'foy'))

build_simple_formula('bic_ca_global', FloatCol(function = ir._bic_ca_global,
    label = u"Chiffre d’affaires global (BIC, cession de fond de commerce"))
build_simple_formula('bic_res_cession', FloatCol(function = ir._bic_res_cession,
    label = u"Résultat (BIC, cession de fond de commerce)"))
build_simple_formula('bic_benef_fiscal_cession', FloatCol(function = ir._bic_benef_fiscal_cession,
    label = u"Bénéfice fiscal (BIC, cession de fond de commerce)"))

build_simple_formula('bnc', FloatCol(function = ir._bnc, entity = 'foy'))

build_simple_formula('bnc_forf_benef_fiscal', FloatCol(function = ir._bnc_forf_benef_fiscal,
    label = u"Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)"))

build_simple_formula('beap', FloatCol(function = ir._beap, entity = 'foy'))
build_simple_formula('rvcm', FloatCol(function = ir._rvcm, entity = 'foy'))
build_simple_formula('fon_forf_bati', FloatCol(function = ir._fon_forf_bati, entity = 'foy'))
build_simple_formula('fon_forf_nbat', FloatCol(function = ir._fon_forf_nbat, entity = 'foy'))
build_simple_formula('rfon', FloatCol(function = ir._rfon, entity = 'foy'))

build_simple_formula('sal', FloatCol(function = ir._sal, entity = 'foy',
    label = u"Salaires y compris salaires en nature"))
build_simple_formula('sal_net', FloatCol(function = ir._sal_net, entity = 'foy', label = u"Salaires nets"))
build_simple_formula('pen_net', FloatCol(function = ir._pen_net, entity = 'foy'))
build_simple_formula('tspr', FloatCol(function = ir._tspr, entity = 'foy'))
build_simple_formula('retr', FloatCol(function = ir._retr, entity = 'foy'))
build_simple_formula('rng', FloatCol(function = ir._rng, entity = 'foy', label = u"Revenu net global"))

# Déductions

build_simple_formula('deduc_fam', FloatCol(function = ir._deduc_fam, entity = 'foy',
    label = u"Déductions pour situation et charges de famille"))
build_simple_formula('deduc_rente', FloatCol(function = ir._deduc_rente, entity = 'foy',
    label = u"Arrérages et rentes payées à titre obligatoire et gratuit"))
build_simple_formula('ass_vie', FloatCol(function = ir._ass_vie, entity = 'foy',
    label = u"Primes afférentes aux contrats d'assurance-vie"))

build_simple_formula('smig', FloatCol(function = ir._smig, entity = 'foy',
    label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires"))

build_simple_formula('deduc_smig', FloatCol(function = ir._deduc_smig, entity = 'foy',
    label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG"))

# Réductions d'impots

build_simple_formula('rni', FloatCol(function = ir._rni, entity = 'foy', label = u"Revenu net imposable"))
build_simple_formula('ir_brut', FloatCol(function = ir._ir_brut, entity = 'foy',
    label = u"Impôt avant non-imposabilité"))
build_simple_formula('irpp', FloatCol(function = ir._irpp, entity = 'foy',
    label = u"Impôt sur le revenu des personnes physiques"))

############################################################
# Unité de consommation du ménage
############################################################
#    build_simple_formula('uc', FloatCol(function = cm._uc, entity = 'men', label = u"Unités de consommation"))

#    ############################################################
#    # Catégories
#    ############################################################

#    build_simple_formula('typ_men', IntPresta(cm._typ_men, entity = 'men', label = u"Type de ménage"))
#    build_simple_formula('nb_ageq0', IntPresta(cl._nb_ageq0, entity = 'men',
#        label = u"Effectifs des tranches d'âge quiquennal"))
#    build_simple_formula('nbinde2', IntPresta(cl._nbinde2, entity = 'men',
#        label = u"Nombre d'individus dans le ménage"))

############################################################
# Totaux
############################################################

build_simple_formula('revdisp_i', FloatCol(function = cm._revdisp_i, label = u"Revenu disponible individuel"))
build_simple_formula('revdisp', FloatCol(function = cm._revdisp, entity = 'men',
    label = u"Revenu disponible du ménage"))
#    build_simple_formula('nivvie', FloatCol(function = cm._nivvie, entity = 'men',
#         label = u"Niveau de vie du ménage"))
build_simple_formula('rev_trav', FloatCol(function = cm._rev_trav))
#    build_simple_formula('pen', FloatCol(function = cm._pen))

#    build_simple_formula('rstnet', FloatCol(function = cm._rstnet))
build_simple_formula('rev_cap', FloatCol(function = cm._rev_cap))

build_simple_formula('impo', FloatCol(function = cm._impo))

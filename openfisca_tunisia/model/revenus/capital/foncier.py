# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Revenus fonciers


# Régime réel

class fon_reel_fisc(Variable):
    column = IntCol
    entity = Individu


# Régime forfaitaire bâti

class fon_forf_bati_rec(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_rel(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_fra(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_tax(Variable):
    column = IntCol
    entity = Individu


# Régime forfaitaire non bâti

class fon_forf_nbat_rec(Variable):
    column = IntCol
    entity = Individu


class fon_forf_nbat_dep(Variable):
    column = IntCol
    entity = Individu


class fon_forf_nbat_tax(Variable):
    column = IntCol
    entity = Individu


class fon_sp(Variable):
    column = IntCol
    entity = Individu
    #  part dans les bénéfices ou les pertes de sociétés de personnes et assimilées qui réalisent des revenus fonciers

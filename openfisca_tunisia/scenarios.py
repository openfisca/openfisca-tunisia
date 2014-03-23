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
import datetime
import itertools
import json
import logging
import os
import time
import urllib2
import uuid

import numpy as np
from openfisca_core import legislations, simulations

from . import conv, entities


log = logging.getLogger(__name__)
N_ = lambda message: message


class Scenario(object):
    axes = None
    compact_legislation = None
    tax_benefit_system = None
    test_case = None
    year = None


    def init_single_entity(self, axes = None, enfants = None, foyer_fiscal = None, menage = None,
            parent1 = None, parent2 = None, year = None):
        if enfants is None:
            enfants = []
        assert parent1 is not None
        foyer_fiscal = foyer_fiscal.copy() if foyer_fiscal is not None else {}
        individus = []
        menage = menage.copy() if menage is not None else {}
        for index, individu in enumerate([parent1, parent2] + (enfants or [])):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = 'ind{}'.format(index)
            individus.append(individu)
            if index <= 1 :
                foyer_fiscal.setdefault('declarants', []).append(id)
                if index == 0:
                    menage['personne_de_reference'] = id
                else:
                    menage['conjoint'] = id
            else:
                foyer_fiscal.setdefault('personnes_a_charge', []).append(id)
                menage.setdefault('enfants', []).append(id)
        conv.check(self.make_json_or_python_to_attributes())(dict(
            axes = axes,
            test_case = dict(
                foyers_fiscaux = [foyer_fiscal],
                individus = individus,
                menages = [menage],
                ),
            year = year,
            ))
        return self

    def json_or_python_to_test_case(self, value, state = None):
        if value is None:
            return value, None
        if state is None:
            state = conv.default_state

        column_by_name = self.tax_benefit_system.column_by_name

        # First validation and conversion step
        test_case, error = conv.pipe(
            conv.test_isinstance(dict),
            conv.struct(
                dict(
                    foyers_fiscaux = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            declarant = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.empty_to_none,
                                                conv.not_none,
                                                conv.test(lambda declarant: len(declarant) <= 1,
                                                    error = N_(u'A "foyer_fiscal" must have at most 1 "declarant"'
                                                    ))
                                                ),
                                            personnes_a_charge = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'foy'
                                            ),
                                        )),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    individus = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(
                                        (column.name, column.json_to_python)
                                        for column in column_by_name.itervalues()
                                        if column.entity == 'ind' and column.name not in (
                                            'idfoy', 'idmen', 'quifoy', 'quimen')
                                        ),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    menages = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            autres = conv.pipe(
                                                # personnes ayant un lien autre avec la personne de référence
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            conjoint = conv.test_isinstance((basestring, int)),
                                                # conjoint de la personne de référence
                                            enfants = conv.pipe(
                                                # enfants de la personne de référence ou de son conjoint
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            personne_de_reference = conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'men'
                                            ),
                                        )),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    ),
                ),
            )(value, state = state)
        if error is not None:
            return test_case, error

        # Second validation step
        foyers_fiscaux_individus_id = set(test_case['individus'].iterkeys())
        menages_individus_id = set(test_case['individus'].iterkeys())
        test_case, error = conv.struct(
            dict(
                foyers_fiscaux = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            declarants = conv.uniform_sequence(conv.test_in_pop(foyers_fiscaux_individus_id)),
                            personnes_a_charge = conv.uniform_sequence(conv.test_in_pop(foyers_fiscaux_individus_id)),
                            ),
                        default = conv.noop,
                        ),
                    ),
                menages = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            autres = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                            conjoint = conv.test_in_pop(menages_individus_id),
                            enfants = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                            personne_de_reference = conv.test_in_pop(menages_individus_id),
                            ),
                        default = conv.noop,
                        ),
                    ),
                ),
            default = conv.noop,
            )(test_case, state = state)

        remaining_individus_id = foyers_fiscaux_individus_id.union(menages_individus_id)
        if remaining_individus_id:
            if error is None:
                error = {}
            for individu_id in remaining_individus_id:
                error.setdefault('individus', {})[individu_id] = state._(u"Individual is missing from {}").format(
                    u' & '.join(
                        word
                        for word in [
                            u'foyers_fiscaux' if individu_id not in foyers_fiscaux_individus_id else None,
                            u'menages' if individu_id not in menages_individus_id else None,
                            ]
                        if word is not None
                        ))

        return test_case, error



#
# class Scenario(object):
#     axes = None
#     compact_legislation = None
#     tax_benefit_system = None
#     test_case = None
#     year = Nonefrom __future__ import division
#
# import datetime
# import pickle
#
# from openfisca_core import __version__ as VERSION
#
# from . import ENTITIES_INDEX
#
#
# class Scenario(object):
#     def __init__(self):
#         super(Scenario, self).__init__()
#         self.year = None
#         self.indiv = {}
#         # indiv est un dict de dict. La clé est le noi de l'individu
#         # Exemple :
#         # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0,
#         #     'birth': datetime.date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
#         self.declar = {}
#
#         # menage est un dict de dict la clé est la pref
#         self.menage = {0:{'loyer':500,'so':3, 'code_postal':001}}
#
#         # on ajoute un individu, déclarant et chef de famille
#         self.addIndiv(0, datetime.date(1975, 1, 1), 'vous', 'chef')
#
#         self.nmen = None
#         self.x_axis = None
#         self.maxrev = None
#         self.same_rev_couple = None
#         self.year = None
#
#     def copy(self):
#         from copy import deepcopy
#         return deepcopy(self)
#
#     def check_consistency(self):
#         '''
#         Vérifie que le ménage entré est valide
#         '''
#         for noi, vals in self.indiv.iteritems():
#             age = self.year - vals['birth'].year
#             if age < 0:
#                 return u"L'année de naissance doit être antérieure à celle de la simulation (voir Fichier->Paramètres pour régler la date de la simulation"
#             if vals['quifoy'] in ('vous', 'conj'):
#                 if age < 18: return u'Le déclarant et son éventuel conjoint doivent avoir plus de 18 ans'  # TODO
#             else:
#                 if age > 25 and (vals['inv']==0): return u'Les personnes à charges doivent avoir moins de 25 ans si elles ne sont pas invalides'
# #            if vals['quifoy'] == 'conj' and not vals['quifam'] == 'part':
# #                return u"Un conjoint sur la déclaration d'impôt doit être le partenaire dans la famille"
#         return ''
#
#     def modify(self, noi, newQuifoy = None, newFoyer = None):
#         oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
#         if newQuifoy == None: newQuifoy = oldQuifoy
#         if newFoyer == None: newFoyer = oldFoyer
#         if oldQuifoy == 'vous':
#             toAssign = self.getIndiv(oldFoyer, 'noidec')
#             del self.declar[oldFoyer]
#             self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
#             for person in toAssign:
#                 oldPos = self.indiv[person]['quifoy']
#                 if oldPos == "vous": continue
#                 else: self.modify(person, newQuifoy = oldPos, newFoyer = 0)
#         else:
#             self._assignPerson(noi, quifoy = newQuifoy, foyer = newFoyer)
#         self.genNbEnf()
#
#     def hasConj(self, noidec):
#         '''
#         Renvoie True s'il y a un conjoint dans la déclaration 'noidec', sinon False
#         '''
#         for vals in self.indiv.itervalues():
#             if (vals['noidec'] == noidec) and (vals['quifoy']=='conj'):
#                 return True
#         return False
#
#     def _assignVous(self, noi):
#         '''
#         Ajoute la personne numéro 'noi' et crée son foyer
#         '''
#         self.indiv[noi]['quifoy'] = 'vous'
#         self.indiv[noi]['noidec'] = noi
#         self.declar.update({noi:{}})
#
#     def _assignConj(self, noi, noidec):
#         '''
#         Ajoute la personne numéro 'noi' à la déclaration numéro 'noidec' en tant
#         que 'conj' si declar n'a pas de conj. Sinon, cherche le premier foyer sans
#         conjoint. Sinon, crée un nouveau foyer en tant que vous.
#         '''
#         decnum = noidec
#         if (noidec not in self.declar) or self.hasConj(noidec):
#             for k in self.declar:
#                 if not self.hasConj(k):
#                     decnum = k
#         if not self.hasConj(decnum):
#             self.indiv[noi]['quifoy'] = 'conj'
#             self.indiv[noi]['noidec'] = decnum
#         else:
#             self._assignVous(noi)
#
#     def _assignPac(self, noi, noidec):
#         '''
#         Ajoute la personne numéro 'noi' à la déclaration numéro 'noidec' en tant
#         que 'pac'.
#         '''
#         self.indiv[noi]['quifoy'] = 'pac0'
#         self.indiv[noi]['noidec'] = noidec
#
#     def _assignPerson(self, noi, quifoy = None, foyer = None, quifam = None, famille = None):
#         if quifoy is not None:
#             if   quifoy     == 'vous': self._assignVous(noi)
#             elif quifoy     == 'conj': self._assignConj(noi, foyer)
#             elif quifoy[:3] == 'pac' : self._assignPac(noi, foyer)
#
#         self.genNbEnf()
#
#     def rmvIndiv(self, noi):
#         oldFoyer, oldQuifoy = self.indiv[noi]['noidec'], self.indiv[noi]['quifoy']
#         oldFamille, oldQuifam = self.indiv[noi]['noichef'], self.indiv[noi]['quifam']
#         if oldQuifoy == 'vous':
#             toAssign = self.getIndiv(oldFoyer, 'noidec')
#             for person in toAssign:
#                 if self.indiv[person]['quifoy']     == 'conj': self._assignPerson(person, quifoy = 'conj', foyer = 0)
#                 if self.indiv[person]['quifoy'][:3] == 'pac' : self._assignPerson(person, quifoy = 'pac' , foyer = 0)
#             del self.declar[noi]
#         if oldQuifam == 'chef':
#             toAssign = self.getIndiv(oldFamille, 'noichef')
#             for person in toAssign:
#                 if self.indiv[person]['quifam']     == 'part': self._assignPerson(person, quifam = 'part', famille = 0)
#                 if self.indiv[person]['quifam'][:3] == 'enf' : self._assignPerson(person, quifam = 'enf' , famille = 0)
#             del self.famille[noi]
#         del self.indiv[noi]
#         self.genNbEnf()
#
#     def getIndiv(self, noi, champ = 'noidec'):
#         for person, vals in self.indiv.iteritems():
#             if vals[champ] == noi:
#                 yield person
#
#     def addIndiv(self, noi, birth, quifoy, quifam):
#         self.indiv.update({noi:{'birth':birth,
#                                 'inv': 0,
#                                 'activite':0,
#                                 'quifoy': 'none',
#                                 'quifam': 'none',
#                                 'noidec':  0,
#                                 'noichef': 0,
#                                 'noipref': 0}})
#
#         self._assignPerson(noi, quifoy = quifoy, foyer = 0, quifam = quifam, famille = 0)
#         self.updateMen()
#
#     def nbIndiv(self):
#         return len(self.indiv)
#
#     def genNbEnf(self):
#         for noi, vals in self.indiv.iteritems():
#             if vals.has_key('statmarit'):
#                 statmarit = vals['statmarit']
#             else: statmarit = 2
#             if self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (1,5):
#                 statmarit = 1
#             elif not self.hasConj(noi) and (noi == vals['noidec']) and not statmarit in (2,3,4):
#                 statmarit = 2
#             # si c'est un conjoint, même statmarit que 'vous'
#             if vals['quifoy'] == 'conj':
#                 statmarit = self.indiv[vals['noidec']]['statmarit']
#             vals.update({'statmarit':statmarit})
#
#         for noidec, vals in self.declar.iteritems():
#             vals.update(self.NbEnfFoy(noidec))
#
#     def NbEnfFoy(self, noidec):
#         out = {}
#         n = 0
#         for vals in self.indiv.itervalues():
#             if (vals['noidec']==noidec) and (vals['quifoy'][:3]=='pac'):
#                 n += 1
#                 if (self.year - vals['birth'].year >= 18) and vals['inv'] == 0: out['nbJ'] += 1
#                 vals['quifoy'] = 'pac%d' % n
#         return out
#         pass
#
#     def updateMen(self):
#         '''
#         Il faut virer cela
#         '''
#         people = self.indiv
#         for noi in xrange(self.nbIndiv()):
#             if   noi == 0: quimen = 'pref'
#             elif noi == 1: quimen = 'cref'
#             else:  quimen = 'enf%d' % (noi-1)
#             people[noi].update({'quimen': quimen,
#                                 'noipref': 0})
#
#     def __repr__(self):
#         outstr = "INDIV" + '\n'
#         for key, val in self.indiv.iteritems():
#             outstr += str(key) + str(val) + '\n'
#         outstr += "DECLAR" + '\n'
#         for key, val in self.declar.iteritems():
#             outstr += str(key) + str(val) + '\n'
#         outstr += "MENAGE" + '\n'
#         for key, val in self.menage.iteritems():
#             outstr += str(key) + str(val) + '\n'
#         return outstr
#
#     def saveFile(self, fileName):
#         outputFile = open(fileName, 'wb')
#         pickle.dump({'version': VERSION, 'indiv': self.indiv, 'declar': self.declar, 'menage': self.menage}, outputFile)
#         outputFile.close()
#
#     def openFile(self, fileName):
#         inputFile = open(fileName, 'rb')
#         S = pickle.load(inputFile)
#         inputFile.close()
#         self.indiv = S['indiv']
#         self.declar = S['declar']
#         self.menage = S['menage']
#
#     def populate_datatable(self, datatable):
#         '''
#         Popualte a datatable from a given scenario
#         '''
#         from pandas import DataFrame, concat
#         import numpy as np
#         scenario = self
#
#         if self.nmen is None:
#             raise Exception('france.scenario: self.nmen should be not None')
#
#         nmen = self.nmen
#         same_rev_couple = self.same_rev_couple
#         datatable.NMEN = nmen
#         datatable._nrows = datatable.NMEN*len(scenario.indiv)
#         datesim = datatable.datesim
#         datatable.table = DataFrame()
#
#         idmen = np.arange(60001, 60001 + nmen)
#
#         for noi, dct in scenario.indiv.iteritems():
#             birth = dct['birth']
#             age = datesim.year- birth.year
#             agem = 12*(datesim.year- birth.year) + datesim.month - birth.month
#             noidec = dct['noidec']
#             quifoy = datatable.column_by_name.get('quifoy').enum[dct['quifoy']]
#
#             quimen = datatable.column_by_name.get('quimen').enum[dct['quimen']]
#             dct = {'noi': noi*np.ones(nmen),
#                    'age': age*np.ones(nmen),
#                    'agem': agem*np.ones(nmen),
#                    'quimen': quimen*np.ones(nmen),
#                    'quifoy': quifoy*np.ones(nmen),
#                    'idmen': idmen,
#                    'idfoy': idmen*100 + noidec}
#
#             datatable.table = concat([datatable.table, DataFrame(dct)], ignore_index = True)
#
#         datatable.gen_index(ENTITIES_INDEX)
#
#         for name, column in datatable.column_by_name.iteritems():
#             if name not in datatable.table:
#                 datatable.table[name] = column._default
#
#         entity = 'men'
#         nb = datatable.index[entity]['nb']
#         for noi, dct in scenario.indiv.iteritems():
#             for var, val in dct.iteritems():
#                 if var in ('birth', 'noipref', 'noidec', 'noichef', 'quifoy', 'quimen', 'quifam'):
#                     continue
#                 if not datatable.index[entity] is None:
#                     datatable.set_value(var, np.ones(nb)*val, entity, noi)
#             del var, val
#
#         entity = 'foy'
#         nb = datatable.index[entity]['nb']
#         for noi, dct in scenario.declar.iteritems():
#             for var, val in dct.iteritems():
#                 if not datatable.index[entity][noi] is None:
#                     datatable.set_value(var, np.ones(nb)*val, entity, noi)
#
#         index = datatable.index['men']
#         nb = index['nb']
#         entity = "men"
#         for noi, dct in scenario.menage.iteritems():
#             for var, val in dct.iteritems():
#                 if not index[noi] is None:
#                     datatable.set_value(var, np.ones(nb)*val, entity, noi)
#
#             del var, val
#
#         if nmen>1:
#             if self.maxrev is None:
#                 raise Exception('tunisia.utils.Scenario: self.maxrev should not be None')
#             maxrev = self.maxrev
#             datatable.MAXREV = maxrev
#
#             x_axis = self.x_axis
#             if x_axis is None:
#                 raise Exception('tunisia.utils.Scenario: self.x_axis should not be None')
#             var = None
#             for axe in model.x_axes.itervalues():
#                 if axe.name == x_axis:
#                     datatable.XAXIS = var = axe.col_name
#             if var is None:
#                 datatable.XAXIS = x_axis
#                 var = x_axis
#
#             vls = np.linspace(0, maxrev, nmen)
#             if same_rev_couple is True:
#                 entity = 'men'
#                 datatable.set_value(var, 0.5*vls, entity, opt = 0)
#                 datatable.set_value(var, 0.5*vls, entity, opt = 1)
#             else:
#                 datatable.set_value(var, vls, entity, opt = 0)

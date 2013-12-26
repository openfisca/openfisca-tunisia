# -*- coding:utf-8 -*-Boll
# Copyright © 2012 Clément Schaff, Mahdi Ben Jelloul

"""
OpenFiscaTn, Logiciel libre de simulation du système socio-fiscal tunisien
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""


from datetime import date

from openfisca_core.columns import Prestation, BoolPresta
from openfisca_core.descriptions import ModelDescription

from . import common as cm
from . import cotsoc as cs
from . import irpp as ir
from . import pfam as pf


class OutputDescription(ModelDescription):
    """
    Model description
    """

    ############################################################
    # Cotisations sociales
    ############################################################
    
    # Salaires
    salbrut = Prestation(cs._salbrut, label="Salaires bruts")
    cotpat  = Prestation(cs._cotpat)
    cotsal  = Prestation(cs._cotsal)
    salsuperbrut = Prestation(cs._salsuperbrut, label="Salaires super bruts")
#    sal = Prestation(cs._sal)        
    

    # Pension
    
    ############################################################
    # Prestation familiales
    ############################################################
    
    smig75   = BoolPresta(pf._smig75, label="Indicatrice de salaire supérieur à 75% du smig" ) 
    af_nbenf = Prestation(pf._af_nbenf, entity='men', label="Nombre d'enfants au sens des allocations familiales")
    af  = Prestation(pf._af, entity='men', label="Allocations familiales")
    sal_uniq = BoolPresta(pf._sal_uniq, entity='men', label="Indicatrice de salaire unique")
    maj_sal_uniq = Prestation(pf._maj_sal_uniq, entity='men', label="Majoration du salaire unique")
    contr_creche = Prestation(pf._contr_creche, entity='men', label="Contribution aux frais de crêche")
    pfam = Prestation(pf._pfam, entity='men', label="Prestations familales")
    
    ############################################################
    # Impôt sur le revenu
    ############################################################

    marie = BoolPresta(ir._marie, entity='foy')
    celdiv = BoolPresta(ir._celib, entity='foy')
    divor = BoolPresta(ir._divor, entity='foy')
    veuf = BoolPresta(ir._veuf, entity='foy')
    
    nb_enf = Prestation(ir._nb_enf, entity='foy')
    nb_enf_sup = Prestation(ir._nb_enf_sup, entity='foy')
    nb_par     = Prestation(ir._nb_par, entity='foy')
    nb_infirme = Prestation(ir._nb_infirme, entity='foy')
    
#    rbg = Prestation(ir._rbg, entity='foy', label = u"Revenu brut global")
    
    
    # Bénéfices industriels et commerciaux
    bic = Prestation(ir._bic, entity='foy')
 
    bic_ca_global = Prestation(ir._bic_ca_global, label="Chiffre d’affaires global (BIC, cession de fond de commerce")
    bic_res_cession = Prestation(ir._bic_res_cession, label="Résultat (BIC, cession de fond de commerce)")
    bic_benef_fiscal_cession = Prestation(ir._bic_benef_fiscal_cession, label= "Bénéfice fiscal (BIC, cession de fond de commerce)")   
    
    bnc = Prestation(ir._bnc, entity='foy')
    
    bnc_forf_benef_fiscal = Prestation(ir._bnc_forf_benef_fiscal, label="Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)")
    
    
    beap = Prestation(ir._beap, entity='foy')
    rvcm = Prestation(ir._rvcm, entity='foy')
    fon_forf_bati = Prestation(ir._fon_forf_bati, entity='foy')
    fon_forf_nbat = Prestation(ir._fon_forf_nbat, entity='foy')
    rfon = Prestation(ir._rfon, entity='foy')

    sal = Prestation(ir._sal, entity='foy', label="Salaires y compris salaires en nature")
    sal_net = Prestation(ir._sal_net, entity='foy', label="Salaires nets")
    pen_net = Prestation(ir._pen_net, entity='foy')                               
    tspr    = Prestation(ir._tspr, entity='foy')
    retr    = Prestation(ir._retr, entity='foy')
    rng = Prestation(ir._rng, entity='foy', label=u"Revenu net global")
    
    # Déductions
    
    deduc_fam = Prestation(ir._deduc_fam, entity='foy', label = u"Déductions pour situation et charges de famille")
    deduc_rente     = Prestation(ir._deduc_rente, entity='foy', label = u"Arrérages et rentes payées à titre obligatoire et gratuit")
    ass_vie   = Prestation(ir._ass_vie, entity='foy', label = u"Primes afférentes aux contrats d'assurance-vie")
   
    smig = Prestation(ir._smig, entity='foy', label = u"Indicatrice de SMIG ou SMAG déduite du montant des salaires")
    
    deduc_smig = Prestation(ir._deduc_smig, entity='foy', label = u"Déduction supplémentaire pour les salariés payés au SMIG et SMAG")
   
    # Réductions d'impots
   
    
    rni = Prestation(ir._rni, entity='foy', label = u"Revenu net imposable")
    ir_brut = Prestation(ir._ir_brut, entity='foy', label = u"Impôt avant non-imposabilité")
    irpp = Prestation(ir._irpp, entity='foy', label = u"Impôt sur le revenu des personnes physiques")

    ############################################################
    # Unité de consommation du ménage
    ############################################################
#    uc = Prestation(cm._uc, 'men', label = u"Unités de consommation")

#    ############################################################
#    # Catégories
#    ############################################################
#    
#    typ_men = IntPresta(cm._typ_men, 'men', label = u"Type de ménage")
#    nb_ageq0 = IntPresta(cl._nb_ageq0, 'men', label = u"Effectifs des tranches d'âge quiquennal")
#    nbinde2 = IntPresta(cl._nbinde2, 'men', label = u"Nombre d'individus dans le ménage")
#
    ############################################################
    # Totaux
    ############################################################

    revdisp_i = Prestation(cm._revdisp_i, label = u"Revenu disponible individuel")
    revdisp = Prestation(cm._revdisp, 'men', label = u"Revenu disponible du ménage")
    nivvie = Prestation(cm._nivvie, 'men', label = u"Niveau de vie du ménage")
    rev_trav = Prestation(cm._rev_trav)
#    pen = Prestation(cm._pen)
#    
#    rstnet = Prestation(cm._rstnet)
    rev_cap = Prestation(cm._rev_cap)
#    
    
    impo = Prestation(cm._impo)


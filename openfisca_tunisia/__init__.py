# -*- coding: utf-8 -*-

# This file is part of OpenFisca
# Copyright © 2012 Mahdi Ben Jelloul, Clément Schaff 
# Licensed under the terms of the GPL License v3 or later version
# (see openfisca_tunisia/__init__.py for details)


# Model parameters
ENTITIES_INDEX = ['men', 'foy']

# Data
#WEIGHT = "wprm"
#WEIGHT_INI = "wprm_init"


# Some variables needed by the test case plugins
CURRENCY = u"DT"


# Some variables needed by the test case graph widget


REVENUES_CATEGORIES = {'imposable' : ['sal',]}


XAXIS_PROPERTIES = { 'sali': {
                              'name' : 'sal',
                              'typ_tot' : {'salsuperbrut' : 'Salaire super brut',
                                           'salbrut': 'Salaire brut',
                                           'sal':  'Salaire imposable',
                                           'salnet': 'Salaire net'},
                              'typ_tot_default' : 'sal'},
                             }

# Some variables used by other plugins

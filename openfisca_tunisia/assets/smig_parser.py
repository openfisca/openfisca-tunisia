# -*- coding: utf-8 -*-


import datetime
import os
import pandas as pd
import pkg_resources

# SMIG-40-48.xlsx : 
# https://drive.google.com/file/d/1u3ykLgB9mVFvJ6ru1BjmK-S53bs5KsNa/view?usp=sharing
smig_1990_2010_path = os.path.join(
    pkg_resources.get_distribution('openfisca-tunisia').location,
    'openfisca_tunisia',
    'assets',
    'SMIG-40-48.xlsx',
    )


# SMIGSMAG.xlsx :
# https://drive.google.com/file/d/1wr93GvqYz48kT2gCv6PMMgzc3Oa7Mgsz/view?usp=sharing
smig_all_path = os.path.join(
    pkg_resources.get_distribution('openfisca-tunisia').location,
    'openfisca_tunisia',
    'assets',
    'SMIGSMAG.xlsx',
    )


smig_1990_2010 = pd.read_excel(
    smig_1990_2010_path,
    header = 9,
    parse_cols = "B,C,G",
    names = ['smig_horaire', 'smig_mensuel', 'deb'],
    )

smig_40h = smig_1990_2010.loc[:25].copy()
smig_40h['deb'] = pd.to_datetime(smig_40h.deb, dayfirst = True)
smig_40h['fin'] = smig_40h.deb.shift(-1) + datetime.timedelta(days=-1)

smig_48h = smig_1990_2010.loc[37:].copy()
smig_48h.deb = pd.to_datetime(smig_48h.deb, dayfirst = True)
smig_48h['fin'] = smig_48h.deb.shift(-1) + datetime.timedelta(days=-1)
smig_48h.smig_horaire = (smig_48h.smig_horaire * 1000).astype(int)
smig_48h = smig_48h.reset_index(drop = True)

smig_all = pd.read_excel(
    smig_all_path,
    parse_cols = "A:D",
    names = ['type', 'deb', 'fin', 'smig_horaire'],
    ).sort_values(['type', 'deb'])

smig = smig_all.query("type == 'SMIG'").reset_index(drop = True)

verif = (smig
    .merge(smig_48h, how = 'outer', on = 'deb')
    .query('(smig_horaire_x != smig_horaire_y)') # fin_y != fin_y to get NaNs
    )



header = """<CODE code="smig_horaire" description="SMIG horaire" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smig.deb.loc[i].date()),
    str(smig.fin.loc[i].date()),
    str(smig.smig_horaire.loc[i] / 1000)
    ) for i in range(len(smig)-1, -1, -1)
    ]
print "".join([header] + parts + [footer])


smag = smig_all.query("type == 'SMAG'").reset_index()
header = """<CODE code="smag_horaire" description="SMAG horaire" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smag.deb.loc[i].date()),
    str(smag.fin.loc[i].date()),
    str(smag.smig_horaire.loc[i] / 1000)
    ) for i in range(len(smig), 0, -1)
    ]
print "".join([header] + parts + [footer])


header = """<CODE code="smig_40h_mensuel" description="SMIG 40h mensuel" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smig_40h.deb.loc[i].date()),
    str(smig_40h.fin.loc[i].date()),
    str(smig_40h.smig_mensuel.loc[i])
    ) for i in range(len(smig_40h)-1, -1, -1)
    ]
print "".join([header] + parts + [footer])


header = """<CODE code="smig_48h_mensuel" description="SMIG 48h mensuel" format="float" type="monetary">
"""
footer = """</CODE>
"""
parts = ["""<VALUE deb="{}" fin="{}" valeur="{}" />
""".format(
    str(smig_48h.deb.loc[i].date()),
    str(smig_48h.fin.loc[i].date()),
    str(smig_48h.smig_mensuel.loc[i])
    ) for i in range(len(smig_48h)-1, -1, -1)
    ]
print "".join([header] + parts + [footer])

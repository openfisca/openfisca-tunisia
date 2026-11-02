"""Prestations familiales : à qui elles sont servies et par quel organisme (`pf_allocataire`, `pf_payeur`).

Le moteur vaut pour les deux secteurs. Secteur public : les 81 cas de la circulaire n° 42 (indemnité
familiale et indemnité pour salaire unique). Secteur privé : la loi n° 60-30 (JORT n° 57 des
13-16 décembre 1960, p. 1602-1613, articles 51 à 67 ; loi n° 96-65, JORT n° 60 de 1996), lue
dans la section « Qui perçoit l'allocation » du chapitre des prestations familiales du précis.
Le secteur est porté par la position des parents (`agent_public` ou non), comme dans l'annexe :
un enfant que l'annexe ne range dans aucun cas, dont un parent est salarié, relève du secteur privé.

Règle du secteur privé, telle qu'elle est lue (voir `pf_allocataire`) :

- du 1er avril 1961 au 3 août 1996, l'article 55, alinéa 3, quand le père et la mère ouvrent tous
  deux droit, ne sert que l'allocation du père, la mère pouvant réclamer la différence ;
  l'article 64 verse les allocations à la personne qui a la garde ; l'article 53 énumère les
  personnes du chef desquelles elles sont dues (père ou mère, adoptant ou son conjoint, tuteur
  officieux salarié, personne ayant la garde) ;
- depuis le 4 août 1996 (loi n° 96-65), l'article 55, alinéa 3 nouveau, fait servir l'allocation à
  la personne ayant la garde, et l'allocation la plus élevée si les montants diffèrent ;
- le payeur est la caisse nationale de sécurité sociale (article 65).

La garde est une entrée (`pf_garde_enfant`, ou `pf_situation_parents` pour les divorces avec
garde au père ou à la mère). Dans un couple non séparé, la loi ne dit pas ce que « garde »
veut dire : le modèle n'en parle pas et ne désigne personne quand l'article 55 ne suffit pas.

Source : circulaire du Premier ministre n° 42 du 25 octobre 1996, « la gestion des indemnités
à caractère familial dans le secteur public », JORT n° 89 du 5 novembre 1996 (p. 2534-2552 de l'édition arabe, texte authentique) ;
annexe 2, « Les indemnités familiales au titre des enfants de l'agent public, ou de ses
enfants adoptés, et l'indemnité pour salaire unique » (p. 2537-2550 de l'édition arabe ;
JORT n° 94 du 22 novembre 1996, p. 2353-2362, traduction française). La circulaire rappelle que le décret du 22 novembre 1918
règle l'indemnité familiale et le décret du 24 février 1944 l'indemnité pour salaire unique.

L'annexe 2 range quatre-vingt-un cas, codés de 1 à 81, en sept situations : I parents en vie
et non divorcés (p. 2353-2355), II père décédé (p. 2355-2356), III mère décédée (p. 2356),
IV divorce avec garde au père (p. 2357), V divorce avec garde à la mère (p. 2358-2359),
VI divorce avec garde partagée (p. 2360-2361), VII tuteur ou tutrice (p. 2362). Chaque cas
croise la position du père, celle de la mère et celle de l'enfant, et dit à qui chacune des
deux indemnités est servie. Le tableau est transcrit dans le précis socio-fiscal de la Tunisie
(chapitre des prestations familiales, tableaux « Circulaire n° 42, annexe 2, I à VII »).

Périmètre : la règle porte sur QUI est servi, et par quel organisme lorsque l'annexe le dit.
Les montants (décret n° 96-1906 pour l'indemnité familiale, circulaire pour le salaire unique)
et les conditions d'enfant (âge, rang, handicap) ne sont pas calculés ici.

Modèle. Les deux parents peuvent ne pas appartenir au même ménage que l'enfant (divorce,
décès, tutelle) : la situation se décrit donc sur l'enfant, entité `Individu`, par des entrées.
Chaque enfant a son propre résultat, ce qui permet la garde partagée enfant par enfant.

Cas lus dans l'édition arabe (JORT n° 89, p. 2540 et 2542), que la traduction française
laissait ambigus :

- cas 42 et 43 (III-A et III-B) : le père, agent public non remarié, ne perçoit pas la pension
  de réversion de la mère décédée au cas 42 (indemnité pour salaire unique servie au père) et
  la perçoit au cas 43 (non servie) ; la traduction française disait « ne bénéficiant pas » aux
  deux lignes. La mère y est seulement « décédée » : sa position est indifférente.
- cas 34 (II-A) : l'indemnité est « servie par la caisse de retraite » dans les deux éditions,
  sans nommer le bénéficiaire. Le modèle retient la mère (déduit : elle perçoit déjà la
  pension de réversion et les indemnités familiales de la caisse) ; le texte ne le dit pas.

Les combinaisons absentes de l'annexe donnent `non_designe` : l'annexe ne dit rien
des parents remariés dans les situations II à VI, ni des enfants d'un premier mariage hors
de la situation I.
"""

from numpy import zeros
from openfisca_core.indexed_enums import EnumArray

from openfisca_tunisia.variables.base import *  # noqa F401


REFERENCE_CIRCULAIRE = "https://www.pist.tn/jort/1996/1996F/Jo09496.pdf"


class SituationParents(Enum):
    __order__ = "parents_en_vie_non_divorces pere_decede mere_decedee divorce_garde_pere divorce_garde_mere divorce_garde_partagee tutelle"  # noqa: E501
    parents_en_vie_non_divorces = "Père et mère en vie, non divorcés (I)"
    pere_decede = "Père décédé, mère non remariée (II)"
    mere_decedee = "Mère décédée, père non remarié (III)"
    divorce_garde_pere = "Divorce, le père assure la garde et n'est pas remarié (IV)"
    divorce_garde_mere = "Divorce, la mère assure la garde et n'est pas remariée (V)"
    divorce_garde_partagee = "Divorce, garde assurée conjointement par les parents, non remariés (VI)"  # noqa: E501
    tutelle = "Enfant sous la tutelle d'un tuteur ou d'une tutrice (VII)"


class FiliationEnfant(Enum):
    __order__ = "communs premier_mariage_pere premier_mariage_mere"
    communs = "Enfant commun du père et de la mère"
    premier_mariage_pere = "Enfant d'un premier mariage du père, à sa charge"
    premier_mariage_mere = "Enfant d'un premier mariage de la mère, à sa charge"


class StatutParent(Enum):
    """Position d'un parent dans l'annexe 2 (pour un parent décédé, sa position de son vivant)."""

    __order__ = "non_renseigne agent_public activite_liberale salarie salarie_beneficiaire_indemnites_familiales salarie_non_beneficiaire_indemnites_familiales sans_activite retraite retraite_regime_ouvrant_droit retraite_regime_sans_droit agent_public_reversion_et_indemnites_familiales agent_public_reversion_sans_indemnites_familiales agent_public_sans_reversion_ni_indemnites_familiales agent_public_sans_reversion agent_public_avec_reversion"  # noqa: E501
    non_renseigne = "Non renseigné"
    agent_public = "Agent public"
    activite_liberale = "Exerce une activité professionnelle libérale"
    salarie = "Salarié(e), sans distinction de droit aux indemnités familiales"
    salarie_beneficiaire_indemnites_familiales = "Salarié bénéficiant des indemnités familiales"
    salarie_non_beneficiaire_indemnites_familiales = "Salarié ne bénéficiant pas des indemnités familiales"  # noqa: E501
    sans_activite = "N'exerce pas d'activité professionnelle rémunérée et ne bénéficie pas d'une pension"  # noqa: E501
    retraite = "Titulaire d'une pension de retraite (ou d'une des caisses sociales)"
    retraite_regime_ouvrant_droit = "Pension d'un régime ouvrant droit aux indemnités familiales"
    retraite_regime_sans_droit = "Pension d'un régime n'ouvrant pas droit aux indemnités familiales"  # noqa: E501
    agent_public_reversion_et_indemnites_familiales = "Agent public bénéficiant de la pension de réversion et des indemnités familiales"  # noqa: E501
    agent_public_reversion_sans_indemnites_familiales = "Agent public bénéficiant de la pension de réversion et non bénéficiaire des indemnités familiales"  # noqa: E501
    agent_public_sans_reversion_ni_indemnites_familiales = "Agent public ne bénéficiant ni des indemnités familiales ni de la pension de réversion"  # noqa: E501
    agent_public_sans_reversion = "Agent public non remarié ne bénéficiant pas de la pension de réversion (mère décédée)"  # noqa: E501
    agent_public_avec_reversion = "Agent public non remarié bénéficiant de la pension de réversion (mère décédée)"  # noqa: E501


class StatutTuteur(Enum):
    __order__ = "non_renseigne celibataire marie_conjoint_sans_activite marie_conjoint_avec_revenu"
    non_renseigne = "Non renseigné"
    celibataire = "Le tuteur (la tutrice) est célibataire"
    marie_conjoint_sans_activite = "Marié(e) à un conjoint n'exerçant pas une activité professionnelle rémunérée"  # noqa: E501
    marie_conjoint_avec_revenu = "Marié(e) à un conjoint disposant d'un revenu professionnel ou d'une pension"  # noqa: E501


class GardeEnfant(Enum):
    __order__ = "non_renseigne pere mere"
    non_renseigne = "Non renseigné"
    pere = "Garde assurée par le père"
    mere = "Garde assurée par la mère"


class Allocataire(Enum):
    __order__ = "non_designe non_servie pere mere tuteur mere_montant_anterieur_remariage pere_mere_pouvant_reclamer_difference"  # noqa: E501
    non_designe = "Personne que le texte lu ne permet pas de désigner avec les données saisies (cas non codé)"  # noqa: E501
    non_servie = "Non servie"
    pere = "Servie au père"
    mere = "Servie à la mère"
    tuteur = "Servie au tuteur ou à la tutrice"
    mere_montant_anterieur_remariage = "Servie à la mère, pour le montant dont elle bénéficiait avant le second mariage"  # noqa: E501
    # Secteur privé, du 1er avril 1961 au 3 août 1996 : loi n° 60-30, article 55, alinéa 3 (JORT
    # n° 57 des 13-16 décembre 1960, p. 1602-1613) : quand le père et la mère ouvrent tous deux
    # droit, « seule l'allocation due au père » est servie ; la mère peut demander à recevoir la
    # différence entre les allocations qui pourraient lui être attribuées et celles du père.
    pere_mere_pouvant_reclamer_difference = "Servie au père seul ; la mère peut réclamer la différence (loi n° 60-30, art. 55, al. 3, 1961-1996)"  # noqa: E501


class Payeur(Enum):
    __order__ = "non_precise employeur_du_pere cnss caisse_de_retraite"
    non_precise = "L'annexe ne nomme pas l'organisme"
    employeur_du_pere = "Employeur du père"
    cnss = "Caisse nationale de sécurité sociale"
    caisse_de_retraite = "Caisse de retraite servant la pension"


# Valeurs de la table ci-dessous.
#
# Bénéficiaire : N non servie, P père, M mère, T tuteur, A mère pour le montant antérieur au
# second mariage, G père ou mère selon la garde de l'enfant (garde partagée, cas servis aux
# deux parents « en fonction du nombre des enfants dont la garde est assurée »), H mère selon
# la garde, le père n'étant pas servi (cas 73, 75, 76, 78).
# Organisme payeur : None si l'annexe ne le nomme pas, E employeur du père, C CNSS, R caisse
# de retraite.
_S = SituationParents
_F = FiliationEnfant
_P = StatutParent

_NOMS_BENEFICIAIRES = {
    "N": "non_servie",
    "P": "pere",
    "M": "mere",
    "T": "tuteur",
    "A": "mere_montant_anterieur_remariage",
}
_NOMS_PAYEURS = {
    None: "non_precise",
    "E": "employeur_du_pere",
    "C": "cnss",
    "R": "caisse_de_retraite",
}

# (code, cas, situation, père, mère, filiation, tuteur, (IF, payeur), (SU, payeur))
# Cas 34, 42 et 43 : lus dans l'édition arabe (voir la docstring du module). Une position de
# parent à None vaut « quelle qu'elle soit » (mère décédée des cas 42 et 43).
_I = "parents_en_vie_non_divorces"
_II = "pere_decede"
_III = "mere_decedee"
_IV = "divorce_garde_pere"
_V = "divorce_garde_mere"
_VI = "divorce_garde_partagee"
_VII = "tutelle"
_c, _p, _m = "communs", "premier_mariage_pere", "premier_mariage_mere"
_ap = "agent_public"
_lib = "activite_liberale"
_sal = "salarie"
_salif = "salarie_beneficiaire_indemnites_familiales"
_salnif = "salarie_non_beneficiaire_indemnites_familiales"
_sans = "sans_activite"
_ret = "retraite"
_retok = "retraite_regime_ouvrant_droit"
_retko = "retraite_regime_sans_droit"
_rev_if = "agent_public_reversion_et_indemnites_familiales"
_rev = "agent_public_reversion_sans_indemnites_familiales"
_norev = "agent_public_sans_reversion_ni_indemnites_familiales"
_pere_sans_rev = "agent_public_sans_reversion"
_pere_avec_rev = "agent_public_avec_reversion"
_N = ("N", None)
_tut = {
    "celibataire": "celibataire",
    "sans": "marie_conjoint_sans_activite",
    "revenu": "marie_conjoint_avec_revenu",
}

CAS_ANNEXE_2 = [
    # I. Père et mère en vie, non divorcés (JORT n° 94, p. 2353-2355)
    (1, "I-A", _I, _ap, _ap, _c, None, ("P", None), _N),
    (2, "I-A", _I, _ap, _ap, _p, None, ("P", None), _N),
    (3, "I-A", _I, _ap, _ap, _m, None, ("A", None), _N),
    (4, "I-B", _I, _ap, _lib, _c, None, ("P", None), _N),
    (5, "I-B", _I, _ap, _lib, _p, None, ("P", None), _N),
    (6, "I-B", _I, _ap, _lib, _m, None, _N, _N),
    (7, "I-C", _I, _ap, _sal, _c, None, ("P", None), _N),
    (8, "I-C", _I, _ap, _sal, _p, None, ("P", None), _N),
    (9, "I-C", _I, _ap, _sal, _m, None, _N, _N),
    (10, "I-D", _I, _ap, _sans, _c, None, ("P", None), ("P", None)),
    (11, "I-D", _I, _ap, _sans, _p, None, ("P", None), ("P", None)),
    (12, "I-D", _I, _ap, _sans, _m, None, _N, _N),
    (13, "I-E", _I, _ap, _ret, _c, None, ("P", None), _N),
    (14, "I-E", _I, _ap, _ret, _p, None, ("P", None), _N),
    (15, "I-E", _I, _ap, _ret, _m, None, _N, _N),
    (16, "I-F", _I, _lib, _ap, _c, None, ("M", None), _N),
    (17, "I-F", _I, _lib, _ap, _p, None, _N, _N),
    (18, "I-F", _I, _lib, _ap, _m, None, ("A", None), _N),
    (19, "I-G", _I, _salif, _ap, _c, None, _N, _N),
    (20, "I-G", _I, _salif, _ap, _p, None, ("P", "C"), _N),
    (21, "I-G", _I, _salif, _ap, _m, None, ("A", None), _N),
    (22, "I-H", _I, _salnif, _ap, _c, None, ("M", None), _N),
    (23, "I-H", _I, _salnif, _ap, _p, None, _N, _N),
    (24, "I-H", _I, _salnif, _ap, _m, None, ("A", None), _N),
    (25, "I-I", _I, _sans, _ap, _c, None, ("M", None), ("M", None)),
    (26, "I-I", _I, _sans, _ap, _p, None, _N, _N),
    (27, "I-I", _I, _sans, _ap, _m, None, ("A", None), ("A", None)),
    (28, "I-J", _I, _retok, _ap, _c, None, _N, _N),
    (29, "I-J", _I, _retok, _ap, _p, None, ("P", "R"), _N),
    (30, "I-J", _I, _retok, _ap, _m, None, ("A", None), _N),
    (31, "I-K", _I, _retko, _ap, _c, None, ("M", None), _N),
    (32, "I-K", _I, _retko, _ap, _p, None, _N, _N),
    (33, "I-K", _I, _retko, _ap, _m, None, ("A", None), _N),
    # II. Père décédé, mère non remariée (p. 2355-2356)
    # Cas 34 : bénéficiaire non nommé, déduit : la mère (édition arabe, p. 2540).
    (34, "II-A", _II, _ap, _rev_if, _c, None, ("M", "R"), _N),
    (35, "II-B", _II, _lib, _ap, _c, None, ("M", None), ("M", None)),
    (36, "II-C", _II, _sal, _rev_if, _c, None, ("M", "C"), _N),
    (37, "II-D", _II, _sal, _rev, _c, None, ("M", None), _N),
    (38, "II-E", _II, _sal, _norev, _c, None, ("M", None), ("M", None)),
    (39, "II-F", _II, _sans, _ap, _c, None, ("M", None), ("M", None)),
    (40, "II-G", _II, _ret, _rev_if, _c, None, ("M", "R"), _N),
    (41, "II-H", _II, _ret, _rev, _c, None, ("M", None), _N),
    # III. Mère décédée, père non remarié (p. 2356)
    (42, "III-A", _III, _pere_sans_rev, None, _c, None, ("P", None), ("P", None)),
    (43, "III-B", _III, _pere_avec_rev, None, _c, None, ("P", None), _N),
    (44, "III-C", _III, _lib, _ap, _c, None, _N, _N),
    (45, "III-D", _III, _sal, _ap, _c, None, _N, _N),
    (46, "III-E", _III, _sans, _ap, _c, None, _N, _N),
    (47, "III-F", _III, _ret, _ap, _c, None, _N, _N),
    # IV. Divorce, le père assure la garde (p. 2357)
    (48, "IV-A", _IV, _ap, _ap, _c, None, ("P", None), ("P", None)),
    (49, "IV-B", _IV, _ap, _lib, _c, None, ("P", None), ("P", None)),
    (50, "IV-C", _IV, _ap, _sal, _c, None, ("P", None), ("P", None)),
    (51, "IV-D", _IV, _ap, _sans, _c, None, ("P", None), ("P", None)),
    (52, "IV-E", _IV, _ap, _ret, _c, None, ("P", None), ("P", None)),
    (53, "IV-F", _IV, _lib, _ap, _c, None, _N, _N),
    (54, "IV-G", _IV, _sal, _ap, _c, None, _N, _N),
    (55, "IV-H", _IV, _sans, _ap, _c, None, _N, _N),
    (56, "IV-I", _IV, _ret, _ap, _c, None, ("P", "R"), ("P", "R")),
    # V. Divorce, la mère assure la garde (p. 2358-2359)
    (57, "V-A", _V, _ap, _ap, _c, None, ("M", "E"), ("M", "E")),
    (58, "V-B", _V, _ap, _lib, _c, None, ("M", "E"), ("M", "E")),
    (59, "V-C", _V, _ap, _sal, _c, None, ("M", "E"), ("M", "E")),
    (60, "V-D", _V, _ap, _sans, _c, None, ("M", "E"), ("M", "E")),
    (61, "V-E", _V, _ap, _ret, _c, None, ("M", "E"), ("M", "E")),
    (62, "V-F", _V, _lib, _ap, _c, None, ("M", None), ("M", None)),
    (63, "V-G", _V, _salif, _ap, _c, None, ("M", "C"), ("M", "C")),
    (64, "V-H", _V, _salnif, _ap, _c, None, ("M", None), ("M", None)),
    (65, "V-I", _V, _sans, _ap, _c, None, ("M", None), ("M", None)),
    (66, "V-J", _V, _retok, _ap, _c, None, ("M", "R"), ("M", "R")),
    (67, "V-K", _V, _retko, _ap, _c, None, ("M", None), ("M", None)),
    # VI. Divorce, garde partagée (p. 2360-2361)
    (68, "VI-A", _VI, _ap, _ap, _c, None, ("G", "E"), ("G", "E")),
    (69, "VI-B", _VI, _ap, _lib, _c, None, ("G", "E"), ("G", "E")),
    (70, "VI-C", _VI, _ap, _sal, _c, None, ("G", "E"), ("G", "E")),
    (71, "VI-D", _VI, _ap, _sans, _c, None, ("G", "E"), ("G", "E")),
    (72, "VI-E", _VI, _ap, _ret, _c, None, ("G", "E"), ("G", "E")),
    (73, "VI-F", _VI, _lib, _ap, _c, None, ("H", None), ("H", None)),
    (74, "VI-G", _VI, _salif, _ap, _c, None, ("G", "C"), ("G", "C")),
    (75, "VI-H", _VI, _salnif, _ap, _c, None, ("H", None), ("H", None)),
    (76, "VI-I", _VI, _sans, _ap, _c, None, ("H", None), ("H", None)),
    (77, "VI-J", _VI, _retok, _ap, _c, None, ("G", "R"), ("G", "R")),
    (78, "VI-K", _VI, _retko, _ap, _c, None, ("H", None), ("H", None)),
    # VII. Tuteur ou tutrice (p. 2362)
    (79, "VII-A", _VII, None, None, None, "celibataire", ("T", None), ("T", None)),
    (80, "VII-B", _VII, None, None, None, "marie_conjoint_sans_activite", ("T", None), ("T", None)),  # noqa: E501
    (81, "VII-C", _VII, None, None, None, "marie_conjoint_avec_revenu", ("T", None), _N),
]


class pf_situation_parents(Variable):
    value_type = Enum
    possible_values = SituationParents
    default_value = SituationParents.parents_en_vie_non_divorces
    entity = Individu
    label = "Situation des parents de l'enfant, au sens de l'annexe 2 de la circulaire n° 42 de 1996"  # noqa: E501
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2 (JORT n° 94 du
    22 novembre 1996, p. 2353-2362) : les sept intitulés I à VII. Entrée portée par l'enfant,
    parce que ses parents peuvent ne plus appartenir à son ménage.
    """


class pf_filiation(Variable):
    value_type = Enum
    possible_values = FiliationEnfant
    default_value = FiliationEnfant.communs
    entity = Individu
    label = "Filiation de l'enfant : commun, ou d'un premier mariage de l'un des parents, à sa charge"  # noqa: E501
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Enfants » (JORT n° 94, p. 2353-2355). Hors de
    la situation I, l'annexe ne vise que les enfants communs.
    """


class pf_statut_pere(Variable):
    value_type = Enum
    possible_values = StatutParent
    default_value = StatutParent.non_renseigne
    entity = Individu
    label = "Position du père de l'enfant, au sens de l'annexe 2 de la circulaire n° 42 de 1996"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Père » (JORT n° 94, p. 2353-2361). Pour un père
    décédé, sa position de son vivant.
    """


class pf_statut_mere(Variable):
    value_type = Enum
    possible_values = StatutParent
    default_value = StatutParent.non_renseigne
    entity = Individu
    label = "Position de la mère de l'enfant, au sens de l'annexe 2 de la circulaire n° 42 de 1996"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Mère » (JORT n° 94, p. 2353-2361). Pour une
    mère décédée, sa position de son vivant.
    """


class pf_statut_tuteur(Variable):
    value_type = Enum
    possible_values = StatutTuteur
    default_value = StatutTuteur.non_renseigne
    entity = Individu
    label = "Situation du tuteur ou de la tutrice de l'enfant, au sens de l'annexe 2 (VII)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, VII (JORT n° 94, p. 2362). Utilisée seulement avec la
    situation `tutelle`.
    """


class pf_garde_enfant(Variable):
    value_type = Enum
    possible_values = GardeEnfant
    default_value = GardeEnfant.non_renseigne
    entity = Individu
    label = "Parent qui assure la garde de l'enfant, en cas de garde partagée"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, VI (JORT n° 94, p. 2360-2361) : l'indemnité est servie
    au père et à la mère « en fonction du nombre des enfants dont la garde est assurée ». La
    garde se saisit donc enfant par enfant. Utilisée avec la situation `divorce_garde_partagee`,
    pour le secteur public et pour le secteur privé (loi n° 60-30, article 64 : les allocations
    sont versées à la personne qui a la garde de l'enfant). Dans les situations `divorce_garde_pere`
    et `divorce_garde_mere` la garde est dite par la situation ; dans un couple non séparé elle
    n'est pas saisie : le texte ne dit pas ce qu'elle y veut dire.
    """


class pf_cas_circulaire_42(Variable):
    value_type = int
    default_value = 0
    entity = Individu
    label = "Code (1 à 81) du cas de l'annexe 2 de la circulaire n° 42 de 1996 qui s'applique à l'enfant, 0 si aucun"  # noqa: E501
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE
    documentation = __doc__

    def formula(individu, period):
        """Circulaire n° 42 du 25 octobre 1996, annexe 2 (JORT n° 94 du 22 novembre 1996,
        p. 2353-2362) : la table `CAS_ANNEXE_2` transcrit les quatre-vingt-un cas."""
        situation = individu("pf_situation_parents", period)
        pere = individu("pf_statut_pere", period)
        mere = individu("pf_statut_mere", period)
        filiation = individu("pf_filiation", period)
        tuteur = individu("pf_statut_tuteur", period)
        code = zeros(individu.count, dtype=int)
        for numero, _cas, sit, st_pere, st_mere, fil, st_tuteur, _si, _su in CAS_ANNEXE_2:
            masque = situation == _S[sit]
            if st_tuteur is None:
                masque = masque * (filiation == _F[fil])
                if st_pere is not None:
                    masque = masque * (pere == _P[st_pere])
                if st_mere is not None:
                    masque = masque * (mere == _P[st_mere])
            else:
                masque = masque * (tuteur == StatutTuteur[st_tuteur])
            code = where(masque, numero, code)
        return code


def _est_salarie(statut):
    S = StatutParent
    return (
        (statut == S.salarie)
        + (statut == S.salarie_beneficiaire_indemnites_familiales)
        + (statut == S.salarie_non_beneficiaire_indemnites_familiales)
    )


def _ouvre_droit(statut):
    """Salarié qui ouvre droit aux allocations familiales du secteur privé.

    `salarie` (« sans distinction de droit ») est compté : l'entrée ne dit pas le contraire.
    `salarie_non_beneficiaire_indemnites_familiales` ne l'est pas, par définition."""
    S = StatutParent
    return (statut == S.salarie) + (statut == S.salarie_beneficiaire_indemnites_familiales)


def _est_agent_public(statut):
    S = StatutParent
    return (
        (statut == S.agent_public)
        + (statut == S.agent_public_reversion_et_indemnites_familiales)
        + (statut == S.agent_public_reversion_sans_indemnites_familiales)
        + (statut == S.agent_public_sans_reversion_ni_indemnites_familiales)
        + (statut == S.agent_public_sans_reversion)
        + (statut == S.agent_public_avec_reversion)
    )


def _est_secteur_prive(individu, period):
    """Aucun cas de l'annexe 2 ne s'applique, un parent au moins est salarié, aucun n'est agent public."""
    code = individu("pf_cas_circulaire_42", period)
    pere = individu("pf_statut_pere", period)
    mere = individu("pf_statut_mere", period)
    return (
        (code == 0)
        * (_est_salarie(pere) + _est_salarie(mere))
        * (1 - _est_agent_public(pere))
        * (1 - _est_agent_public(mere))
    )


def _garde(individu, period):
    """Parent qui a la garde : (père, mère), deux indicatrices.

    Les situations IV et V disent la garde ; la situation VI la renvoie à `pf_garde_enfant`.
    Dans toute autre situation (couple non séparé, décès, tutelle), la garde n'est pas établie
    et aucun des deux n'est retenu."""
    situation = individu("pf_situation_parents", period)
    garde = individu("pf_garde_enfant", period)
    partagee = situation == SituationParents.divorce_garde_partagee
    pere = (situation == SituationParents.divorce_garde_pere) + partagee * (
        garde == GardeEnfant.pere
    )
    mere = (situation == SituationParents.divorce_garde_mere) + partagee * (
        garde == GardeEnfant.mere
    )
    return pere, mere


def _indices_allocataire_public(individu, period):
    """Applique à chaque enfant l'allocataire de la colonne « indemnité familiale » de la table."""
    code = individu("pf_cas_circulaire_42", period)
    garde = individu("pf_garde_enfant", period)
    G = GardeEnfant
    indices = zeros(individu.count, dtype=int) + Allocataire.non_designe.index
    for ligne in CAS_ANNEXE_2:
        beneficiaire = ligne[7][0]
        if beneficiaire == "G":
            valeur = where(
                garde == G.pere,
                Allocataire.pere.index,
                where(garde == G.mere, Allocataire.mere.index, Allocataire.non_designe.index),
            )
        elif beneficiaire == "H":
            valeur = where(
                garde == G.mere,
                Allocataire.mere.index,
                where(garde == G.pere, Allocataire.non_servie.index, Allocataire.non_designe.index),
            )
        else:
            valeur = Allocataire[_NOMS_BENEFICIAIRES[beneficiaire]].index
        indices = where(code == ligne[0], valeur, indices)
    return indices


def _indices_allocataire(individu, period, avant_1996):
    """Table de la circulaire pour le secteur public, loi n° 60-30 pour le secteur privé.

    Secteur privé, seuls cas retenus (tout autre renvoie `non_designe`) :

    - couple non séparé, père et mère ouvrant droit, avant le 4 août 1996 : article 55, alinéa 3,
      allocation du père, la mère pouvant réclamer la différence ;
    - parents séparés, garde connue, un seul des deux parents ouvrant droit : l'allocation est
      versée à la personne qui a la garde (article 64 ; article 53, dernier alinéa pour la
      personne qui n'a pas d'activité propre), avant comme après 1996.

    Non codé, faute de texte qui tranche (points du précis, section « Qui perçoit
    l'allocation ») :
    TODO (1) ce que « garde » veut dire quand les parents vivent ensemble : couple non séparé
    depuis le 4 août 1996, ou un seul parent ouvrant droit ;
    TODO (2) avant 1996, parents séparés ouvrant droit tous deux : article 55, alinéa 3 (allocation
    du père) face à l'article 64 (versement à la garde) ;
    TODO (4) depuis 1996, parents séparés ouvrant droit tous deux : « l'allocation la plus élevée »
    si les montants diffèrent ; les parents n'étant pas dans le ménage de l'enfant, leurs
    montants ne sont pas calculables, et la rémunération et le sexe ne relient pas
    `personne_de_reference` et `conjoint` au père et à la mère ;
    TODO (6) tutelle : tuteur officieux salarié, article 53 3° ;
    décès d'un parent (articles 56 à 59) : non codé.
    """
    indices = _indices_allocataire_public(individu, period)
    prive = _est_secteur_prive(individu, period)
    pere_droit = _ouvre_droit(individu("pf_statut_pere", period))
    mere_droit = _ouvre_droit(individu("pf_statut_mere", period))
    couple = individu("pf_situation_parents", period) == SituationParents.parents_en_vie_non_divorces
    garde_pere, garde_mere = _garde(individu, period)
    un_seul_droit = pere_droit != mere_droit
    valeur = zeros(individu.count, dtype=int) + Allocataire.non_designe.index
    if avant_1996:
        valeur = where(
            couple * pere_droit * mere_droit,
            Allocataire.pere_mere_pouvant_reclamer_difference.index,
            valeur,
        )
    valeur = where(garde_pere * un_seul_droit, Allocataire.pere.index, valeur)
    valeur = where(garde_mere * un_seul_droit, Allocataire.mere.index, valeur)
    return where(prive, valeur, indices)


class pf_allocataire(Variable):
    value_type = Enum
    possible_values = Allocataire
    default_value = Allocataire.non_designe
    entity = Individu
    label = "À qui sont servies les prestations familiales (indemnité familiale, allocations familiales), au titre de l'enfant"  # noqa: E501
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Avant le 1er avril 1961 : la table de la circulaire seulement (secteur public)."""
        return EnumArray(_indices_allocataire_public(individu, period), Allocataire)

    def formula_1961_04_01(individu, period):
        """Secteur public : circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2,
        colonne « Indemnité familiale » (JORT n° 94 du 22 novembre 1996, p. 2353-2362), qui
        applique le décret du 22 novembre 1918 ; voir `pf_cas_circulaire_42` pour le cas retenu.

        Secteur privé, loi n° 60-30, dans sa rédaction d'origine (en vigueur le 1er avril 1961,
        article 130) : l'article 53 énumère les personnes du chef desquelles les allocations
        sont dues ; l'article 55, alinéa 3, ne sert, quand le père et la mère ouvrent tous deux
        droit, que l'allocation du père, la mère pouvant réclamer la différence
        (`pere_mere_pouvant_reclamer_difference`) ; l'article 64 verse les allocations à la
        personne qui a la garde. Voir `_indices_allocataire` pour les cas retenus et les cas
        non codés."""
        return EnumArray(_indices_allocataire(individu, period, avant_1996=True), Allocataire)

    def formula_1996_08_04(individu, period):
        """Secteur public : comme avant. Secteur privé : loi n° 96-65, exécutoire le 4 août 1996,
        article 55, alinéa 3 nouveau : l'allocation est servie à la personne ayant la garde et,
        si les montants dus du chef de deux personnes diffèrent, l'allocation la plus élevée.
        Dans un couple non séparé, la loi ne dit pas ce que « garde » veut dire et les montants
        par personne ne sont pas rattachables au père et à la mère : `non_designe`. Seul est codé
        le versement à la garde (article 64) quand un seul parent ouvre droit."""
        return EnumArray(_indices_allocataire(individu, period, avant_1996=False), Allocataire)


class pf_salaire_unique_servi(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "L'indemnité pour salaire unique est servie à l'allocataire de l'enfant (secteur public)"  # noqa: E501
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Circulaire n° 42 de 1996, annexe 2, colonne « Indemnité pour salaire unique » (JORT
        n° 94, p. 2353-2362), qui applique le décret du 24 février 1944. Quand elle est servie,
        elle l'est à l'allocataire de l'indemnité familiale, par le même organisme (vérifié sur
        les 81 cas par `tests/test_indemnites_familiales_public.py`). Dans le secteur privé, la
        majoration pour salaire unique (loi n° 80-36, art. 65 bis) se calcule au niveau du
        ménage (`majoration_salaire_unique`)."""
        code = individu("pf_cas_circulaire_42", period)
        allocataire = individu("pf_allocataire", period)
        servie = zeros(individu.count, dtype=bool)
        for ligne in CAS_ANNEXE_2:
            if ligne[8][0] != "N":
                servie = servie + (code == ligne[0])
        personne_servie = (allocataire != Allocataire.non_servie) * (
            allocataire != Allocataire.non_designe
        )
        return servie * personne_servie


class pf_majoration_salaire_unique_allocataire(Variable):
    value_type = Enum
    possible_values = Allocataire
    default_value = Allocataire.non_designe
    entity = Individu
    label = "À qui est versée la majoration pour salaire unique du secteur privé, au titre de l'enfant"  # noqa: E501
    definition_period = MONTH
    reference = "https://www.pist.tn/jort/1981/1981F/Jo03881.pdf"

    def formula_1980_05_01(individu, period):
        """Loi n° 80-36 du 28 mai 1980, article 65 bis, en vigueur le 1er mai 1980 : la
        majoration est « versée à la personne qui a la garde des enfants ». Secteur privé seulement,
        un parent au moins ouvrant droit aux allocations ; la garde est connue pour les parents
        séparés (`pf_situation_parents`, `pf_garde_enfant`), sinon `non_designe`. Avant le
        1er mai 1980 la majoration n'existe pas (valeur par défaut, `non_designe`).

        Non codé : le maintien aux titulaires de pensions (décret n° 81-731, JORT n° 38 de 1981,
        p. 1334-1335, effet au 1er mai 1981), faute d'une entrée distinguant les pensions du
        régime des salariés ; le montant, au niveau du ménage (`majoration_salaire_unique`)."""
        prive = _est_secteur_prive(individu, period)
        ouvre_droit = _ouvre_droit(individu("pf_statut_pere", period)) + _ouvre_droit(
            individu("pf_statut_mere", period)
        )
        garde_pere, garde_mere = _garde(individu, period)
        indices = zeros(individu.count, dtype=int) + Allocataire.non_designe.index
        indices = where(prive * ouvre_droit * garde_pere, Allocataire.pere.index, indices)
        indices = where(prive * ouvre_droit * garde_mere, Allocataire.mere.index, indices)
        return EnumArray(indices, Allocataire)


class pf_payeur(Variable):
    value_type = Enum
    possible_values = Payeur
    default_value = Payeur.non_precise
    entity = Individu
    label = "Organisme qui sert les prestations familiales de l'enfant, lorsque le texte le nomme"
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Avant le 1er avril 1961 : la table de la circulaire seulement."""
        return EnumArray(_indices_payeur_public(individu, period), Payeur)

    def formula_1961_04_01(individu, period):
        """Secteur public : circulaire n° 42 de 1996, annexe 2 : « par l'employeur du père »,
        « par la CNSS », « par la caisse de retraite » (JORT n° 94, p. 2353-2362).

        Secteur privé : la caisse nationale de sécurité sociale verse les allocations aux ayants
        droit (loi n° 60-30, article 65, en vigueur le 1er avril 1961).

        Non codé : le dernier employeur, pour les allocations maintenues (articles 56 à 59)
        quand il est dispensé d'affiliation ou ne s'est pas affilié (article 60), et le paiement
        direct par les employeurs affiliés (article 48, 2°) ; le modèle n'a pas de variable
        d'affiliation de l'employeur à la caisse. La caisse est retenue par défaut."""
        indices = _indices_payeur_public(individu, period)
        indices = where(_est_secteur_prive(individu, period), Payeur.cnss.index, indices)
        return EnumArray(indices, Payeur)


def _indices_payeur_public(individu, period):
    code = individu("pf_cas_circulaire_42", period)
    indices = zeros(individu.count, dtype=int)
    for ligne in CAS_ANNEXE_2:
        nom = _NOMS_PAYEURS[ligne[7][1]]
        indices = where(code == ligne[0], Payeur[nom].index, indices)
    return indices

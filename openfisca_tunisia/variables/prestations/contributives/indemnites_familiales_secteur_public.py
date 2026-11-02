"""Indemnité familiale et indemnité pour salaire unique du secteur public : qui est servi.

Source : circulaire du Premier ministre n° 42 du 25 octobre 1996, « la gestion des indemnités
à caractère familial dans le secteur public », JORT n° 89 du 5 novembre 1996 (p. 2349-2352) ;
annexe 2, « Les indemnités familiales au titre des enfants de l'agent public, ou de ses
enfants adoptés, et l'indemnité pour salaire unique », JORT n° 94 du 22 novembre 1996
(p. 2353-2362, traduction française). La circulaire rappelle que le décret du 22 novembre 1918
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

Cas que l'annexe ne tranche pas, laissés sans règle (le résultat est `hors_annexe`) :

- cas 34 (II-A) : l'indemnité est « servie par la caisse de retraite » sans que le
  bénéficiaire soit nommé ;
- cas 42 et 43 (III-A et III-B) : les deux lignes ont la même description du père et de la
  mère et des résultats différents pour l'indemnité pour salaire unique (servie au cas 42,
  non servie au cas 43) ; la description de la mère y manque.

Les combinaisons absentes de l'annexe donnent aussi `hors_annexe` : l'annexe ne dit rien
des parents remariés dans les situations II à VI, ni des enfants d'un premier mariage hors
de la situation I.
"""

from numpy import zeros
from openfisca_core.indexed_enums import EnumArray

from openfisca_tunisia.variables.base import *  # noqa F401


REFERENCE_CIRCULAIRE = "https://www.pist.tn/jort/1996/1996F/Jo09496.pdf"


class SituationParentsSecteurPublic(Enum):
    __order__ = "parents_en_vie_non_divorces pere_decede mere_decedee divorce_garde_pere divorce_garde_mere divorce_garde_partagee tutelle"  # noqa: E501
    parents_en_vie_non_divorces = "Père et mère en vie, non divorcés (I)"
    pere_decede = "Père décédé, mère non remariée (II)"
    mere_decedee = "Mère décédée, père non remarié (III)"
    divorce_garde_pere = "Divorce, le père assure la garde et n'est pas remarié (IV)"
    divorce_garde_mere = "Divorce, la mère assure la garde et n'est pas remariée (V)"
    divorce_garde_partagee = "Divorce, garde assurée conjointement par les parents, non remariés (VI)"  # noqa: E501
    tutelle = "Enfant sous la tutelle d'un tuteur ou d'une tutrice (VII)"


class FiliationEnfantSecteurPublic(Enum):
    __order__ = "communs premier_mariage_pere premier_mariage_mere"
    communs = "Enfant commun du père et de la mère"
    premier_mariage_pere = "Enfant d'un premier mariage du père, à sa charge"
    premier_mariage_mere = "Enfant d'un premier mariage de la mère, à sa charge"


class StatutParentSecteurPublic(Enum):
    """Position d'un parent dans l'annexe 2 (pour un parent décédé, sa position de son vivant)."""

    __order__ = "non_renseigne agent_public activite_liberale salarie salarie_beneficiaire_indemnites_familiales salarie_non_beneficiaire_indemnites_familiales sans_activite retraite retraite_regime_ouvrant_droit retraite_regime_sans_droit agent_public_reversion_et_indemnites_familiales agent_public_reversion_sans_indemnites_familiales agent_public_sans_reversion_ni_indemnites_familiales"  # noqa: E501
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


class StatutTuteurSecteurPublic(Enum):
    __order__ = "non_renseigne celibataire marie_conjoint_sans_activite marie_conjoint_avec_revenu"
    non_renseigne = "Non renseigné"
    celibataire = "Le tuteur (la tutrice) est célibataire"
    marie_conjoint_sans_activite = "Marié(e) à un conjoint n'exerçant pas une activité professionnelle rémunérée"  # noqa: E501
    marie_conjoint_avec_revenu = "Marié(e) à un conjoint disposant d'un revenu professionnel ou d'une pension"  # noqa: E501


class GardeEnfantSecteurPublic(Enum):
    __order__ = "non_renseigne pere mere"
    non_renseigne = "Non renseigné"
    pere = "Garde assurée par le père"
    mere = "Garde assurée par la mère"


class BeneficiaireIndemniteSecteurPublic(Enum):
    __order__ = "hors_annexe non_servie pere mere tuteur mere_montant_anterieur_remariage"
    hors_annexe = "Cas que l'annexe 2 ne prévoit pas ou ne tranche pas"
    non_servie = "Non servie"
    pere = "Servie au père"
    mere = "Servie à la mère"
    tuteur = "Servie au tuteur ou à la tutrice"
    mere_montant_anterieur_remariage = "Servie à la mère, pour le montant dont elle bénéficiait avant le second mariage"  # noqa: E501


class PayeurIndemniteSecteurPublic(Enum):
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
_S = SituationParentsSecteurPublic
_F = FiliationEnfantSecteurPublic
_P = StatutParentSecteurPublic

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
# Les cas 34, 42 et 43, ambigus, n'y figurent pas (voir la docstring du module).
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
    # II. Père décédé, mère non remariée (p. 2355-2356) ; le cas 34 est ambigu
    (35, "II-B", _II, _lib, _ap, _c, None, ("M", None), ("M", None)),
    (36, "II-C", _II, _sal, _rev_if, _c, None, ("M", "C"), _N),
    (37, "II-D", _II, _sal, _rev, _c, None, ("M", None), _N),
    (38, "II-E", _II, _sal, _norev, _c, None, ("M", None), ("M", None)),
    (39, "II-F", _II, _sans, _ap, _c, None, ("M", None), ("M", None)),
    (40, "II-G", _II, _ret, _rev_if, _c, None, ("M", "R"), _N),
    (41, "II-H", _II, _ret, _rev, _c, None, ("M", None), _N),
    # III. Mère décédée, père non remarié (p. 2356) ; les cas 42 et 43 sont ambigus
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


class pf_public_situation_parents(Variable):
    value_type = Enum
    possible_values = SituationParentsSecteurPublic
    default_value = SituationParentsSecteurPublic.parents_en_vie_non_divorces
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


class pf_public_filiation(Variable):
    value_type = Enum
    possible_values = FiliationEnfantSecteurPublic
    default_value = FiliationEnfantSecteurPublic.communs
    entity = Individu
    label = "Filiation de l'enfant : commun, ou d'un premier mariage de l'un des parents, à sa charge"  # noqa: E501
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Enfants » (JORT n° 94, p. 2353-2355). Hors de
    la situation I, l'annexe ne vise que les enfants communs.
    """


class pf_public_statut_pere(Variable):
    value_type = Enum
    possible_values = StatutParentSecteurPublic
    default_value = StatutParentSecteurPublic.non_renseigne
    entity = Individu
    label = "Position du père de l'enfant, au sens de l'annexe 2 de la circulaire n° 42 de 1996"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Père » (JORT n° 94, p. 2353-2361). Pour un père
    décédé, sa position de son vivant.
    """


class pf_public_statut_mere(Variable):
    value_type = Enum
    possible_values = StatutParentSecteurPublic
    default_value = StatutParentSecteurPublic.non_renseigne
    entity = Individu
    label = "Position de la mère de l'enfant, au sens de l'annexe 2 de la circulaire n° 42 de 1996"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, colonne « Mère » (JORT n° 94, p. 2353-2361). Pour une
    mère décédée, sa position de son vivant.
    """


class pf_public_statut_tuteur(Variable):
    value_type = Enum
    possible_values = StatutTuteurSecteurPublic
    default_value = StatutTuteurSecteurPublic.non_renseigne
    entity = Individu
    label = "Situation du tuteur ou de la tutrice de l'enfant, au sens de l'annexe 2 (VII)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, VII (JORT n° 94, p. 2362). Utilisée seulement avec la
    situation `tutelle`.
    """


class pf_public_garde_enfant(Variable):
    value_type = Enum
    possible_values = GardeEnfantSecteurPublic
    default_value = GardeEnfantSecteurPublic.non_renseigne
    entity = Individu
    label = "Parent qui assure la garde de l'enfant, en cas de garde partagée"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = REFERENCE_CIRCULAIRE
    documentation = """
    Circulaire n° 42 de 1996, annexe 2, VI (JORT n° 94, p. 2360-2361) : l'indemnité est servie
    au père et à la mère « en fonction du nombre des enfants dont la garde est assurée ». La
    garde se saisit donc enfant par enfant. Utilisée seulement avec la situation
    `divorce_garde_partagee`.
    """


class pf_public_cas_annexe_2(Variable):
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
        situation = individu("pf_public_situation_parents", period)
        pere = individu("pf_public_statut_pere", period)
        mere = individu("pf_public_statut_mere", period)
        filiation = individu("pf_public_filiation", period)
        tuteur = individu("pf_public_statut_tuteur", period)
        code = zeros(individu.count, dtype=int)
        for numero, _cas, sit, st_pere, st_mere, fil, st_tuteur, _si, _su in CAS_ANNEXE_2:
            masque = situation == _S[sit]
            if st_tuteur is None:
                masque = (
                    masque
                    * (pere == _P[st_pere])
                    * (mere == _P[st_mere])
                    * (filiation == _F[fil])
                )
            else:
                masque = masque * (tuteur == StatutTuteurSecteurPublic[st_tuteur])
            code = where(masque, numero, code)
        return code


def _resultat(individu, period, position, enum, noms):
    """Applique à chaque enfant le bénéficiaire de la colonne `position` de la table (7 pour
    l'indemnité familiale, 8 pour l'indemnité pour salaire unique)."""
    code = individu("pf_public_cas_annexe_2", period)
    garde = individu("pf_public_garde_enfant", period)
    G = GardeEnfantSecteurPublic
    indices = zeros(individu.count, dtype=int)
    for ligne in CAS_ANNEXE_2:
        beneficiaire, payeur = ligne[position]
        masque = code == ligne[0]
        if beneficiaire == "G":
            valeur = where(
                garde == G.pere,
                enum.pere.index,
                where(garde == G.mere, enum.mere.index, enum.hors_annexe.index),
            )
        elif beneficiaire == "H":
            valeur = where(
                garde == G.mere,
                enum.mere.index,
                where(garde == G.pere, enum.non_servie.index, enum.hors_annexe.index),
            )
        else:
            valeur = enum[noms[beneficiaire]].index
        indices = where(masque, valeur, indices)
    return indices


def _beneficiaire(individu, period, position):
    indices = _resultat(
        individu, period, position, BeneficiaireIndemniteSecteurPublic, _NOMS_BENEFICIAIRES
    )
    return EnumArray(indices, BeneficiaireIndemniteSecteurPublic)


def _payeur(individu, period, position):
    code = individu("pf_public_cas_annexe_2", period)
    indices = zeros(individu.count, dtype=int)
    for ligne in CAS_ANNEXE_2:
        nom = _NOMS_PAYEURS[ligne[position][1]]
        indices = where(code == ligne[0], PayeurIndemniteSecteurPublic[nom].index, indices)
    return EnumArray(indices, PayeurIndemniteSecteurPublic)


_POSITION_INDEMNITE_FAMILIALE = 7
_POSITION_SALAIRE_UNIQUE = 8


class indemnite_familiale_public_beneficiaire(Variable):
    value_type = Enum
    possible_values = BeneficiaireIndemniteSecteurPublic
    default_value = BeneficiaireIndemniteSecteurPublic.hors_annexe
    entity = Individu
    label = "À qui l'indemnité familiale du secteur public est servie, au titre de l'enfant"
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2, colonne
        « Indemnité familiale » (JORT n° 94 du 22 novembre 1996, p. 2353-2362), qui applique le
        décret du 22 novembre 1918 : voir `pf_public_cas_annexe_2` pour le cas retenu."""
        return _beneficiaire(individu, period, _POSITION_INDEMNITE_FAMILIALE)


class indemnite_familiale_public_payeur(Variable):
    value_type = Enum
    possible_values = PayeurIndemniteSecteurPublic
    default_value = PayeurIndemniteSecteurPublic.non_precise
    entity = Individu
    label = "Organisme qui sert l'indemnité familiale du secteur public, lorsque l'annexe le nomme"
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Circulaire n° 42 de 1996, annexe 2, colonne « Indemnité familiale » : « par l'employeur
        du père », « par la CNSS », « par la caisse de retraite » (JORT n° 94, p. 2353-2362)."""
        return _payeur(individu, period, _POSITION_INDEMNITE_FAMILIALE)


class indemnite_salaire_unique_public_beneficiaire(Variable):
    value_type = Enum
    possible_values = BeneficiaireIndemniteSecteurPublic
    default_value = BeneficiaireIndemniteSecteurPublic.hors_annexe
    entity = Individu
    label = "À qui l'indemnité pour salaire unique du secteur public est servie, au titre de l'enfant"  # noqa: E501
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2, colonne
        « Indemnité pour salaire unique » (JORT n° 94 du 22 novembre 1996, p. 2353-2362), qui
        applique le décret du 24 février 1944."""
        return _beneficiaire(individu, period, _POSITION_SALAIRE_UNIQUE)


class indemnite_salaire_unique_public_payeur(Variable):
    value_type = Enum
    possible_values = PayeurIndemniteSecteurPublic
    default_value = PayeurIndemniteSecteurPublic.non_precise
    entity = Individu
    label = "Organisme qui sert l'indemnité pour salaire unique du secteur public, lorsque l'annexe le nomme"  # noqa: E501
    definition_period = MONTH
    reference = REFERENCE_CIRCULAIRE

    def formula(individu, period):
        """Circulaire n° 42 de 1996, annexe 2, colonne « Indemnité pour salaire unique »
        (JORT n° 94, p. 2353-2362)."""
        return _payeur(individu, period, _POSITION_SALAIRE_UNIQUE)

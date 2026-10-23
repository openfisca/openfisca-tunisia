"""Tarifs des structures sanitaires publiques : malades payants et tarifs réduits.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : arrêtés
des ministres des finances et de la santé publique du 25 janvier 1993 et du 19 décembre 1996,
modifié les 17 avril 1998, 29 janvier 2003 et 7 juillet 2008 ; décrets n° 93-529, 94-1738 et
98-409. Sont éprouvés, feuille par feuille :

- la valeur la veille et le jour de chaque date d'effet, clôtures comprises ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- la note des séries dont les états antérieurs ne sont pas versés ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du sous-arbre, que le système des pensions ne charge pas.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Standard Library
import datetime

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

TARIFS = TunisiaTaxBenefitSystem().parameters.sante.tarifs_hospitaliers

# (fascicule cité dans la note, chemin du fascicule sur pist.tn, date d'effet)
A93 = ("JORT n° 10 du 5 février 1993", "/1993/1993F/Jo01093.pdf", "1993-02-07")
D93 = ("JORT n° 19 du 9 mars 1993", "/1993/1993F/Jo01993.pdf", "1993-01-01")
D94 = ("JORT n° 68 du 30 août 1994", "/1994/1994F/Jo06894.pdf", "1994-09-06")
A96 = ("JORT n° 104 du 27 décembre 1996", "/1996/1996F/Jo10496.pdf", "1997-01-04")
D98 = ("JORT n° 17 du 27 février 1998", "/1998/1998F/Jo01798.pdf", "1998-03-08")
A98 = ("JORT n° 33 du 24 avril 1998", "/1998/1998F/Jo03398.pdf", "1998-05-04")
A03 = ("JORT n° 10 du 4 février 2003", "/2003/2003F/Jo0102003.pdf", "2003-02-10")
A08 = ("JORT n° 56 du 11 juillet 2008", "/2008/2008F/Jo0562008.pdf", "2008-07-17")

MP = "malades_payants"
CONS = f"{MP}.consultation"
HOSP = f"{MP}.hospitalisation"
LC = f"{MP}.lettres_cles"
FORF = f"{MP}.forfaits_actes"
TR = "tarifs_reduits"

# Chemin sous tarifs_hospitaliers : unité, et suite des (texte, valeur). None : clôture.
SERIES = {
    # Consultations des malades payants (article 2).
    f"{CONS}.medecine_generale": ("currency", [(A93, 5), (A96, 7)]),
    f"{CONS}.medecine_dentaire": ("currency", [(A93, 5), (A96, 7)]),
    f"{CONS}.specialite_professeurs_agreges": ("currency", [(A93, 12), (A96, 14)]),
    f"{CONS}.specialite_autres_specialistes": ("currency", [(A93, 8), (A96, 10)]),
    f"{CONS}.majoration_choix_medecin": ("/1", [(A93, 0.5), (A96, 0.5)]),
    # Journée d'hospitalisation des malades payants (article 4).
    f"{HOSP}.hopital_circonscription": ("currency", [(A93, 12), (A96, 15)]),
    f"{HOSP}.hopital_regional_medecine": ("currency", [(A93, 15), (A96, 20)]),
    f"{HOSP}.hopital_regional_chirurgie": ("currency", [(A93, 20), (A96, 30)]),
    f"{HOSP}.universitaire_medecine": ("currency", [(A93, 18), (A96, 30)]),
    f"{HOSP}.universitaire_specialites_medicales": ("currency", [(A93, 20), (A96, 35)]),
    f"{HOSP}.universitaire_nephrologie": ("currency", [(A93, 30), (A96, 35)]),
    f"{HOSP}.universitaire_chirurgie": ("currency", [(A93, 30), (A96, 40)]),
    f"{HOSP}.universitaire_reanimation": ("currency", [(A93, 30), (A96, 60)]),
    f"{HOSP}.taux_hospitalisation_jour": ("/1", [(A96, 0.75)]),
    f"{HOSP}.majoration_chambre_particuliere": ("/1", [(A93, 0.5), (A96, 0.5)]),
    f"{HOSP}.taux_accompagnant": ("/1", [(A93, 2 / 3), (A96, 2 / 3)]),
    f"{HOSP}.taux_accompagnant_indication_medicale": ("/1", [(A96, 0.5)]),
    f"{MP}.reduction_conventionnelle_plafond": ("/1", [(A96, 0.15)]),
    # Lettres clés (article 10, puis article 10 nouveau).
    f"{LC}.chirurgie": ("currency", [(A96, 1.4), (A08, 1.4)]),
    f"{LC}.specialite": ("currency", [(A96, 1.2), (A08, 1.2)]),
    f"{LC}.radiodiagnostic": ("currency", [(A96, 0.9), (A08, 0.9)]),
    f"{LC}.radiologie_interventionnelle": ("currency", [(A96, 0.9), (A08, None)]),
    f"{LC}.radiotherapie": ("currency", [(A96, 0.9), (A08, 0.9)]),
    f"{LC}.echographie": ("currency", [(A08, 3.6)]),
    f"{LC}.biologie": ("currency", [(A96, 0.16), (A08, 0.16)]),
    f"{LC}.anatomie_cytologie_pathologiques": ("currency", [(A96, 0.16), (A08, 0.16)]),
    f"{LC}.prelevement_produits_biologiques": ("currency", [(A96, 0.8), (A08, 0.8)]),
    f"{LC}.medecin_dentiste": ("currency", [(A96, 0.85), (A08, 0.85)]),
    f"{LC}.sage_femme": ("currency", [(A96, 0.6), (A08, 0.6)]),
    f"{LC}.physiotherapeute": ("currency", [(A96, 0.6), (A08, 0.6)]),
    f"{LC}.orthophoniste": ("currency", [(A96, 0.6), (A08, 0.6)]),
    f"{LC}.orthoptiste": ("currency", [(A96, 0.6), (A08, 0.6)]),
    f"{LC}.infirmier": ("currency", [(A96, 0.5), (A08, 0.5)]),
    f"{LC}.scanographie.s10": ("currency", [(A08, 90)]),
    f"{LC}.scanographie.s20": ("currency", [(A08, 180)]),
    f"{LC}.scanographie.s30": ("currency", [(A08, 240)]),
    f"{LC}.scanographie.s35": ("currency", [(A08, 290)]),
    f"{LC}.scanographie.s40": ("currency", [(A08, 325)]),
    f"{LC}.imagerie_resonance_magnetique.i3": ("currency", [(A08, 50)]),
    f"{LC}.imagerie_resonance_magnetique.i10": ("currency", [(A08, 180)]),
    f"{LC}.imagerie_resonance_magnetique.i15": ("currency", [(A08, 270)]),
    f"{LC}.imagerie_resonance_magnetique.i20": ("currency", [(A08, 325)]),
    f"{LC}.imagerie_resonance_magnetique.i25": ("currency", [(A08, 400)]),
    # Forfaits d'actes (article 11, remplacé en 1998, complété en 2003).
    f"{FORF}.hemodialyse_seance": ("currency", [(A96, 89), (A98, 89)]),
    f"{FORF}.lithotripsie": ("currency", [(A96, 500), (A98, 500)]),
    f"{FORF}.imagerie_resonance_magnetique": (
        "currency",
        [(A96, 360), (A98, 360), (A08, None)],
    ),
    f"{FORF}.accouchement_normal.universitaire": ("currency", [(A96, 150), (A98, 150)]),
    f"{FORF}.accouchement_normal.hopital_regional": (
        "currency",
        [(A96, 100), (A98, 100)],
    ),
    f"{FORF}.accouchement_normal.hopital_circonscription": (
        "currency",
        [(A96, 50), (A98, 50)],
    ),
    f"{FORF}.accouchement_cesarienne.universitaire": (
        "currency",
        [(A96, 300), (A98, 300)],
    ),
    f"{FORF}.accouchement_cesarienne.hopital_regional": (
        "currency",
        [(A96, 200), (A98, 200)],
    ),
    f"{FORF}.scanner_crane": ("currency", [(A96, 80), (A98, 80)]),
    f"{FORF}.scanner_reste_corps": ("currency", [(A96, 100), (A98, 100)]),
    f"{FORF}.fecondation_in_vitro": ("currency", [(A98, 250)]),
    f"{FORF}.insemination_sperme_conjoint": ("currency", [(A98, 50)]),
    f"{FORF}.photokeratectomie_laser": ("currency", [(A03, 300)]),
    f"{FORF}.photokeratectomie_laser_reprise": ("currency", [(A03, 100)]),
    f"{FORF}.keratomileusis_laser": ("currency", [(A03, 400)]),
    f"{FORF}.keratomileusis_laser_deux_yeux": ("currency", [(A03, 700)]),
    # Tarifs réduits en dinars, 1993-1998.
    f"{TR}.consultation.centre_sante_base": (
        "currency",
        [(D93, 0.6), (D94, 1), (D98, None)],
    ),
    f"{TR}.consultation.hopital_circonscription": (
        "currency",
        [(D93, 1), (D94, 1.5), (D98, None)],
    ),
    f"{TR}.consultation.hopital_regional": (
        "currency",
        [(D93, 1.5), (D94, 2), (D98, None)],
    ),
    f"{TR}.consultation.universitaire": ("currency", [(D93, 2), (D94, 3), (D98, None)]),
    f"{TR}.hospitalisation.hopital_circonscription_medecine": (
        "currency",
        [(D93, 7), (D94, 8), (D98, None)],
    ),
    f"{TR}.hospitalisation.hopital_regional_medecine": (
        "currency",
        [(D93, 10), (D94, 12), (D98, None)],
    ),
    f"{TR}.hospitalisation.universitaire_medecine": (
        "currency",
        [(D93, 12), (D94, 15), (D98, None)],
    ),
    f"{TR}.hospitalisation.hopital_circonscription_chirurgie": (
        "currency",
        [(D93, 13), (D94, 15), (D98, None)],
    ),
    f"{TR}.hospitalisation.hopital_regional_chirurgie": (
        "currency",
        [(D93, 15), (D94, 18), (D98, None)],
    ),
    f"{TR}.hospitalisation.universitaire_chirurgie": (
        "currency",
        [(D93, 18), (D94, 20), (D98, None)],
    ),
    f"{TR}.hospitalisation.universitaire_reanimation": (
        "currency",
        [(D94, 30), (D98, None)],
    ),
    # Tarifs réduits en part des tarifs des malades payants, depuis 1998.
    f"{TR}.taux_consultation.centre_sante_base": ("/1", [(D98, 0.20)]),
    f"{TR}.taux_consultation.hopital_circonscription": ("/1", [(D98, 0.25)]),
    f"{TR}.taux_consultation.hopital_regional": ("/1", [(D98, 0.30)]),
    f"{TR}.taux_consultation.universitaire": ("/1", [(D98, 0.30)]),
    f"{TR}.actes.taux_maximal_conventionnels": ("/1", [(D94, 0.10), (D98, None)]),
    f"{TR}.actes.prothese_taux_maximal_conventionnels": (
        "/1",
        [(D94, 0.10), (D98, None)],
    ),
    f"{TR}.actes.taux": ("/1", [(D98, 0.20)]),
    f"{TR}.actes.plafond": ("currency", [(D98, 30)]),
    f"{TR}.actes.hemodialyse_seance": ("currency", [(D98, 1)]),
    f"{TR}.actes.prothese_taux": ("/1", [(D98, 0.20)]),
    f"{TR}.actes.prothese_plafond": ("currency", [(D98, 50)]),
    f"{TR}.taux_accompagnant": ("/1", [(D98, 0.5)]),
    f"{TR}.taux_accompagnant_prescription": ("/1", [(D98, 1 / 3)]),
    f"{TR}.arrondi": ("currency", [(D98, 0.5)]),
}

# Séries dont des états antérieurs à la première date existent et ne sont pas versés.
INCOMPLETES = {
    chemin: "1993" for chemin, (_, suite) in SERIES.items() if suite[0][0] in (A93, D93)
}
INCOMPLETES.update(
    {
        chemin: "1997"
        for chemin, (_, suite) in SERIES.items()
        if suite[0][0] == A96 and (chemin.startswith(LC) or chemin.startswith(FORF))
    }
)


def parametre(chemin):
    noeud = TARIFS
    for nom in chemin.split("."):
        noeud = noeud.children[nom]
    return noeud


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


def egal(lu, attendu):
    if attendu is None:
        return lu is None
    return lu == pytest.approx(attendu)


LECTURES = []
for chemin, (_, suite) in SERIES.items():
    for rang, (texte, valeur) in enumerate(suite):
        LECTURES.append((chemin, texte[2], valeur))
        if rang > 0:
            LECTURES.append((chemin, veille(texte[2]), suite[rang - 1][1]))


@pytest.mark.parametrize(("chemin", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(chemin, instant, attendu):
    assert egal(parametre(chemin)(instant), attendu)


@pytest.mark.parametrize("chemin", SERIES)
def test_rien_avant_la_premiere_date(chemin):
    premiere = SERIES[chemin][1][0][0][2]
    assert parametre(chemin)(veille(premiere)) is None


@pytest.mark.parametrize("chemin", SERIES)
def test_chaque_date_porte_sa_reference(chemin):
    p = parametre(chemin)
    suite = SERIES[chemin][1]
    dates = {texte[2] for texte, _ in suite}
    references = {str(d): liste for d, liste in p.metadata["reference"].items()}
    assert {v.instant_str for v in p.values_list} == dates
    assert set(references) == dates
    for (fascicule, lien, date), _ in suite:
        liste = references[date]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert (
                "rticle" in reference["title"]
            ), f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert (
                fascicule in reference["note"]
            ), f"{chemin} au {date} : fascicule non cité"
            assert ", p. " in reference["note"] or ", pp. " in reference["note"]


@pytest.mark.parametrize("chemin", SERIES)
def test_note_des_series_incompletes(chemin):
    """La note est portée à la première date de la série, seule date de `notes`."""
    notes = {
        str(d): liste
        for d, liste in parametre(chemin).metadata.get("notes", {}).items()
    }
    if chemin in INCOMPLETES:
        premiere = SERIES[chemin][1][0][0][2]
        annee = INCOMPLETES[chemin]
        assert notes == {
            premiere: [
                {"note": f"Série incomplète : états antérieurs à {annee} non versés."}
            ]
        }
    else:
        assert notes == {}


@pytest.mark.parametrize("chemin", SERIES)
def test_unites(chemin):
    with open(f"{RACINE_PARAMETRES}/../units.yaml", encoding="utf-8") as f:
        enregistrees = {unite["name"] for unite in yaml.safe_load(f)}
    unite = parametre(chemin).metadata["unit"]
    assert unite == SERIES[chemin][0]
    assert unite in enregistrees


def test_le_sous_arbre_ne_porte_que_les_feuilles_attendues():
    feuilles = {
        d.name.removeprefix(f"{TARIFS.name}.")
        for d in TARIFS.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [TARIFS] + [d for d in TARIFS.get_descendants() if hasattr(d, "children")]
    for noeud in noeuds:
        assert list(noeud.children) and set(noeud.children) == set(
            noeud.metadata["order"]
        )


# Tarifs réduits de 1998 recalculés depuis les feuilles, pour une consultation : le décret
# désigne la consultation de médecine générale dans les centres de santé de base et les
# hôpitaux de circonscription (article 17). Les deux autres lignes demandent un choix de ligne
# de l'arrêté de 1996 que le texte ne fait pas : elles ne sont pas éprouvées ici.
@pytest.mark.parametrize(
    ("structure", "attendu"),
    [("centre_sante_base", 1.5), ("hopital_circonscription", 2.0)],
)
def test_tarif_reduit_de_consultation_1998_par_l_arrondi(structure, attendu):
    instant = "1998-03-08"
    tarif = parametre(f"{CONS}.medecine_generale")(instant)
    taux = parametre(f"{TR}.taux_consultation.{structure}")(instant)
    tranche = parametre(f"{TR}.arrondi")(instant)
    tranches = -(-round(tarif * taux * 1000) // round(tranche * 1000))
    assert tranches * tranche == pytest.approx(attendu)


def test_le_systeme_des_pensions_ne_lit_pas_la_sante():
    assert "sante" not in SOUS_ARBRES_PENSION

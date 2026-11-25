"""Droit de consommation sur les bières, vins, alcools et boissons alcoolisées (22-03 à 22-08).

Les valeurs attendues sont écrites en clair, tirées des fascicules lus au Journal officiel :
annexes I à III du décret n° 97-1368 (JORT n° 59 de 1997, p. 1316), annexes du décret
n° 2013-929 (JORT n° 14 de 2013, pp. 674-675), annexe du décret gouvernemental n° 2015-1768
(JORT n° 92 de 2015, p. 2722), tableaux annexés à la loi n° 88-62 par les lois de finances pour
2016 (article 44) et 2018 (article 45), article 20 de la loi de finances pour 2021. Sont
éprouvés, feuille par feuille :

- la valeur la veille et le jour de chaque date d'effet, clôtures comprises ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence : texte, article, fascicule, page et lien ;
- la note des séries dont les états antérieurs ne sont pas versés ;
- les unités, toutes enregistrées dans `units.yaml` ;
- la forme du sous-arbre, et le système des pensions qui ne le charge pas.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Standard Library
import datetime
import re

# Third Party
import pytest
import yaml

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.sous_ensembles import RACINE_PARAMETRES, SOUS_ARBRES_PENSION

ACCISES = TunisiaTaxBenefitSystem().parameters.fiscalite_indirecte.accises
RACINE = ACCISES.children["bieres_vins_alcools"]

D_1997 = ("1997-08-04", "JORT n° 59 du 25 juillet 1997", "/1997/1997F/Jo05997.pdf")
D_2013 = ("2013-02-21", "JORT n° 14 du 15 février 2013", "/2013/2013F/Jo0142013.pdf")
D_2015 = ("2015-11-24", "JORT n° 92 du 17 novembre 2015", "/2015/2015F/Jo0922015.pdf")
# Édition française lue sur un extrait local ; pist.tn ne sert que l'édition arabe.
LF_2016 = ("2016-01-01", "JORT n° 104 du 29 décembre 2015", "/2015/2015A/Ja1042015.pdf")
LF_2018 = ("2018-01-01", "JORT n° 101 du 19 décembre 2017", "/2017/2017F/Jo1012017.pdf")
LF_2021 = ("2021-01-01", "JORT n° 128 du 25 décembre 2020", "/2020/2020F/Jo1282020.pdf")


def suite(*couples):
    return [(texte[0], valeur, texte) for texte, valeur in couples]


def par_unite_avant_2015(v1997, v2013):
    return suite((D_1997, v1997), (D_2013, v2013), (D_2015, None))


# Chemin sous bieres_vins_alcools : unité, et suite des (date, valeur, texte). None : clôture.
SERIES = {
    "bieres.par_centilitre": (
        "currency/cl",
        suite((D_2015, 0.018), (LF_2016, 0.018), (LF_2018, 0.018), (LF_2021, 0.024)),
    ),
    "bieres.par_recipient.boite_moins_0_250_l": ("currency/unit", par_unite_avant_2015(0.160, 0.270)),
    "bieres.par_recipient.boite_0_250_a_0_320_l": ("currency/unit", par_unite_avant_2015(0.430, 0.730)),
    "bieres.par_recipient.bouteille_jusqu_a_0_320_l": ("currency/unit", par_unite_avant_2015(0.430, 0.730)),
    "bieres.par_recipient.recipient_0_321_a_0_400_l": ("currency/unit", par_unite_avant_2015(0.510, 0.870)),
    "bieres.par_recipient.recipient_0_401_a_0_500_l": ("currency/unit", par_unite_avant_2015(0.600, 1.020)),
    "bieres.par_recipient.recipient_0_501_a_0_660_l": ("currency/unit", par_unite_avant_2015(0.670, 1.140)),
    "bieres.par_recipient.recipient_0_661_a_1_l": ("currency/unit", par_unite_avant_2015(1.200, 2.040)),
    "bieres.pression": ("currency/l", par_unite_avant_2015(0.780, 1.330)),
    "bieres.vrac": ("currency/l", par_unite_avant_2015(0.610, 1.040)),
    "vins.vrac_livre_aux_embouteilleurs": (
        "currency/hl",
        suite((D_1997, 5.0), (D_2013, 7.5), (D_2015, 7.5), (LF_2016, 7.5), (LF_2018, 7.5)),
    ),
    "vins.mousseux": (
        "currency/unit",
        suite((D_1997, 16.0), (D_2013, 24.0), (D_2015, 24.0), (LF_2016, 24.0), (LF_2018, 24.0)),
    ),
    "vins.liqueur_mistelles_mouts": (
        "currency/unit",
        suite((D_1997, 2.5), (D_2013, 3.75), (D_2015, 3.75), (LF_2016, 3.75), (LF_2018, 3.75)),
    ),
    "vins.autres_vins_par_litre": (
        "currency/l",
        suite((D_2015, 1.8), (LF_2016, 1.8), (LF_2018, 1.8), (LF_2021, 2.4)),
    ),
    "vins.autres_vins_par_bouteille.bouteille_jusqu_a_0_375_l": ("currency/unit", par_unite_avant_2015(0.450, 0.675)),
    "vins.autres_vins_par_bouteille.bouteille_0_376_a_0_500_l": ("currency/unit", par_unite_avant_2015(0.600, 0.900)),
    "vins.autres_vins_par_bouteille.bouteille_0_501_a_0_750_l": ("currency/unit", par_unite_avant_2015(0.900, 1.350)),
    "vins.autres_vins_par_bouteille.bouteille_0_751_a_1_l": ("currency/unit", par_unite_avant_2015(1.200, 1.800)),
    # Le décret de 2013 laisse 22-05, 22-06 et Ex 22-08 « sans modification » : pas de date en 2013.
    "vermouths": ("/1", suite((D_1997, 2.0), (D_2015, 0.5), (LF_2016, 0.5), (LF_2018, 1.0))),
    "autres_boissons_fermentees": (
        "/1",
        suite((D_1997, 0.25), (D_2015, 0.25), (LF_2016, 0.25), (LF_2018, 0.25)),
    ),
    "alcool_ethylique_boissons": (
        "currency/hl",
        suite((D_1997, 380.0), (D_2013, 570.0), (D_2015, 570.0), (LF_2016, 570.0), (LF_2018, 570.0)),
    ),
    "spiritueux.eaux_de_vie": ("/1", suite((D_1997, 6.83), (D_2015, 0.5), (LF_2016, 0.5), (LF_2018, 1.0))),
    "spiritueux.spiritueux_non_classes": (
        "/1",
        suite((D_1997, 6.48), (D_2015, 0.5), (LF_2016, 0.5), (LF_2018, 1.0)),
    ),
    "spiritueux.spiritueux_classes": (
        "/1",
        suite((D_1997, 3.95), (D_2015, 0.5), (LF_2016, 0.5), (LF_2018, 1.0)),
    ),
    "spiritueux.pastis_anisette": ("/1", suite((D_1997, 5.97), (D_2015, 0.5), (LF_2016, 0.5), (LF_2018, 1.0))),
}

# Séries qui commencent en 1997 alors que des états antérieurs existent (loi n° 88-62,
# décret n° 91-551, décret n° 93-2090). Les tarifs au volume de 2015 sont nés avec leur texte.
COMPLETES = {"bieres.par_centilitre", "vins.autres_vins_par_litre"}
INCOMPLETES = set(SERIES) - COMPLETES


def parametre(chemin):
    noeud = RACINE
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
for chemin, (_, serie) in SERIES.items():
    for rang, (date, valeur, _) in enumerate(serie):
        LECTURES.append((chemin, date, valeur))
        if rang > 0:
            LECTURES.append((chemin, veille(date), serie[rang - 1][1]))


@pytest.mark.parametrize(("chemin", "instant", "attendu"), LECTURES)
def test_lecture_la_veille_et_le_jour_de_chaque_date(chemin, instant, attendu):
    assert egal(parametre(chemin)(instant), attendu)


@pytest.mark.parametrize("chemin", SERIES)
def test_rien_avant_la_premiere_date(chemin):
    premiere = SERIES[chemin][1][0][0]
    assert parametre(chemin)(veille(premiere)) is None


@pytest.mark.parametrize("chemin", SERIES)
def test_chaque_date_porte_sa_reference(chemin):
    p = parametre(chemin)
    serie = SERIES[chemin][1]
    dates = {date for date, _, _ in serie}
    references = {str(d): liste for d, liste in p.metadata["reference"].items()}
    assert {v.instant_str for v in p.values_list} == dates
    assert set(references) == dates
    for date, _, (_, fascicule, lien) in serie:
        liste = references[date]
        assert liste, f"{chemin} : aucune référence au {date}"
        for reference in liste:
            assert "rticle" in reference["title"], f"{chemin} au {date} : article non cité"
            assert reference["href"] == f"https://www.pist.tn/jort{lien}"
            assert fascicule in reference["note"], f"{chemin} au {date} : fascicule non cité"
            assert re.search(r"\bpp?\. \d{3,4}", reference["note"]), f"{chemin} au {date} : page non citée"


def test_mousseux_2016_rapporte_l_ecart_des_deux_editions():
    note = parametre("vins.mousseux").metadata["reference"]["2016-01-01"][0]["note"]
    assert "4,000D / l'unité" in note
    assert "24,000" in note
    assert "p. 3609" in note


@pytest.mark.parametrize("chemin", SERIES)
def test_note_des_series_incompletes(chemin):
    notes = {str(d): liste for d, liste in parametre(chemin).metadata.get("notes", {}).items()}
    if chemin in INCOMPLETES:
        premiere = SERIES[chemin][1][0][0]
        assert notes == {premiere: [{"note": "Série incomplète : états antérieurs à 1997 non versés."}]}
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
        d.name.removeprefix(f"{RACINE.name}.")
        for d in RACINE.get_descendants()
        if not hasattr(d, "children")
    }
    assert feuilles == set(SERIES)


def test_ordre_declare():
    noeuds = [
        RACINE,
        parametre("bieres"),
        parametre("bieres.par_recipient"),
        parametre("vins"),
        parametre("vins.autres_vins_par_bouteille"),
        parametre("spiritueux"),
    ]
    for noeud in noeuds:
        assert set(noeud.children) == set(noeud.metadata["order"])
    assert "bieres_vins_alcools" in ACCISES.metadata["order"]
    assert set(ACCISES.children) == set(ACCISES.metadata["order"])


# Tarif à des dates repères : (bière 0,661-1 l par unité, bière par cl, vin 0,751-1 l par
# unité, autres vins par litre, mousseux, vermouths, whiskies classés).
ETATS = [
    ("1997-08-04", 1.200, None, 1.200, None, 16.0, 2.0, 3.95),
    ("2013-02-21", 2.040, None, 1.800, None, 24.0, 2.0, 3.95),
    ("2015-11-24", None, 0.018, None, 1.8, 24.0, 0.5, 0.5),
    ("2016-01-01", None, 0.018, None, 1.8, 24.0, 0.5, 0.5),
    ("2018-01-01", None, 0.018, None, 1.8, 24.0, 1.0, 1.0),
    ("2021-01-01", None, 0.024, None, 2.4, 24.0, 1.0, 1.0),
    ("2026-01-01", None, 0.024, None, 2.4, 24.0, 1.0, 1.0),
]


@pytest.mark.parametrize(
    ("date", "biere_unite", "biere_cl", "vin_unite", "vin_litre", "mousseux", "vermouths", "whiskies"),
    ETATS,
)
def test_etat_du_droit_aux_dates_reperes(
        date, biere_unite, biere_cl, vin_unite, vin_litre, mousseux, vermouths, whiskies):
    lus = [
        parametre("bieres.par_recipient.recipient_0_661_a_1_l")(date),
        parametre("bieres.par_centilitre")(date),
        parametre("vins.autres_vins_par_bouteille.bouteille_0_751_a_1_l")(date),
        parametre("vins.autres_vins_par_litre")(date),
        parametre("vins.mousseux")(date),
        parametre("vermouths")(date),
        parametre("spiritueux.spiritueux_classes")(date),
    ]
    attendus = [biere_unite, biere_cl, vin_unite, vin_litre, mousseux, vermouths, whiskies]
    for lu, attendu in zip(lus, attendus):
        assert egal(lu, attendu)


def test_le_systeme_des_pensions_ne_charge_pas_la_fiscalite_indirecte():
    assert "fiscalite_indirecte" not in SOUS_ARBRES_PENSION

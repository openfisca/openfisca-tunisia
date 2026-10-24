"""Régime de retraite des députés : retenue et contribution de l'État, 1985-2023.

Les valeurs attendues sont écrites en clair, tirées des textes lus au Journal officiel : loi
n° 85-16, article 5 ; loi n° 94-71 ; loi de finances pour 2002, article 85 ; loi n° 2007-43,
article premier ; loi de finances pour 2026, articles 102 et 103. Sont éprouvés :

- la valeur la veille et le jour de chaque date d'effet ;
- le début de chaque série : rien n'est lu la veille de sa première date ;
- chaque valeur datée porte sa référence, avec un lien vers pist.tn ;
- la note de série incomplète et l'unité.

Un test YAML n'asserte que des variables : ce test lit donc les paramètres.
"""

# Standard Library
import datetime

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

DEPUTES = TunisiaTaxBenefitSystem().parameters.prelevements_sociaux.cotisations_sociales.secteur_public.regimes_speciaux.deputes

SERIES = {
    "retenue": [
        ("1985-03-17", 0.10),
        ("1994-07-01", 0.11),
        ("2002-07-01", 0.115),
        ("2003-07-01", 0.1175),
        ("2004-07-01", 0.12),
        ("2007-07-01", 0.124),
        ("2008-07-01", 0.128),
        ("2009-07-01", 0.132),
        ("2023-03-13", 0.1325),
    ],
    "contribution_etat": [
        ("1985-03-17", 0.15),
        ("1995-07-01", 0.162),
        ("2002-07-01", 0.167),
        ("2003-07-01", 0.1695),
        ("2004-07-01", 0.172),
        ("2005-07-01", 0.1745),
        ("2006-07-01", 0.177),
        ("2007-01-01", 0.183),
        ("2008-01-01", 0.189),
        ("2009-01-01", 0.195),
        ("2023-03-13", 0.205),
    ],
}

CAS = [
    (feuille, i, date, valeur)
    for feuille, serie in SERIES.items()
    for i, (date, valeur) in enumerate(serie)
]


def veille(date):
    return (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()


@pytest.mark.parametrize(("feuille", "rang", "date", "valeur"), CAS)
def test_valeur_le_jour_et_la_veille(feuille, rang, date, valeur):
    parametre = DEPUTES.children[feuille]
    assert parametre(date) == pytest.approx(valeur)
    if rang == 0:
        assert parametre(veille(date)) is None
    else:
        assert parametre(veille(date)) == pytest.approx(SERIES[feuille][rang - 1][1])


@pytest.mark.parametrize("feuille", SERIES)
def test_dates_et_references(feuille):
    parametre = DEPUTES.children[feuille]
    dates = sorted(str(v.instant_str) for v in parametre.values_list)
    assert dates == [date for date, _ in SERIES[feuille]]
    references = parametre.metadata["reference"]
    assert sorted(str(date) for date in references) == dates
    for liste in references.values():
        for reference in liste:
            assert reference["href"].startswith("https://www.pist.tn/jort/")
            assert reference["note"].startswith("JORT n° ")


@pytest.mark.parametrize("feuille", SERIES)
def test_unite_et_serie_incomplete(feuille):
    parametre = DEPUTES.children[feuille]
    assert parametre.metadata["unit"] == "/1"
    notes = parametre.metadata["notes"]
    assert notes[next(iter(notes))][0]["note"] == "Série incomplète : états antérieurs à 1985 non versés."


def test_loi_de_finances_2026_lue_sur_l_edition_arabe():
    for feuille in SERIES:
        reference = DEPUTES.children[feuille].metadata["reference"]
        dernier = reference[max(reference, key=str)][0]
        assert "/2025/2025A/Ja1482025.pdf" in dernier["href"]

"""Salaire minimum : dates d'effet et indemnités hors salaire minimum, lues au JORT.

- SMAG : 550 millimes au 1er octobre 1969 (décret n° 69-344, art. 8) ; 1,200 dinar au
  1er février 1977 (décret n° 77-116, art. 6) ; 10,608 puis 11,608 dinars aux 1er juillet et
  1er décembre 2012 (décret n° 2012-1982, art. 1er).
- SMIG : le décret n° 71-164 ne relève pas le minimum ; il sert en sus une indemnité de
  cherté de vie (0,020 dinar l'heure, 4 dinars par mois), hors assiette sociale (art. 5),
  que le décret n° 74-63 intègre au SMIG au 1er janvier 1974.
- Indemnité complémentaire provisoire : 1er avril 1981 (décret n° 81-437, art. 10) ; la
  majoration du décret n° 82-501 s'y ajoute au 1er février 1982 (art. 13) sans la modifier.

Les dates sont lues la veille et le jour de chaque effet. Un test YAML n'asserte que des
variables, et aucune ne lit ces paramètres sur ces périodes : le test lit donc les paramètres.
"""

# Third Party
import pytest

# First Party
from openfisca_tunisia import TunisiaTaxBenefitSystem

MARCHE_TRAVAIL = TunisiaTaxBenefitSystem().parameters.marche_travail

CAS = [
    # SMAG journalier
    ("smag_journalier", "1969-09-30", 0.5),
    ("smag_journalier", "1969-10-01", 0.55),
    ("smag_journalier", "1977-01-31", 0.9),
    ("smag_journalier", "1977-02-01", 1.2),
    ("smag_journalier", "2012-06-30", 9),
    ("smag_journalier", "2012-07-01", 10.608),
    ("smag_journalier", "2012-11-30", 10.608),
    ("smag_journalier", "2012-12-01", 11.608),
    # SMIG : le minimum de 1966 vaut jusqu'au 31 décembre 1973
    ("smig_48h_horaire", "1971-05-01", 0.084),
    ("smig_48h_horaire", "1973-12-31", 0.084),
    ("smig_48h_horaire", "1974-01-01", 0.13),
    ("smig_40h_horaire", "1973-12-31", 0.084),
    ("smig_48h_mensuel", "1973-12-31", 17.472),
    ("smig_48h_mensuel", "1974-01-01", 27.04),
    ("smig_40h_mensuel", "1973-12-31", 14.56),
    ("smig_40h_mensuel", "1974-01-01", 22.533),
    # Indemnité de cherté de vie, en sus du minimum
    ("indemnite_cherte_de_vie_horaire", "1971-05-01", 0.02),
    ("indemnite_cherte_de_vie_horaire", "1973-12-31", 0.02),
    ("indemnite_cherte_de_vie_horaire", "1974-01-01", 0),
    ("indemnite_cherte_de_vie_mensuelle", "1971-05-01", 4),
    # Indemnité complémentaire provisoire et majoration de 1982
    ("indemnite_complementaire_provisoire", "1981-04-01", 10),
    ("indemnite_complementaire_provisoire", "1982-02-01", 10),
    ("majoration_smig_48h_mensuel", "1982-02-01", 20.368),
    ("majoration_smig_40h_mensuel", "1982-02-01", 20),
]


@pytest.mark.parametrize(("nom", "instant", "attendu"), CAS)
def test_valeur(nom, instant, attendu):
    assert MARCHE_TRAVAIL.children[nom](instant) == pytest.approx(attendu)


@pytest.mark.parametrize(
    "nom",
    [
        "indemnite_cherte_de_vie_horaire",
        "indemnite_cherte_de_vie_mensuelle",
        "indemnite_complementaire_provisoire",
        "majoration_smig_48h_mensuel",
        "majoration_smig_40h_mensuel",
    ],
)
def test_pas_de_valeur_avant_le_texte(nom):
    premiere = {
        "indemnite_cherte_de_vie_horaire": "1971-04-30",
        "indemnite_cherte_de_vie_mensuelle": "1971-04-30",
        "indemnite_complementaire_provisoire": "1981-03-31",
        "majoration_smig_48h_mensuel": "1982-01-31",
        "majoration_smig_40h_mensuel": "1982-01-31",
    }[nom]
    assert MARCHE_TRAVAIL.children[nom](premiere) is None


@pytest.mark.parametrize(
    ("regime", "smig"),
    [("48h", 85.072), ("40h", 75.586)],
)
def test_smig_1982_se_decompose_selon_le_decret_82_501(regime, smig):
    """Art. 2 et 3 : SMIG de 1980 + indemnité complémentaire provisoire + majoration."""
    avant = MARCHE_TRAVAIL.children[f"smig_{regime}_mensuel"]("1981-03-31")
    icp = MARCHE_TRAVAIL.children["indemnite_complementaire_provisoire"]("1982-02-01")
    majoration = MARCHE_TRAVAIL.children[f"majoration_smig_{regime}_mensuel"](
        "1982-02-01"
    )
    assert avant + icp + majoration == pytest.approx(smig)
    assert MARCHE_TRAVAIL.children[f"smig_{regime}_mensuel"](
        "1982-02-01"
    ) == pytest.approx(smig)


def test_montant_mensuel_de_cherte_de_vie_sans_valeur_apres_1973():
    """Le décret n° 74-63 n'intègre au SMIG que le montant horaire : la série mensuelle s'arrête."""
    mensuelle = MARCHE_TRAVAIL.children["indemnite_cherte_de_vie_mensuelle"]
    assert mensuelle("1973-12-31") == pytest.approx(4)
    assert mensuelle("1974-01-01") is None

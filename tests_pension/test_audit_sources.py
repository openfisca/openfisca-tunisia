"""Le rapport d'audit rattache chaque texte cité à son fascicule du JORT.

Le cache `jort_cache.db` range sous un même numéro des enregistrements qui ne sont pas
le texte cité : le rectificatif, qui porte le type, le numéro et la date de signature
du texte qu'il corrige, et les homonymes d'un autre type — la circulaire n° 2009-20 n'est
pas la loi n° 2009-20. Trié par date de signature puis par
identifiant, le cache plaçait le mauvais enregistrement en tête, et le rapport le
retenait (issue #33).

Les enregistrements ci-dessous reproduisent ceux du cache ; les tests n'ont pas besoin
de la base, sauf `test_avec_le_cache_reel`, sauté quand elle est absente.
"""

import importlib.util
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parent.parent / "scripts" / "generate_pension_source_audit.py"
_spec = importlib.util.spec_from_file_location("generate_pension_source_audit", SCRIPT)
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


def record(type_, numero, titre, date_signature, jort_annee, jort_numero, pdf):
    return {
        "type": type_,
        "numero": numero,
        "titre": titre,
        "date_signature": date_signature,
        "date_publication": None,
        "jort_annee": jort_annee,
        "jort_numero": jort_numero,
        "pages": None,
        "pdf_fr": pdf,
        "pdf_ar": None,
    }


# Pour chaque texte : la référence telle que l'écrivent les paramètres, puis les
# enregistrements du cache dans l'ordre où la requête les rend, le mauvais en tête.
CAS = {
    "1974-499": (
        {
            "title": "Décret n° 74-499 du 27 avril 1974, relatif au régime de pension de "
            "vieillesse, d'invalidité et de survivants dans le secteur non agricole, "
            "article 17",
            "href": "https://www.pist.tn/jort/1974/1974F/Jo03074.pdf",
        },
        [
            record(
                "Decret", "74-499",
                "Decret n° 74-499 du 27 Avril 1974, relatif au regime de pension de "
                "vieillesse,invalidite et de survivants dans le secteur non agricole "
                "(rectificatif)",
                "1974-04-27", 1974, 39, "/jort/1974/1974F/Jo03974.pdf",
            ),
            record(
                "Decret", "74-499",
                "Decret n° 74-499 du 27 Avril 1974, relatif au regime de pension de "
                "vieillesse,d'invalidite et de survivants dans le secteurs non agricole",
                "1974-04-27", 1974, 30, "/jort/1974/1974F/Jo03074.pdf",
            ),
        ],
        30,
    ),
    "1982-1030": (
        {
            "title": "Décret n° 82-1030 du 15 juillet 1982, modifiant le décret n° 74-499 "
            "du 27 avril 1974 relatif au régime des pensions de vieillesse, d'invalidité "
            "et de survivants dans le secteur non agricole, article premier (article 15 bis)",
            "href": "https://www.pist.tn/jort/1982/1982F/Jo05182.pdf",
        },
        [
            record(
                "Decret", "82-1030",
                "Decret n° 82-1030 du 15 Juillet 1982, modifiant le decret no 74-499 du 27 "
                "avril 1974,relatif au regime de pensions de vieillesse,d'invalidite et de "
                "survivants,dans le secteur non agricole (J.O.R.T.no 51 du 20 et 23 juillet "
                "1982,page 1606)(rectificatif)",
                "1982-07-15", 1982, 66, "/jort/1982/1982F/Jo06682.pdf",
            ),
            record(
                "Decret", "82-1030",
                "Decret n° 82-1030 du 15 Juillet 1982, modifiant le decret no 74-499 du 27 "
                "avril 1974 relatif au regime des pensions de veillesse d'invalidite et de "
                "survivants dans le secteur non agricole",
                "1982-07-15", 1982, 51, "/jort/1982/1982F/Jo05182.pdf",
            ),
        ],
        51,
    ),
    "1981-6": (
        {
            "title": "Loi n° 81-6 du 12 février 1981, organisant les régimes de sécurité "
            "sociale dans le secteur agricole, article 49",
            "href": "https://www.pist.tn/jort/1981/1981F/Jo00981.pdf",
        },
        [
            record(
                "Loi", "81-6",
                "Loi n° 81-6 du 12 Février 1981, organisant les regimes de securite sociale "
                "dans le secteur agricole (rectificatif)",
                "1981-02-12", 1981, 26, "/jort/1981/1981F/Jo02681.pdf",
            ),
            record(
                "Loi", "81-6",
                "Loi n° 81-6 du 12 Février 1981, organisant les regimes de securite sociale "
                "dans le secteur agricole",
                "1981-02-12", 1981, 9, "/jort/1981/1981F/Jo00981.pdf",
            ),
            record(
                "Decret-Loi", "81-6",
                "Decret-Loi n° 81-6 du 01 Septembre 1981, completant l'article du 3 du "
                "decret-loi no 74-22 du 2 novembre 1974",
                "1981-09-01", 1981, 55, "/jort/1981/1981F/Jo05581.pdf",
            ),
        ],
        9,
    ),
    "2009-20": (
        {
            "title": "Loi n° 2009-20 du 13 avril 2009, portant dispositions exceptionnelles "
            "relatives à la retraite des professeurs de l'enseignement supérieur, "
            "article 2 (article 29 bis de la loi n° 85-12)",
            "href": "https://www.pist.tn/jort/2009/2009F/Jo0302009.pdf",
        },
        [
            record(
                "Circulaire", "2009-20",
                "Circulaire n° 2009-20, portant mise en circulation d'une nouvelle piece "
                "de monnaie tunisienne",
                None, 2009, 100, "/jort/2009/2009F/Jo1002009.pdf",
            ),
            record(
                "Loi", "2009-20",
                "Loi n° 2009-20 du 13 Avril 2009, portant dispositions exceptionnelles "
                "relatives a la retraite des professeurs de l'enseignement superieur",
                "2009-04-13", 2009, 30, "/jort/2009/2009F/Jo0302009.pdf",
            ),
        ],
        30,
    ),
}


@pytest.mark.parametrize("law", sorted(CAS))
def test_le_texte_principal_l_emporte(law):
    reference, records, fascicule = CAS[law]
    hints = audit.collect_citation_hints([reference])[law]
    best = audit.best_jort_match(law, records, hints)
    assert best is not None
    assert best["jort_numero"] == fascicule
    assert not audit.is_rectificatif(best)


@pytest.mark.parametrize("law", ["1974-499", "1982-1030", "1981-6"])
def test_le_rectificatif_passe_apres_le_texte_meme_sans_lien(law):
    reference, records, fascicule = CAS[law]
    hints = {"types": audit.collect_citation_hints([reference])[law]["types"]}
    ranked = audit.rank_jort_matches(law, records, hints)
    assert ranked[0]["jort_numero"] == fascicule
    assert audit.is_rectificatif(ranked[-1])


def test_la_circulaire_homonyme_est_ecartee():
    reference, records, _ = CAS["2009-20"]
    hints = audit.collect_citation_hints([reference])["2009-20"]
    ranked = audit.rank_jort_matches("2009-20", records, hints)
    assert [match["type"] for match in ranked] == ["Loi"]


def test_le_decret_loi_n_est_pas_la_loi():
    reference, records, _ = CAS["1981-6"]
    hints = audit.collect_citation_hints([reference])["1981-6"]
    ranked = audit.rank_jort_matches("1981-6", records, hints)
    assert {match["type"] for match in ranked} == {"Loi"}


def test_concordance_des_types():
    assert audit.text_type_matches("décret", "Decret gouvernemental")
    assert audit.text_type_matches("loi", "Loi organique")
    assert audit.text_type_matches("arrêté", "Arrete")
    assert not audit.text_type_matches("décret", "Decret-Loi")
    assert not audit.text_type_matches("loi", "Circulaire")


def test_le_lien_appartient_au_premier_texte_du_titre():
    reference = CAS["1982-1030"][0]
    hints = audit.collect_citation_hints([reference])
    assert hints["1982-1030"]["pdfs"] == {"/jort/1982/1982f/jo05182.pdf"}
    assert hints["1974-499"] == {"types": {"decret"}, "pdfs": set()}


def test_un_texte_sans_type_concordant_n_est_pas_rattache():
    _, records, _ = CAS["2009-20"]
    hints = {"types": {"decret"}, "pdfs": set()}
    assert audit.best_jort_match("2009-20", records, hints) is None


@pytest.mark.skipif(
    not audit.EXTERNAL_JORT_CACHE.exists(),
    reason="jort_cache.db absent (dépôt PDFs-legislation-tunisie non cloné à côté)",
)
@pytest.mark.parametrize("law", sorted(CAS))
def test_avec_le_cache_reel(law):
    reference, _, fascicule = CAS[law]
    hints = audit.collect_citation_hints([reference])[law]
    records = audit.query_external_jort_cache({law})[law]
    assert audit.best_jort_match(law, records, hints)["jort_numero"] == fascicule


def test_un_mot_qui_finit_en_loi_n_est_pas_un_type():
    hints = audit.collect_citation_hints(["Contrat d'emploi n° 81-6"])
    assert hints == {}

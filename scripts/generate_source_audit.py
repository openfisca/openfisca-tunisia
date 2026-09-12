#!/usr/bin/env python3
"""Audit des sources des paramètres d'OpenFisca-Tunisia.

Mesure, sous-arbre par sous-arbre, ce que les paramètres disent de leur fondement
juridique : combien portent une valeur, combien une référence, de quelle qualité est
cette référence, et si le texte cité se retrouve dans le corpus du JORT.

Porté depuis `openfisca-tunisia-pension`, avec trois différences que l'échelle impose :
le dépôt compte 2 400 fichiers au lieu de 66, les valeurs sont le plus souvent portées
par des nœuds *internes* aux fichiers, et la qualité d'une référence — structurée ou
non, sur pist.tn ou non, datée ou non — y est plus instructive que sa seule présence.

Usage :
    uv run python scripts/generate_source_audit.py [--sans-jort] [--sortie CHEMIN]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sqlite3
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterator

import yaml

ROOT = Path(__file__).resolve().parents[1]
PARAMETERS_DIR = ROOT / "openfisca_tunisia" / "parameters"
REPORT_PATH = ROOT / "reports" / "source_audit.md"

# Le corpus du JORT est un dépôt voisin, hors de celui-ci. Il n'est pas toujours à la
# même place — un worktree déplace `ROOT` —, d'où cette recherche, et l'option
# `--corpus-jort` qui la court-circuite. Absent, l'audit se rabat sur `--sans-jort`.
CANDIDATS_JORT = (
    ROOT.parent / "PDFs-legislation-tunisie" / "jort_cache.db",
    Path.home() / "projets" / "PDFs-legislation-tunisie" / "jort_cache.db",
)


def trouver_corpus_jort() -> Path | None:
    for candidat in CANDIDATS_JORT:
        if candidat.exists():
            return candidat
    return None


# Clés réservées d'OpenFisca : tout le reste, dans un fichier de paramètres, est un
# nœud enfant. C'est par elles qu'on distingue un sous-paramètre d'une métadonnée.
CLES_RESERVEES = frozenset(
    {"description", "metadata", "values", "brackets", "documentation", "reference"}
)

# Un numéro de texte précédé de son type. Le `n°` est facultatif — le dépôt écrit
# « Décret 97-1832 » aussi bien que « décret n° 97-1832 » — mais le type reste
# obligatoire : c'est lui qui empêche « JORT n° 104 des 30-31 décembre » et
# « pp. 838-839 » de passer pour des numéros de texte.
TEXTE_CITE_RE = re.compile(
    r"\b(?P<type>lois?(?:\s+organique|\s+constitutionnelle|\s+d['’]orientation)?"
    r"|d[ée]crets?(?:[-‑\s]lois?|\s+gouvernemental|\s+pr[ée]sidentiel)?"
    r"|arr[êe]t[ée]s?|circulaires?|d[ée]cisions?|avis)"
    r"[-‑\s]*(?:n[°º]\s*)?(?P<a>\d{2,4})[-‑](?P<b>\d{1,4})(?!\d)",
    re.IGNORECASE,
)

# Un texte cité par sa seule date : « arrêté conjoint ... du 19 mai 2020 ». Réel, mais
# insoluble contre un cache indexé par numéro : il mérite sa propre catégorie.
TEXTE_SANS_NUMERO_RE = re.compile(
    r"\b(lois?|d[ée]crets?(?:[-‑\s]lois?)?|arr[êe]t[ée]s?|circulaires?|d[ée]cisions?)"
    r"\b(?![^.;]{0,40}\d{2,4}[-‑]\d)[^.;]{0,60}?\bdu\s+\d{1,2}(?:er)?\s+\w+\s+\d{4}",
    re.IGNORECASE,
)

# La suite d'une énumération : « …/2961/2960 », « …+2019-209 ». Soit `année-numéro`,
# soit un numéro seul, qui reprend alors l'année du texte précédent.
SUITE_NUMEROS_RE = re.compile(
    r"\s*[/+]\s*(?:(?P<annee>\d{2,4})[-‑](?P<numero>\d{1,4})|(?P<seul>\d{1,4}))(?!\d)"
)

JORT_PDF_RE = re.compile(r"(/jort/\d{4}/\d{4}F/[^/?#]+\.pdf)$", re.IGNORECASE)
RECTIFICATIF_RE = re.compile(r"\brectificatif\b", re.IGNORECASE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

HOTE_PROBANT = "www.pist.tn"
HOTE_NON_PROBANT = "gitlab.com"


# --------------------------------------------------------------------------------
# Lecture de l'arbre sur le disque
# --------------------------------------------------------------------------------


# `CSafeLoader` s'appuie sur libyaml : sur les 1 557 fichiers du dépôt, il fait passer
# l'analyse de ~35 s à ~4 s. Il n'est pas garanti présent, d'où le repli.
CHARGEUR = getattr(yaml, "CSafeLoader", yaml.SafeLoader)


def charger_yaml(chemin: Path) -> Any:
    with chemin.open(encoding="utf-8") as flux:
        return yaml.load(flux, Loader=CHARGEUR)


def texte_date(cle: Any) -> str:
    """Une date non guillemetée arrive de YAML en `datetime.date`, non en `str`."""
    if isinstance(cle, (dt.date, dt.datetime)):
        return cle.isoformat()[:10]
    return str(cle)


def est_une_date(cle: Any) -> bool:
    return bool(DATE_RE.match(texte_date(cle)))


# --------------------------------------------------------------------------------
# Références : leur forme, leur hôte, leur datation
# --------------------------------------------------------------------------------


def entrees_de_reference(reference: Any, date: str | None = None) -> Iterator[dict]:
    """Aplatit une référence en entrées `{date, titre, href, libre}`.

    Trois formes coexistent dans le dépôt : la chaîne libre, le dictionnaire
    structuré `{title, href, note}`, et — de très loin la plus répandue — le
    dictionnaire indexé par date de valeur dont chaque entrée est l'une des deux
    précédentes, ou une liste d'entre elles.
    """
    if reference is None:
        return
    if isinstance(reference, str):
        yield {"date": date, "titre": reference, "href": None, "libre": True}
    elif isinstance(reference, list):
        for element in reference:
            yield from entrees_de_reference(element, date)
    elif isinstance(reference, dict):
        if "title" in reference or "href" in reference:
            yield {
                "date": date,
                "titre": str(reference.get("title") or ""),
                "href": reference.get("href"),
                "libre": False,
            }
        else:
            for cle, valeur in reference.items():
                sous_date = texte_date(cle) if est_une_date(cle) else date
                yield from entrees_de_reference(valeur, sous_date)


def hote(href: str | None) -> str | None:
    if not href:
        return None
    correspondance = re.match(r"https?://([^/]+)", href.strip())
    return correspondance.group(1).lower() if correspondance else None


# --------------------------------------------------------------------------------
# Textes cités
# --------------------------------------------------------------------------------


def normaliser_type(valeur: str | None) -> str:
    """« Décret-Loi » → « decret-loi » : sans accents, en minuscules, au singulier."""
    decompose = unicodedata.normalize("NFKD", valeur or "")
    sans_accent = "".join(c for c in decompose if not unicodedata.combining(c))
    mots = sans_accent.replace("‑", "-").replace("-", " ").lower().split()
    mots = [mot[:-1] if len(mot) > 3 and mot.endswith("s") else mot for mot in mots]
    return " ".join(mots)


def identifiant(a: str, b: str) -> str | None:
    """`(97, 1832)` → `1997-1832` : le premier terme est l'année, toujours.

    On ne tente pas de redresser la forme inversée « décret-loi 79-2022 », où le
    numéro précède l'année. Le dépôt cite en effet les décrets `96-1990`, `96-1994`,
    `96-2000`, `96-2007` et `99-2016`, dont le second terme a l'allure d'une année
    sans en être une : toute règle qui rattraperait `79-2022` corromprait ces cinq
    textes-là. Un audit ne devine pas — la forme inversée ressort d'elle-même en
    « texte introuvable dans le corpus », ce qui est le signalement attendu.
    """
    if len(a) == 2:
        annee = int(a)
        annee_pleine = 2000 + annee if annee < 30 else 1900 + annee
    else:
        annee_pleine = int(a)
    if not 1850 <= annee_pleine <= 2099:
        return None
    return f"{annee_pleine}-{int(b)}"


def textes_cites(texte: str) -> list[tuple[str, str]]:
    """Les `(identifiant, type)` des textes nommés dans une chaîne.

    Le dépôt enchaîne souvent plusieurs textes derrière un seul type :
    « Décret 2012-2964/2961/2960 », « Décret 2019-433+2019-209+2019-1133 ». Les
    numéros qui suivent un `/` ou un `+` sont donc rattachés au même type, et ceux
    qui viennent sans année — « Décret 96-1912/1908/1909 » — héritent de la sienne.
    """
    trouves = []
    for m in TEXTE_CITE_RE.finditer(texte):
        loi = identifiant(m["a"], m["b"])
        if not loi:
            continue
        type_cite = normaliser_type(m["type"])
        trouves.append((loi, type_cite))
        annee = m["a"]
        position = m.end()
        while (suite := SUITE_NUMEROS_RE.match(texte, position)) is not None:
            if suite["annee"] is not None:
                annee, numero = suite["annee"], suite["numero"]
            else:
                numero = suite["seul"]
            enchaine = identifiant(annee, numero)
            if enchaine:
                trouves.append((enchaine, type_cite))
            position = suite.end()
    return trouves


def numeros_jort(loi: str) -> tuple[str, str]:
    """Le cache enregistre « 97-1832 » pour 1997 et « 2007-268 » pour 2007."""
    annee, suffixe = loi.split("-", 1)
    court = f"{int(annee) % 100:02d}-{suffixe}" if int(annee) < 2000 else loi
    return loi, court


# --------------------------------------------------------------------------------
# Rapprochement avec le corpus JORT
# --------------------------------------------------------------------------------


class CorpusJort:
    """Accès mémorisé au cache JORT : une requête par texte, jamais deux."""

    REQUETE = """
        SELECT type, numero, titre, date_signature, date_publication,
               jort_annee, jort_numero, pages, pdf_fr
        FROM textes WHERE numero IN (?, ?) ORDER BY date_signature, recid
    """

    def __init__(self, chemin: Path | None, actif: bool = True) -> None:
        self.chemin = chemin
        self.disponible = bool(actif and chemin and chemin.exists())
        self._cache: dict[str, list[dict]] = {}
        self._connexion = (
            sqlite3.connect(f"file:{chemin}?mode=ro", uri=True)
            if self.disponible
            else None
        )

    def enregistrements(self, loi: str) -> list[dict]:
        if loi in self._cache:
            return self._cache[loi]
        lignes: list[dict] = []
        if self._connexion is not None:
            colonnes = (
                "type numero titre date_signature date_publication "
                "jort_annee jort_numero pages pdf_fr"
            ).split()
            for ligne in self._connexion.execute(self.REQUETE, numeros_jort(loi)):
                lignes.append(dict(zip(colonnes, ligne)))
        self._cache[loi] = lignes
        return lignes

    def fermer(self) -> None:
        if self._connexion is not None:
            self._connexion.close()


def type_concorde(attendu: str, effectif: str | None) -> bool:
    """Un « décret » cité admet un « décret gouvernemental », mais pas un
    « décret-loi » ; une « loi » admet une « loi organique », pas une circulaire."""
    reel = normaliser_type(effectif)
    return reel == attendu or reel.startswith(attendu + " ")


def est_rectificatif(enregistrement: dict) -> bool:
    """Le cache range un rectificatif sous le type et le numéro du texte qu'il
    corrige ; seule la mention « (rectificatif) » du titre l'en distingue."""
    return bool(
        RECTIFICATIF_RE.search(enregistrement.get("type") or "")
        or RECTIFICATIF_RE.search(enregistrement.get("titre") or "")
    )


def classer_enregistrements(
    loi: str, enregistrements: list[dict], indices: dict[str, set[str]]
) -> list[dict]:
    """Les enregistrements qui peuvent être le texte cité, le meilleur en tête.

    Le type doit concorder avec le type cité — la circulaire n° 2009-20 n'est pas la
    loi n° 2009-20 — et un rectificatif passe toujours après le texte principal, qui
    porte les mêmes type, numéro et date de signature. Viennent ensuite la
    concordance du fascicule avec le lien de la référence, puis celle de l'année de
    signature avec l'année du numéro. Le tri est stable.
    """
    attendus = indices.get("types", set())
    if attendus:
        enregistrements = [
            e
            for e in enregistrements
            if any(type_concorde(a, e.get("type")) for a in attendus)
        ]
    fascicules = {p.lower() for p in indices.get("pdfs", set())}
    annee = loi.split("-", 1)[0]

    def cle(e: dict) -> tuple[bool, bool, bool]:
        ecart_pdf = (
            bool(fascicules) and (e.get("pdf_fr") or "").lower() not in fascicules
        )
        ecart_annee = not (e.get("date_signature") or "").startswith(annee)
        return est_rectificatif(e), ecart_pdf, ecart_annee

    return sorted(enregistrements, key=cle)


def chemin_fascicule(href: str | None) -> str | None:
    m = JORT_PDF_RE.search(href or "")
    return m.group(1).lower() if m else None


# --------------------------------------------------------------------------------
# Parcours des paramètres
# --------------------------------------------------------------------------------


def parcourir_noeuds(donnees: Any, nom: str, fichier: Path) -> Iterator[dict]:
    """Chaque nœud du fichier, ses valeurs, sa référence propre.

    Les valeurs d'OpenFisca-Tunisia sont le plus souvent portées par des nœuds
    *internes* : `traitement_de_base.yaml` n'a ni `values` ni `brackets` à sa racine,
    mais un `echelon_N` par échelon, chacun avec ses valeurs et sa référence. Ne
    regarder que la racine, comme le fait le script d'origine, reviendrait à ignorer
    les quatre cinquièmes du dépôt.
    """
    if not isinstance(donnees, dict):
        return
    metadonnees = donnees.get("metadata")
    metadonnees = metadonnees if isinstance(metadonnees, dict) else {}
    reference = metadonnees.get("reference", donnees.get("reference"))

    dates_valeurs: set[str] = set()
    # La valeur elle-même, et pas seulement sa date : une valeur nulle posée à la
    # création d'un grade n'est pas du même ordre qu'un montant non sourcé.
    valeurs_par_date: dict[str, Any] = {}
    if isinstance(donnees.get("values"), dict):
        dates_valeurs = {texte_date(c) for c in donnees["values"] if est_une_date(c)}
        for cle_date, contenu in donnees["values"].items():
            if est_une_date(cle_date) and isinstance(contenu, dict):
                valeurs_par_date[texte_date(cle_date)] = contenu.get("value")
    if isinstance(donnees.get("brackets"), list):
        for tranche in donnees["brackets"]:
            if isinstance(tranche, dict):
                for champ in tranche.values():
                    if isinstance(champ, dict):
                        dates_valeurs |= {
                            texte_date(c) for c in champ if est_une_date(c)
                        }

    yield {
        "nom": nom,
        "fichier": fichier,
        "description": donnees.get("description", ""),
        "valeurs": "values" in donnees or "brackets" in donnees,
        "dates_valeurs": sorted(dates_valeurs),
        "valeurs_par_date": valeurs_par_date,
        "reference": reference,
    }

    for cle, enfant in donnees.items():
        if cle in CLES_RESERVEES or not isinstance(enfant, dict):
            continue
        yield from parcourir_noeuds(enfant, f"{nom}.{cle}", fichier)


def collecter(corpus: CorpusJort) -> dict[str, Any]:
    fichiers: list[dict] = []
    noeuds: list[dict] = []
    indices: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"types": set(), "pdfs": set()}
    )

    for chemin in sorted(PARAMETERS_DIR.rglob("*.yaml")):
        relatif = chemin.relative_to(PARAMETERS_DIR)
        if relatif.name == "index.yaml":
            continue
        sous_arbre = relatif.parts[0] if len(relatif.parts) > 1 else "(racine)"
        racine = relatif.with_suffix("").as_posix().replace("/", ".")
        donnees = charger_yaml(chemin)
        du_fichier = list(parcourir_noeuds(donnees, racine, chemin))

        # Une référence portée par un ancêtre vaut pour ses descendants : elle ne
        # dit pas la même chose qu'une référence propre, mais le paramètre n'est
        # pas pour autant « sans aucune référence ».
        avec_ref = [n["nom"] for n in du_fichier if n["reference"] is not None]
        for noeud in du_fichier:
            noeud["sous_arbre"] = sous_arbre
            noeud["ref_propre"] = noeud["reference"] is not None
            noeud["ref_heritee"] = any(
                noeud["nom"].startswith(a + ".") for a in avec_ref
            )
            noeud["entrees"] = list(entrees_de_reference(noeud["reference"]))
            noeud["hotes"] = {
                h for h in (hote(e["href"]) for e in noeud["entrees"]) if h
            }
            noeud["libre"] = any(e["libre"] for e in noeud["entrees"])
            noeud["datee"] = any(e["date"] for e in noeud["entrees"])
            noeud["structuree"] = any(not e["libre"] for e in noeud["entrees"])
            noeud["avec_lien"] = any(e["href"] for e in noeud["entrees"])

            cites: list[tuple[str, str, str | None]] = []
            for entree in noeud["entrees"]:
                trouves = textes_cites(entree["titre"])
                for rang, (loi, type_cite) in enumerate(trouves):
                    indices[loi]["types"].add(type_cite)
                    cites.append((loi, type_cite, entree["date"]))
                    # Le lien vise le fascicule du *premier* texte nommé ; les
                    # suivants — « modifiant le décret n° … » — n'en reçoivent rien.
                    fascicule = chemin_fascicule(entree["href"])
                    if rang == 0 and fascicule:
                        indices[loi]["pdfs"].add(fascicule)
                noeud.setdefault("sans_numero", [])
                if not trouves and TEXTE_SANS_NUMERO_RE.search(entree["titre"]):
                    noeud["sans_numero"].append(entree["titre"][:140])
            noeud["cites"] = cites
            noeud.setdefault("sans_numero", [])
        noeuds.extend(du_fichier)

        entrees_fichier = [e for n in du_fichier for e in n["entrees"]]
        hotes_fichier = {h for h in (hote(e["href"]) for e in entrees_fichier) if h}
        fichiers.append(
            {
                "chemin": chemin,
                "sous_arbre": sous_arbre,
                "reference": any(n["ref_propre"] for n in du_fichier),
                "pist": HOTE_PROBANT in hotes_fichier,
                "gitlab": HOTE_NON_PROBANT in hotes_fichier,
                "noeuds": du_fichier,
            }
        )

    # Une requête par texte cité, toutes mémorisées.
    lois = sorted({loi for n in noeuds for loi, _, _ in n["cites"]})
    resolutions = {
        loi: classer_enregistrements(loi, corpus.enregistrements(loi), indices[loi])
        for loi in lois
    }
    return {
        "fichiers": fichiers,
        "noeuds": noeuds,
        "lois": lois,
        "resolutions": resolutions,
        "indices": indices,
    }


# --------------------------------------------------------------------------------
# Arbre chargé contre arbre sur le disque
# --------------------------------------------------------------------------------


def noms_charges() -> set[str] | None:
    """Les noms de paramètres qu'OpenFisca charge réellement, ou None s'il échoue."""
    try:
        from openfisca_core.parameters import ParameterNode
    except ImportError:
        return None
    racine = ParameterNode("", directory_path=str(PARAMETERS_DIR))
    noms: set[str] = set()

    def descendre(noeud: Any, chemin: str) -> None:
        if chemin:
            noms.add(chemin)
        for cle, enfant in (getattr(noeud, "children", None) or {}).items():
            descendre(enfant, f"{chemin}.{cle}" if chemin else cle)

    descendre(racine, "")
    return noms


def anomalies_de_chargement(charges: set[str] | None) -> dict[str, list]:
    """Ce qui est sur le disque mais hors de l'arbre chargé, ou mal nommé.

    Un paramètre invisible n'est pas seulement mal sourcé : il n'existe pas. Le
    contrôle vaut mieux qu'un chiffre de sourçage.
    """
    non_charges: list[dict] = []
    mal_nommes: list[dict] = []
    for chemin in sorted(PARAMETERS_DIR.rglob("*")):
        if chemin.is_dir() or chemin.name.startswith("."):
            continue
        relatif = chemin.relative_to(PARAMETERS_DIR)
        if chemin.suffix not in {".yaml", ".yml"}:
            frere = chemin.with_suffix(".yaml")
            non_charges.append(
                {
                    "chemin": relatif.as_posix(),
                    "lignes": len(
                        chemin.read_text(
                            encoding="utf-8", errors="replace"
                        ).splitlines()
                    ),
                    "motif": "sans extension `.yaml` : OpenFisca ne le lit pas",
                    "frere": frere.exists(),
                }
            )
            continue
        nom = relatif.with_suffix("").as_posix()
        if not re.fullmatch(r"[A-Za-z0-9_/]+", nom):
            impropres = sorted({c for c in nom if not re.match(r"[A-Za-z0-9_/]", c)})
            mal_nommes.append(
                {
                    "chemin": relatif.as_posix(),
                    "parametre": nom.replace("/", "."),
                    "caracteres": impropres,
                }
            )
    vides: list[str] = []
    if charges is not None:
        for chemin in sorted(PARAMETERS_DIR.rglob("*")):
            if not chemin.is_dir():
                continue
            relatif = chemin.relative_to(PARAMETERS_DIR)
            if not relatif.parts:
                continue
            nom = relatif.as_posix().replace("/", ".")
            a_des_donnees = any(
                f.name != "index.yaml" for f in chemin.iterdir() if f.is_file()
            ) or any(f.is_dir() for f in chemin.iterdir())
            if a_des_donnees and nom not in charges:
                vides.append(nom)
    return {"non_charges": non_charges, "mal_nommes": mal_nommes, "absents": vides}


# --------------------------------------------------------------------------------
# Rapport
# --------------------------------------------------------------------------------


def tableau(lignes: list[str], entete: list[str], alignement: list[str]) -> None:
    lignes.append("| " + " | ".join(entete) + " |")
    lignes.append("| " + " | ".join(alignement) + " |")


def rendre(
    donnees: dict[str, Any],
    chargement: dict[str, list],
    corpus: CorpusJort,
    duree: float,
    charges: set[str] | None,
) -> str:
    noeuds = donnees["noeuds"]
    fichiers = donnees["fichiers"]
    resolutions = donnees["resolutions"]
    porteurs = [n for n in noeuds if n["valeurs"]]

    L = [
        "# Audit des sources des paramètres d'OpenFisca-Tunisia",
        "",
        f"Généré le {dt.date.today().isoformat()} par "
        "`scripts/generate_source_audit.py`, en "
        f"{duree:.1f} s"
        + ("" if corpus.disponible else " (sans rapprochement JORT)")
        + ".",
        "",
        "Ce rapport mesure, par sous-arbre, ce que les paramètres disent de leur "
        "fondement juridique : combien portent une valeur, combien une référence, de "
        "quelle qualité est cette référence, et si le texte cité se retrouve dans le "
        "corpus du JORT.",
        "",
        "## Ce que compte ce rapport",
        "",
        "Un *fichier* de paramètres porte souvent plusieurs *paramètres* : "
        "`fonction_publique/.../traitement_de_base.yaml` n'a pas de valeur à sa "
        "racine, mais un `echelon_N` par échelon, chacun avec ses valeurs et sa "
        "référence. Les deux unités sont donc comptées séparément, et les colonnes "
        "le disent. Les `index.yaml`, qui ne portent que l'ordre d'affichage, sont "
        "exclus : c'est l'écart avec un `grep` naïf sur l'arborescence, qui en "
        "compte trois portant un champ `reference` et un lien `pist.tn`.",
        "",
    ]

    # -- Fichiers non chargés : d'abord, car un paramètre invisible n'existe pas.
    L += ["## Fichiers non chargés ou mal nommés", ""]
    if chargement["non_charges"]:
        L += [
            "Ces fichiers sont dans l'arborescence mais **hors de l'arbre chargé** : "
            "OpenFisca ne lit que les `.yaml` et `.yml`.",
            "",
        ]
        tableau(
            L,
            ["Fichier", "Lignes", "Motif", "`.yaml` voisin ?"],
            ["---", "---:", "---", "---"],
        )
        for entree in chargement["non_charges"]:
            voisin = "oui" if entree["frere"] else "**non**"
            L.append(
                f"| `{entree['chemin']}` | {entree['lignes']} | "
                f"{entree['motif']} | {voisin} |"
            )
    else:
        L.append("Tout fichier de l'arborescence porte une extension `.yaml`.")
    L.append("")
    if chargement["mal_nommes"]:
        L += [
            "Ces fichiers sont chargés, mais leur nom contient un caractère que "
            "l'accès pointé ne sait pas franchir : le paramètre existe et reste "
            "inatteignable par `parameters(period).<chemin>`.",
            "",
        ]
        tableau(
            L,
            ["Fichier", "Paramètre", "Caractères impropres", "Portée"],
            ["---", "---", "---", "---"],
        )
        for entree in chargement["mal_nommes"]:
            chars = ", ".join(f"`{c}`" for c in entree["caracteres"])
            portee = (
                "**inatteignable** en accès pointé"
                if " " in entree["parametre"]
                else "identifiant non ASCII"
            )
            L.append(
                f"| `{entree['chemin']}` | `{entree['parametre']}` | {chars} | "
                f"{portee} |"
            )
        L.append("")
    if chargement["absents"]:
        L += [
            "Répertoires porteurs de données dont le nœud n'apparaît pas dans "
            "l'arbre chargé :",
            "",
        ]
        L += [f"- `{nom}`" for nom in chargement["absents"]]
        L.append("")
    if charges is None:
        L += [
            "_L'arbre chargé n'a pas pu être construit (OpenFisca-Core absent) : "
            "seuls les contrôles sur le disque ont été faits._",
            "",
        ]

    # -- Synthèse par sous-arbre
    L += ["## Synthèse par sous-arbre", ""]
    tableau(
        L,
        [
            "Sous-arbre",
            "Fichiers",
            "Paramètres avec valeur",
            "dont référencés",
            "dont URL JORT",
            "dont sans rien",
        ],
        ["---", "---:", "---:", "---:", "---:", "---:"],
    )
    par_sous_arbre: dict[str, list[dict]] = defaultdict(list)
    for noeud in porteurs:
        par_sous_arbre[noeud["sous_arbre"]].append(noeud)
    fichiers_par_sous_arbre = Counter(f["sous_arbre"] for f in fichiers)

    def ligne_synthese(nom: str, lot: list[dict], nb_fichiers: int) -> str:
        ref = [n for n in lot if n["ref_propre"] or n["ref_heritee"]]
        jort = [n for n in lot if HOTE_PROBANT in n["hotes"]]
        rien = len(lot) - len(ref)
        return (
            f"| `{nom}` | {nb_fichiers} | {len(lot)} | "
            f"{len(ref)} | {len(jort)} | {rien} |"
        )

    for nom in sorted(par_sous_arbre):
        L.append(ligne_synthese(nom, par_sous_arbre[nom], fichiers_par_sous_arbre[nom]))
    L.append(ligne_synthese("**Ensemble**", porteurs, len(fichiers)))
    L.append("")
    L += [
        "La colonne « URL JORT » ne compte que les liens vers `www.pist.tn`, le "
        "fascicule officiel. Un paramètre est dit référencé s'il porte une "
        "référence propre ou s'il en hérite d'un nœud de son fichier.",
        "",
    ]

    # -- Niveaux de référence
    L += ["## Niveaux de référence", ""]
    references = [n for n in porteurs if n["ref_propre"]]
    hotes = Counter(h for n in porteurs for h in n["hotes"])
    fichiers_ref = sum(1 for f in fichiers if f["reference"])
    fichiers_pist = sum(1 for f in fichiers if f["pist"])
    fichiers_gitlab = sum(1 for f in fichiers if f["gitlab"])
    tableau(
        L, ["Niveau", "Fichiers", "Paramètres avec valeur"], ["---", "---:", "---:"]
    )
    L += [
        f"| Porte un champ `reference` | {fichiers_ref} | {len(references)} |",
        "| Référence **structurée** (dictionnaire, non chaîne libre) | – | "
        f"{sum(1 for n in porteurs if n['structuree'])} |",
        "| … dont **titre et lien** | – | "
        f"{sum(1 for n in porteurs if n['avec_lien'])} |",
        "| … dont **titre seul, sans lien** | – | "
        f"{sum(1 for n in porteurs if n['structuree'] and not n['avec_lien'])} |",
        "| Référence en **chaîne libre** | – | "
        f"{sum(1 for n in porteurs if n['libre'])} |",
        "| Référence **datée** (indexée par date de valeur) | – | "
        f"{sum(1 for n in porteurs if n['datee'])} |",
        "| Référence **globale** (non datée) | – | "
        f"{sum(1 for n in porteurs if n['ref_propre'] and not n['datee'])} |",
        f"| Lien **pist.tn** | {fichiers_pist} | {hotes[HOTE_PROBANT]} |",
        f"| Lien **gitlab.com** (non probant) | {fichiers_gitlab} | "
        f"{hotes[HOTE_NON_PROBANT]} |",
        "",
    ]
    autres = {
        h: c for h, c in hotes.items() if h not in (HOTE_PROBANT, HOTE_NON_PROBANT)
    }
    if autres:
        L += [
            "Autres hôtes cités : "
            + ", ".join(f"`{h}` ({c})" for h, c in sorted(autres.items()))
            + ".",
            "",
        ]
    L += [
        "La datation n'est presque jamais discriminante : la convention du dépôt "
        "indexe la référence par date de valeur. Le contrôle instructif est "
        "l'inverse — les dates de valeur **qu'aucune référence ne couvre** ; il est "
        "en section « Anomalies ».",
        "",
    ]

    # -- Paramètres sans aucune référence
    L += ["## Paramètres sans aucune référence", ""]
    sans = [n for n in porteurs if not n["ref_propre"] and not n["ref_heritee"]]
    if sans:
        L += [
            f"{len(sans)} paramètres portent une valeur sans qu'aucune référence, "
            "propre ou héritée, ne la fonde. Regroupés par fichier, le plus fourni "
            "en tête, vingt fichiers par sous-arbre au plus.",
            "",
        ]
        par_arbre_sans: dict[str, Counter] = defaultdict(Counter)
        for noeud in sans:
            relatif = noeud["fichier"].relative_to(PARAMETERS_DIR).as_posix()
            par_arbre_sans[noeud["sous_arbre"]][relatif] += 1
        for nom in sorted(
            par_arbre_sans, key=lambda k: -sum(par_arbre_sans[k].values())
        ):
            compteur = par_arbre_sans[nom]
            total = sum(compteur.values())
            L += [
                f"### `{nom}` — {total} paramètres dans {len(compteur)} fichiers",
                "",
            ]
            tableau(L, ["Fichier", "Paramètres sans référence"], ["---", "---:"])
            for fichier, nombre in compteur.most_common(20):
                L.append(f"| `{fichier}` | {nombre} |")
            if len(compteur) > 20:
                reste = sum(compteur.values()) - sum(
                    n for _, n in compteur.most_common(20)
                )
                L.append(f"| _…et {len(compteur) - 20} autres fichiers_ | {reste} |")
            L.append("")
    else:
        L += ["Tout paramètre porteur de valeur a une référence.", ""]

    # -- Textes cités
    L += ["## Textes cités et leur résolution dans le corpus JORT", ""]
    occurrences = Counter(loi for n in noeuds for loi, _, _ in n["cites"])
    if not corpus.disponible:
        L += [
            "_Rapprochement JORT désactivé (`--sans-jort`) : les textes sont "
            "listés, leur résolution ne l'est pas._",
            "",
        ]
    tableau(
        L,
        ["Texte cité", "Type cité", "Occurrences", "Résolution"],
        ["---", "---", "---:", "---"],
    )
    for loi in donnees["lois"]:
        types = ", ".join(sorted(donnees["indices"][loi]["types"])) or "–"
        classes = resolutions.get(loi) or []
        if not corpus.disponible:
            etat = "_non contrôlé_"
        elif classes:
            m = classes[0]
            etat = (
                f"JORT {m['jort_annee']}/{m['jort_numero']} du "
                f"{m['date_publication'] or '?'} "
                f"({m['type']} du {m['date_signature'] or '?'})"
            )
        else:
            etat = "**introuvable**"
        L.append(f"| `{loi}` | {types} | {occurrences[loi]} | {etat} |")
    L.append("")

    # -- Anomalies
    L += ["## Anomalies", ""]

    libres = [n for n in porteurs if n["libre"]]
    L += [f"### Référence en chaîne libre — {len(libres)} paramètres", ""]
    if libres:
        tableau(L, ["Paramètre", "Référence"], ["---", "---"])
        for noeud in libres[:40]:
            brut = next(e["titre"] for e in noeud["entrees"] if e["libre"])
            L.append(f"| `{noeud['nom']}` | {brut[:120]} |")
        if len(libres) > 40:
            L.append(f"| _…et {len(libres) - 40} autres_ | |")
    else:
        L.append("Aucune.")
    L.append("")

    gitlab = [n for n in porteurs if HOTE_NON_PROBANT in n["hotes"]]
    L += [
        f"### Lien gitlab.com — {len(gitlab)} paramètres",
        "",
        "Un dépôt personnel n'est pas une source officielle : ces liens doivent "
        "céder la place au fascicule du JORT sur `pist.tn`.",
        "",
    ]
    if gitlab:
        fichiers_gl = sorted(
            {n["fichier"].relative_to(PARAMETERS_DIR).as_posix() for n in gitlab}
        )
        L += [f"- `{f}`" for f in fichiers_gl]
    else:
        L.append("Aucun.")
    L.append("")

    introuvables = [
        loi for loi in donnees["lois"] if corpus.disponible and not resolutions.get(loi)
    ]
    L += [f"### Textes cités introuvables dans le corpus — {len(introuvables)}", ""]
    if introuvables:
        tableau(L, ["Texte", "Type cité", "Occurrences"], ["---", "---", "---:"])
        for loi in introuvables:
            types = ", ".join(sorted(donnees["indices"][loi]["types"])) or "–"
            L.append(f"| `{loi}` | {types} | {occurrences[loi]} |")
    else:
        L.append("Aucun." if corpus.disponible else "_Non contrôlé (`--sans-jort`)._")
    L.append("")

    sans_numero = [n for n in porteurs if n["sans_numero"]]
    L += [
        f"### Textes cités par leur seule date — {len(sans_numero)} paramètres",
        "",
        "Ces citations sont réelles mais insolubles contre un corpus indexé par "
        "numéro : « arrêté conjoint … du 19 mai 2020 ». Elles ne sont pas des "
        "références fautives, elles demandent un numéro.",
        "",
    ]
    if sans_numero:
        tableau(L, ["Paramètre", "Citation"], ["---", "---"])
        for noeud in sans_numero[:30]:
            L.append(f"| `{noeud['nom']}` | {noeud['sans_numero'][0]} |")
        if len(sans_numero) > 30:
            L.append(f"| _…et {len(sans_numero) - 30} autres_ | |")
    else:
        L.append("Aucune.")
    L.append("")

    # -- Date de valeur antérieure au texte
    # Regroupé par (texte, date de valeur) : le même couple se répète à l'identique
    # sur tous les échelons d'un grade, et la liste brute n'apprendrait rien de plus
    # que sa première ligne. C'est le nombre de couples distincts qui se corrige.
    anachronismes: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    total_anachronismes = 0
    for noeud in porteurs:
        for loi, _type, date in noeud["cites"]:
            if not date:
                continue
            classes = resolutions.get(loi) or []
            if not classes:
                continue
            signature = classes[0].get("date_signature")
            if not signature or date >= signature:
                continue
            total_anachronismes += 1
            cle = (loi, date, signature, classes[0].get("type") or "")
            groupe = anachronismes.setdefault(
                cle, {"parametres": 0, "fichiers": set(), "exemple": noeud["nom"]}
            )
            groupe["parametres"] += 1
            groupe["fichiers"].add(noeud["fichier"])
    L += [
        "### Date de valeur antérieure au texte qui la fonde — "
        f"{total_anachronismes} paramètres, {len(anachronismes)} couples distincts",
        "",
        "Une valeur qui prend effet **avant la signature** du texte cité. Ce n'est "
        "pas une erreur en soi : les décrets de rémunération tunisiens sont "
        "couramment rétroactifs, et le dépôt date délibérément ses valeurs à la "
        "date d'effet énoncée par le texte, non à sa signature. C'est donc une "
        "**file de revue**, pas une liste de fautes — mais c'est dans cette file "
        "que se trouvent les dates fausses et les textes cités à tort, et les "
        "écarts les plus larges sont les plus suspects. Le contrôle porte sur la "
        "signature et non sur la publication, qui ajouterait un bruit certain.",
        "",
    ]
    if anachronismes:
        tableau(
            L,
            [
                "Texte cité",
                "Signé le",
                "Date de valeur",
                "Écart",
                "Paramètres",
                "Fichiers",
                "Exemple",
            ],
            ["---", "---", "---", "---:", "---:", "---:", "---"],
        )
        ordonnes = sorted(anachronismes.items(), key=lambda e: -e[1]["parametres"])
        for (loi, date, signature, type_texte), groupe in ordonnes[:40]:
            ecart = (
                dt.date.fromisoformat(signature) - dt.date.fromisoformat(date)
            ).days
            L.append(
                f"| `{loi}` ({type_texte}) | {signature} | {date} | {ecart} j | "
                f"{groupe['parametres']} | {len(groupe['fichiers'])} | "
                f"`{groupe['exemple']}` |"
            )
        if len(anachronismes) > 40:
            L.append(f"| _…et {len(anachronismes) - 40} autres couples_ | | | | | | |")
        # Le volume dit où le travail est ; l'écart dit où l'erreur est probable.
        # Un décret rétroactif de six semaines ne surprend pas ; de quatre ans, si.
        par_ecart = sorted(
            anachronismes.items(),
            key=lambda e: (
                -(dt.date.fromisoformat(e[0][2]) - dt.date.fromisoformat(e[0][1])).days
            ),
        )
        L += [
            "",
            "Les dix écarts les plus larges, à regarder en premier :",
            "",
        ]
        tableau(
            L,
            ["Texte cité", "Signé le", "Date de valeur", "Écart", "Paramètres"],
            ["---", "---", "---", "---:", "---:"],
        )
        for (loi, date, signature, type_texte), groupe in par_ecart[:10]:
            ecart = (
                dt.date.fromisoformat(signature) - dt.date.fromisoformat(date)
            ).days
            L.append(
                f"| `{loi}` ({type_texte}) | {signature} | {date} | {ecart} j | "
                f"{groupe['parametres']} |"
            )
    else:
        L.append("Aucune." if corpus.disponible else "_Non contrôlé (`--sans-jort`)._")
    L.append("")

    # -- Dates de valeur qu'aucune référence ne couvre
    # Là encore, regroupé : la même date manquante se répète sur tous les échelons.
    decouvertes: dict[tuple[str, str], dict[str, Any]] = {}
    total_decouverts = 0
    total_non_nuls = 0
    for noeud in porteurs:
        if not noeud["ref_propre"] or not noeud["datee"]:
            continue
        couvertes = {e["date"] for e in noeud["entrees"] if e["date"]}
        manquantes = [d for d in noeud["dates_valeurs"] if d not in couvertes]
        if not manquantes:
            continue
        # Une date non couverte dont la valeur est nulle marque le plus souvent la
        # création d'un grade, pas un montant non sourcé. Les deux sont comptées,
        # mais séparément : seule la seconde est une lacune de source indiscutable.
        valeurs = noeud["valeurs_par_date"]
        non_nulles = [d for d in manquantes if valeurs.get(d) not in (0, 0.0)]
        total_decouverts += 1
        if non_nulles:
            total_non_nuls += 1
        relatif = noeud["fichier"].relative_to(PARAMETERS_DIR).as_posix()
        cle = (relatif, ", ".join(manquantes))
        groupe = decouvertes.setdefault(cle, {"parametres": 0, "non_nulles": 0})
        groupe["parametres"] += 1
        if non_nulles:
            groupe["non_nulles"] += 1
    L += [
        "### Dates de valeur qu'aucune référence ne couvre — "
        f"{total_decouverts} paramètres dans "
        f"{len({f for f, _ in decouvertes})} fichiers, "
        f"dont **{total_non_nuls} à valeur non nulle**",
        "",
        "Le paramètre porte une référence datée, mais l'une de ses dates de valeur "
        "n'y figure pas : cette valeur-là n'est fondée par rien.",
        "",
        "La distinction compte. Une date non couverte portant une valeur **nulle** "
        f"— {total_decouverts - total_non_nuls} des {total_decouverts} — marque "
        "d'ordinaire la création d'un grade, et son absence de source ne prête pas "
        "à conséquence. Les autres sont des **montants non sourcés**, et c'est là "
        "la lacune indiscutable. Le tableau est classé sur cette colonne.",
        "",
    ]
    if decouvertes:
        tableau(
            L,
            ["Fichier", "Dates non couvertes", "Paramètres", "dont valeur non nulle"],
            ["---", "---", "---:", "---:"],
        )
        ordonnes_dates = sorted(
            decouvertes.items(),
            key=lambda e: (-e[1]["non_nulles"], -e[1]["parametres"]),
        )
        for (relatif, dates), groupe in ordonnes_dates[:40]:
            L.append(
                f"| `{relatif}` | {dates} | {groupe['parametres']} | "
                f"{groupe['non_nulles']} |"
            )
        if len(decouvertes) > 40:
            L.append(f"| _…et {len(decouvertes) - 40} autres_ | | | |")
    else:
        L.append("Aucune.")
    L.append("")

    return "\n".join(L) + "\n"


def main() -> None:
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument(
        "--sans-jort",
        action="store_true",
        help="saute le rapprochement avec le corpus JORT (usage rapide)",
    )
    analyseur.add_argument(
        "--corpus-jort",
        type=Path,
        default=None,
        help="chemin de `jort_cache.db` (par défaut : recherché dans les dépôts voisins)",
    )
    analyseur.add_argument(
        "--sortie", type=Path, default=REPORT_PATH, help="chemin du rapport"
    )
    arguments = analyseur.parse_args()

    debut = time.perf_counter()
    chemin_corpus = arguments.corpus_jort or trouver_corpus_jort()
    if not arguments.sans_jort and chemin_corpus is None:
        print(
            "Corpus JORT introuvable : rapprochement ignoré. "
            "Indiquez-le avec --corpus-jort, ou demandez --sans-jort."
        )
    corpus = CorpusJort(chemin_corpus, actif=not arguments.sans_jort)
    try:
        donnees = collecter(corpus)
        charges = noms_charges()
        chargement = anomalies_de_chargement(charges)
        duree = time.perf_counter() - debut
        rapport = rendre(donnees, chargement, corpus, duree, charges)
    finally:
        corpus.fermer()

    arguments.sortie.parent.mkdir(parents=True, exist_ok=True)
    arguments.sortie.write_text(rapport, encoding="utf-8")
    print(f"{arguments.sortie} écrit en {duree:.1f} s")


if __name__ == "__main__":
    main()

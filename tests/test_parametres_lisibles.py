"""Deux gardes sur la prose des fichiers de paramètres.

Un arbre de paramètres est un magasin de valeurs datées. Il doit pouvoir vivre comme une
base indépendante des formules, et se lire avec le seul texte de droit.

CES DEUX GARDES SONT NÉES D'ACCIDENTS RÉELS.

  1. L'issue openfisca-tunisia-pension#46 est née de six mentions du modèle dans des
     paramètres, dont cinq étaient devenues FAUSSES après qu'une version eut branché les
     formules qu'elles disaient absentes. Une phrase qui décrit le modèle se périme ; le
     droit qu'elle entoure, non.
  2. Dans openfisca-tunisia, la PR #430 a retiré deux de ces mentions ; la PR #432, coupée
     d'une branche antérieure, les a silencieusement réintroduites en fusionnant, et rien ne
     l'a signalé. Ces deux gardes y sont nées de cet accident, et sont portées ici parce que
     le même tic vient du même auteur.
"""

import pathlib
import re
import unicodedata

PARAMETRES = pathlib.Path(__file__).parent.parent / "openfisca_tunisia_pension" / "parameters"

# Tournures qui décrivent le modèle et non le droit.
MENTIONS_DU_MODELE = [
    r"aucune\s+(?:variable|formule)",
    r"\bl(?:a|es)\s+formules?\b",
    r"variable\s+d[’']entrée",
    r"\bentités?\b",
    r"\b(?:FoyerFiscal|Menage|Individu)\b",
    r"\ble\s+modèle\s+(?:porte|ne\s+sait|lit)",
]

# Sigles et chiffres romains : une suite de capitales n'est pas toujours un cri.
CAPITALES_ADMISES = {
    "JORT", "SMIG", "SMAG", "TVA", "CNSS", "CNRPS", "C.N.R.P.S", "CNR", "CPS",
    "CAVIS", "CNAM", "ICP", "CSS", "FTE", "AMEN", "IS", "IRPP", "LF", "URL",
    "FOPROLOS", "PNAFN", "AMG", "UHT", "ATMP", "BTAF", "PME", "CEA", "CEI",
    "HU", "TCL", "TFP", "BCT", "INS", "PIB", "OCDE", "TPE", "SMIG/SMAG",
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
}
PONCTUATION = "«»\"“”'’(),.;:!?—–-[]{}…"


def prose(texte):
    """Les tranches de PROSE : blocs `documentation` et champs `note`.

    Les `title`, les `description` et les valeurs portent des codes qui sont des
    données — `C/D`, `A1+300/A2+270`, « NON sommee » — et ne sont pas de la prose.
    """
    for m in re.finditer(r"^(\s*)documentation:\s*\|.*?\n", texte, re.M):
        indentation = len(m.group(1))
        fin = len(texte)
        for ligne in re.finditer(r"^(?![ \t]*$)([ \t]*)\S", texte[m.end():], re.M):
            if len(ligne.group(1)) <= indentation:
                fin = m.end() + ligne.start()
                break
        yield texte[m.end():fin]
    for m in re.finditer(r"^\s*note:\s*(.*)$", texte, re.M):
        yield m.group(1)


def fichiers():
    return sorted(PARAMETRES.rglob("*.yaml"))


def test_aucune_mention_du_modele():
    """Un paramètre ne nomme ni variable, ni formule, ni entité — pas même pour dire
    qu'aucune ne le lit."""
    fautes = []
    for f in fichiers():
        for bloc in prose(f.read_text(encoding="utf-8")):
            for motif in MENTIONS_DU_MODELE:
                for m in re.finditer(motif, bloc, re.I):
                    debut = max(0, m.start() - 40)
                    fautes.append(f"{f.relative_to(PARAMETRES)} : …{bloc[debut:m.end() + 40]}…")
    assert not fautes, "mentions du modèle dans des paramètres :\n" + "\n".join(fautes)


def est_capitalise(mot):
    noyau = mot.strip(PONCTUATION)
    if noyau in CAPITALES_ADMISES or any(c.isdigit() for c in noyau):
        return False
    lettres = [c for c in noyau if unicodedata.category(c).startswith("L")]
    return len(lettres) >= 3 and all(c.isupper() for c in lettres)


def test_aucune_emphase_en_capitales():
    """La prose d'un paramètre ne crie pas : l'emphase par capitales est une convention
    de commentaire de code, non de notice."""
    fautes = []
    for f in fichiers():
        for bloc in prose(f.read_text(encoding="utf-8")):
            mots = re.findall(r"\S+", bloc)
            for i in range(len(mots) - 1):
                if est_capitalise(mots[i]) and est_capitalise(mots[i + 1]):
                    fautes.append(f"{f.relative_to(PARAMETRES)} : « {mots[i]} {mots[i + 1]} »")
                    break
    assert not fautes, "emphase en capitales dans des paramètres :\n" + "\n".join(fautes)

"""Régime des salariés non agricoles."""

# Third Party
import numpy as np
from openfisca_core.errors import ParameterNotFoundError
from openfisca_core.model_api import (
    ADD,
    YEAR,
    Enum,
    Variable,
    apply_thresholds,
    max_,
)

# First Party
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites

# from openfisca_tunisia_pension.tools import add_vectorial_timedelta, year_


def dates_d_ouverture_du_droit(date_de_liquidation, annee):
    """Date d'ouverture du droit de chaque assuré, pour un exercice annuel.

    La date de liquidation est retenue quand elle tombe dans l'exercice ; sinon, le
    1er janvier de l'exercice, date à laquelle les variables annuelles du système
    lisent leurs paramètres.
    """
    annee_de_liquidation = (
        date_de_liquidation.astype("datetime64[Y]").astype(int) + 1970
    )
    premier_janvier = np.datetime64(f"{annee}-01-01", "D")
    return np.where(
        annee_de_liquidation == annee,
        date_de_liquidation.astype("datetime64[D]"),
        premier_janvier,
    )


def salaire_moyen_actualise(annee, salaire_par_annee, dates, salaire_reference_a):
    """Salaire moyen de référence, rédaction du décret n° 94-1429 (art. 18 et 19 nouveaux).

    Args:
        annee: année d'ouverture du droit ; ses salaires ne sont pas comptés.
        salaire_par_annee: fonction qui rend, pour une année de salaire, le salaire
            annuel de chaque assuré.
        dates: date d'ouverture du droit de chaque assuré (datetime64[D]).
        salaire_reference_a: fonction qui rend le nœud de paramètres
            `salaire_reference` à une date donnée.

    Sont retenues, en remontant depuis l'année qui précède l'ouverture du droit, les
    dernières années de salaire non nul, en nombre fixé par la durée de la fenêtre en
    vigueur à la date d'ouverture du droit ; si l'assuré en compte moins, la moyenne se
    fait sur celles-ci (art. 18, alinéa 2). Chaque salaire est multiplié par le
    coefficient de son année dans le barème d'actualisation applicable à cette même
    date. Le résultat est un montant annuel.
    """
    dates = np.asarray(dates, dtype="datetime64[D]")
    resultat = np.zeros(len(dates), dtype=np.float64)
    salaires_lus = {}

    def salaires(annee_de_salaire):
        if annee_de_salaire not in salaires_lus:
            salaires_lus[annee_de_salaire] = np.asarray(
                salaire_par_annee(annee_de_salaire), dtype=np.float64
            )
        return salaires_lus[annee_de_salaire]

    for date_d_ouverture in np.unique(dates):
        instant = str(date_d_ouverture)
        membres = dates == date_d_ouverture
        salaire_reference = salaire_reference_a(instant)
        nombre_annees = int(salaire_reference.duree_mois) // 12
        bareme = salaire_reference.actualisation
        premiere_annee = min(int(nom.removeprefix("annee_")) for nom in bareme)
        # Le barème applicable aux droits ouverts une année donne le coefficient 1 aux
        # salaires de l'année précédente. S'il manque, aucun barème n'est connu pour
        # cette année d'ouverture : erreur explicite plutôt qu'un barème plus ancien.
        try:
            getattr(bareme, f"annee_{annee - 1}")
        except ParameterNotFoundError as error:
            raise ParameterNotFoundError(
                f"retraite.rsna.salaire_reference.actualisation.annee_{annee - 1}"
                f" (aucun barème d'actualisation identifié pour les droits ouverts"
                f" le {instant})",
                instant,
                variable_name="rsna_salaire_de_reference",
            ) from error
        total = np.zeros(membres.sum(), dtype=np.float64)
        retenues = np.zeros(membres.sum(), dtype=np.int64)
        for annee_de_salaire in range(annee - 1, premiere_annee - 1, -1):
            if (retenues >= nombre_annees).all():
                break
            salaire = salaires(annee_de_salaire)[membres]
            retenue = (salaire > 0) & (retenues < nombre_annees)
            if not retenue.any():
                continue
            try:
                coefficient = float(getattr(bareme, f"annee_{annee_de_salaire}"))
            except ParameterNotFoundError as error:
                raise ParameterNotFoundError(
                    f"retraite.rsna.salaire_reference.actualisation.annee_{annee_de_salaire}"
                    f" (aucun barème d'actualisation identifié ne donne de coefficient aux"
                    f" salaires de {annee_de_salaire} pour un droit ouvert le {instant})",
                    instant,
                    variable_name="rsna_salaire_de_reference",
                ) from error
            total += np.where(retenue, salaire * coefficient, 0.0)
            retenues += retenue
        resultat[membres] = total / np.maximum(retenues, 1)
    return resultat


class RegimeRSNA(AbstractRegimeEnAnnuites):
    name = "Régime des salariés non agricoles"
    variable_prefix = "rsna"
    parameters_prefix = "rsna"

    class RSNATypesRaisonDepartAnticipe(Enum):
        __order__ = "non_concerne licenciement_economique usure_prematuree_organisme mere_3_enfants convenance_personnelle"
        non_concerne = "Non concerné"
        # A partir de 50 ans :
        licenciement_economique = "Licenciement économique avec au minimum 60 mois de cotisations (20 trimestres)"
        usure_prematuree_organisme = "Usure prématurée de l'organisme médicalement constatée avec au minimum 60 mois de cotisations (20 trimestres)"
        mere_3_enfants = "Femme salariée, mère de 3 enfants en vie, justifiant d'au moins 180 mois de cotisations (60 trimestres)"
        # A partir de 55 ans :
        convenance_personnelle = (
            "Convenance personnelle, avec 360 mois de cotisations (120 trimestres)"
        )

    class eligible(Variable):
        value_type = bool
        entity = Individu
        label = "L'individu est éligible à une pension CNRPS"
        definition_period = YEAR

        def formula(individu, period, parameters):
            duree_assurance = individu("regime_name_duree_assurance", period=period)
            salaire_de_reference = individu(
                "regime_name_salaire_de_reference", period=period
            )
            age = individu("age", period=period)
            rsna = parameters(period).retraite.regime_name
            duree_stage_accomplie = duree_assurance > 4 * rsna.stage_requis
            critere_age_verifie = age >= rsna.age_legal
            return (
                duree_stage_accomplie * critere_age_verifie * (salaire_de_reference > 0)
            )

    class pension_minimale(Variable):
        value_type = float
        default_value = 0  # Pas de pension minimale par défaut, elle est à zéro
        entity = Individu
        definition_period = YEAR
        label = "Pension minimale"

        def formula(individu, period, parameters):
            rsna = parameters(period).retraite.regime_name
            pension_minimale = rsna.pension_minimale
            # TODO Annualiser le Smig
            smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
            duree_assurance = individu("regime_name_duree_assurance", period)
            # TODO: vérifier et corriger
            return apply_thresholds(
                duree_assurance / 4,
                [
                    rsna.stage_derog,
                    rsna.stage_requis,
                ],
                [
                    0,
                    pension_minimale.inf * smig_annuel,
                    pension_minimale.sup * smig_annuel,
                ],
            )

    class salaire_de_reference(Variable):
        value_type = float
        entity = Individu
        label = "Salaires de référence du régime des salariés non agricoles"
        definition_period = YEAR

        def formula_1974_01_01(individu, period, parameters):
            """Articles 18 et 19 du décret n° 74-499, dans leur rédaction de 1974.

            Les salaires des trois ou des cinq dernières années, la période la plus
            avantageuse étant retenue ; ces années sont celles qui précèdent le 1er janvier
            de l'année d'ouverture du droit, laquelle n'est donc pas comptée. Le salaire
            mensuel moyen est le 1/36 ou le 1/60 du total ; il est rendu ici en montant
            annuel, comme dans la rédaction de 1994.
            """
            salaire_reference = parameters(
                period
            ).retraite.regime_name.salaire_reference

            def moyenne_annuelle(nombre_annees, diviseur_mois):
                total = sum(
                    individu(
                        "regime_name_salaire_de_base",
                        period=period.offset(-rang, "year"),
                        options=[ADD],
                    )
                    for rang in range(1, int(nombre_annees) + 1)
                )
                return 12 * total / diviseur_mois

            return max_(
                moyenne_annuelle(
                    salaire_reference.periode_courte_annees,
                    salaire_reference.diviseur_court_mois,
                ),
                moyenne_annuelle(
                    salaire_reference.periode_longue_annees,
                    salaire_reference.diviseur_long_mois,
                ),
            )

        def formula_1990_09_23(individu, period, parameters):
            """Décret n° 90-1455 : dix années (article 18 nouveau), divisées par 36 ou 60 mois.

            L'article 18 nouveau retient dix années ; l'article 19, non modifié, divise
            toujours le total par 36 ou 60 mois. Les deux articles ne se concilient pas, et
            aucun texte publié ne dit lequel l'a emporté jusqu'au décret n° 94-1429. Aucune
            valeur n'est calculée plutôt qu'une valeur inventée.

            L'exercice 1994 fait exception pour les droits ouverts à compter du
            1er juillet 1994, date d'effet de la rédaction du décret n° 94-1429 : quand la
            date de liquidation de chaque assuré tombe entre le 1er juillet et le
            31 décembre 1994, le calcul suit cette rédaction.
            """
            if period.start.year == 1994:
                dates = dates_d_ouverture_du_droit(
                    individu("regime_name_liquidation_date", period), 1994
                )
                if (dates >= np.datetime64("1994-07-01")).all():
                    return salaire_moyen_actualise(
                        1994,
                        lambda annee: individu(
                            "regime_name_salaire_de_base",
                            period=period.offset(annee - 1994, "year"),
                            options=[ADD],
                        ),
                        dates,
                        lambda instant: parameters(
                            instant
                        ).retraite.regime_name.salaire_reference,
                    )
            raise NotImplementedError(
                "Salaire de référence du régime des salariés non agricoles du 23 septembre "
                "1990 au 30 juin 1994 : l'article 18 du décret n° 74-499, récrit par le "
                "décret n° 90-1455, retient dix années, et l'article 19, non modifié, divise "
                "leur total par 36 ou 60 mois. Les textes ne disent pas lequel l'emporte."
            )

        def formula_1994_07_01(individu, period, parameters):
            """Décret n° 94-1429 : articles 18 et 19 nouveaux, et barème d'actualisation.

            Les cinq, sept puis dix dernières années de salaire (au 1er juillet 1994, 1995
            et 1996) qui précèdent le 1er janvier de l'année d'ouverture du droit, chacune
            actualisée par le coefficient de son année au barème applicable à la date
            d'ouverture du droit. Cette date est la date de liquidation quand elle tombe
            dans l'exercice, le 1er janvier de l'exercice sinon.

            L'absence de barème pour l'année d'ouverture du droit arrête le calcul sur
            une erreur : c'est le cas à partir de 2025, faute de barème identifié après
            celui de 2024.
            """
            # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement
            annee = period.start.year
            return salaire_moyen_actualise(
                annee,
                lambda annee_de_salaire: individu(
                    "regime_name_salaire_de_base",
                    period=period.offset(annee_de_salaire - annee, "year"),
                    options=[ADD],
                ),
                dates_d_ouverture_du_droit(
                    individu("regime_name_liquidation_date", period), annee
                ),
                lambda instant: parameters(
                    instant
                ).retraite.regime_name.salaire_reference,
            )

"""Régime des salariés non agricoles."""

# Third Party
from numpy import apply_along_axis, vstack
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
from openfisca_tunisia_pension.tools import make_mean_over_largest

# from openfisca_tunisia_pension.tools import add_vectorial_timedelta, year_


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
            """
            raise NotImplementedError(
                "Salaire de référence du régime des salariés non agricoles du 23 septembre "
                "1990 au 30 juin 1994 : l'article 18 du décret n° 74-499, récrit par le "
                "décret n° 90-1455, retient dix années, et l'article 19, non modifié, divise "
                "leur total par 36 ou 60 mois. Les textes ne disent pas lequel l'emporte."
            )

        def formula_1994_07_01(individu, period):
            # TODO: gérer le nombre d'année n
            # TODO: plafonner les salaires à 6 fois le smig de l'année d'encaissement
            k = 10
            mean_over_largest = make_mean_over_largest(k=k)
            n = 40
            salaire_refererence = apply_along_axis(
                mean_over_largest,
                axis=0,
                arr=vstack(
                    [
                        individu(
                            "regime_name_salaire_de_base", period=year, options=[ADD]
                        )
                        for year in range(period.start.year, period.start.year - n, -1)
                    ]
                ),
            )
            return salaire_refererence

"""Régime de la Caisse nationale de retraite et de prévoyance sociale (CNRPS)."""

# Third Party
from numpy import apply_along_axis, select, vstack
from openfisca_core.model_api import (
    ADD,
    ETERNITY,
    YEAR,
    Variable,
    apply_thresholds,
    select,
    where,
)

# First Party
from openfisca_tunisia_pension.entities import Individu
from openfisca_tunisia_pension.regimes.regime import AbstractRegimeEnAnnuites
from openfisca_tunisia_pension.tools import make_mean_over_consecutive_largest

# Avant 1985

# La pension d’ancienneté pour cette modalité le droit est acquis lorsque la double condition
# - de 60 ans d’âge
# - et 30ans de services effectifs civils ou militaires est remplie.
# Sont dispensés de la condition d’âge les agents :
# - admis à la retraite d’office ;
# - révoqués sans suspension des droits à la pension ;
# - licenciés pour suppression d’emplois;
# - admis à la retraite pour incapacité physique ;
# - admis à la retraite pour insuffisance professionnelle.

# La pension proportionnelle, dont le droit est acquis :
# - Sans conditions d’âge ni de durée de services aux agents mis à la retraite pour incapacité physique imputable et non imputable aux services ;
# - Sans conditions de durée de services :
#   - aux agents mis à la retraite pour limite d’âge ;
#   - licenciés pour suppression d’emploi et ayant plus de 15ans de services ;
#   - aux femmes mères de 3 enfants âgés de moins de 16 ans ;
# - Sans conditions d’âge
#   - aux agents licenciés pour insuffisance professionnelle ;
# - Sur demande ou d’office aux agents de plus de 50 ans et plus de 20 ans de services.


# Après 1985

# Le départ à la retraite est prononcé :
# Lors de l'atteinte de l'âge légal de mise à retraite ;
# Avant l'atteinte de cet âge:
# a/ en cas d'invalidité physique ;
# b/ sur demande ;
# c/ en cas de démission ;
# d/ à l'initiative de l'employeur pour insuffisance professionnelle de l'agent ;
# e/ en cas de révocation ;
# f/ sur demande pour les mères de trois enfants;
# g/ d’office.


class RegimeCNRPS(AbstractRegimeEnAnnuites):
    name = "Régime des salariés non agricoles"
    variable_prefix = "cnrps"
    parameters_prefix = "cnrps"

    class eligible(Variable):
        value_type = bool
        entity = Individu
        label = "L'individu est éligible à une pension CNRPS"
        definition_period = YEAR

        def formula(individu, period, parameters):
            cnrps_duree = individu("regime_name_duree_assurance", period=period)
            cnss_duree = individu("cnss_duree_assurance", period=period)
            duree_totale = cnrps_duree + cnss_duree

            salaire_de_reference = individu(
                "regime_name_salaire_de_reference", period=period
            )
            age = individu("age", period=period)

            duree_requise_annees = individu("regime_name_duree_requise_annees", period)
            age_requis = individu("regime_name_age_requis", period)

            duree_de_service_minimale_accomplie = (
                duree_totale >= 4 * duree_requise_annees
            )
            critere_age_verifie = age >= age_requis

            return (
                duree_de_service_minimale_accomplie
                * critere_age_verifie
                * (salaire_de_reference > 0)
            )

    class duree_requise_annees(Variable):
        value_type = float
        entity = Individu
        label = "La durée d'assurance (en années) requise pour ouvrir le droit à la pension CNRPS"
        definition_period = YEAR

        def formula(individu, period, parameters):
            cnrps = parameters(period).retraite.regime_name
            duree_requise = cnrps.duree_de_service_minimale

            mere_3_enfants = individu("mere_3_enfants", period)
            depart_sur_demande = individu("depart_anticipe_sur_demande", period)
            astreignant = individu("fonction_astreignante", period)
            invalidite = individu("invalidite_physique", period)

            conditions = [
                invalidite,
                depart_sur_demande & astreignant,
                depart_sur_demande & ~astreignant,
                mere_3_enfants,
            ]

            choix = [
                0,
                cnrps.depart_anticipe.sur_demande.astreignants.duree_minimum,
                cnrps.depart_anticipe.sur_demande.cadre_commun.duree_minimum,
                cnrps.depart_anticipe.meres_3_enfants.duree_minimum,
            ]

            return select(conditions, choix, default=duree_requise)

    class age_requis(Variable):
        value_type = float
        entity = Individu
        label = "L'âge requis pour ouvrir le droit à la pension CNRPS"
        definition_period = YEAR

        def formula(individu, period, parameters):
            cnrps = parameters(period).retraite.regime_name
            age_legal_cadre_commun = cnrps.age_legal.civil.cadre_commun

            mere_3_enfants = individu("mere_3_enfants", period)
            depart_sur_demande = individu("depart_anticipe_sur_demande", period)
            astreignant = individu("fonction_astreignante", period)
            invalidite = individu("invalidite_physique", period)

            conditions = [
                invalidite,
                depart_sur_demande & astreignant,
                depart_sur_demande & ~astreignant,
                mere_3_enfants,
            ]

            choix = [
                0,
                cnrps.depart_anticipe.sur_demande.astreignants.age_minimum,
                cnrps.depart_anticipe.sur_demande.cadre_commun.age_minimum,
                cnrps.depart_anticipe.meres_3_enfants.age_minimum,
            ]

            return select(conditions, choix, default=age_legal_cadre_commun)

    class pension_minimale(Variable):
        value_type = float
        default_value = 0  # Pas de pension minimale par défaut, elle est à zéro
        entity = Individu
        definition_period = YEAR
        label = "Pension minimale"

        def formula(individu, period, parameters):
            cnrps = parameters(period).retraite.regime_name
            pension_minimale = cnrps.pension_minimale
            duree_de_service_minimale = cnrps.duree_de_service_minimale
            # TODO Annualiser le Smig
            smig_annuel = 12 * parameters(period).marche_travail.smig_40h_mensuel
            duree_assurance = individu("regime_name_duree_assurance", period)
            return apply_thresholds(
                duree_assurance / 4,
                [
                    pension_minimale.duree_service_allocation_vieillesse,
                    duree_de_service_minimale,
                ],
                [
                    0,
                    pension_minimale.allocation_vieillesse * smig_annuel,
                    pension_minimale.minimum_garanti * smig_annuel,
                ],
            )

    class salaire_de_reference_calcule_sur_demande(Variable):
        value_type = bool
        entity = Individu
        label = "Le salaire de référence du régime de la CNRPS est calculé à la demande de l'agent sur ses meilleures années"
        definition_period = ETERNITY

    class salaire_de_reference(Variable):
        value_type = float
        entity = Individu
        label = "Salaires de référence du régime de la CNRPS"
        definition_period = YEAR

        def formula(individu, period):
            """Dernière rémunération perçue ou les 2 plus élevées consécutives sur demande (Art 36 l 85-12)."""
            n = 40
            k = 2
            mean_over_largest = make_mean_over_consecutive_largest(k)
            moyenne_2_salaires_plus_eleves = apply_along_axis(
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

            derniere_remuneration = individu(
                "regime_name_salaire_de_base", period=period, options=[ADD]
            )

            salaire_refererence = where(
                individu(
                    "regime_name_salaire_de_reference_calcule_sur_demande", period
                ),
                moyenne_2_salaires_plus_eleves,
                derniere_remuneration,
            )
            return salaire_refererence

    class bonifications(Variable):
        value_type = float
        entity = Individu
        label = "Bonifications"
        definition_period = YEAR

        def formula(individu, period, parameters):
            bonifications = parameters(period).retraite.regime_name.bonifications
            cadre_actif = bonifications.cadre_actif

            duree_militaire = individu("duree_service_militaire", period)
            duree_actif = individu("duree_service_cadre_actif", period)

            # Article 32 de la loi n° 85-12 : 5 ans pour 35 ans de services, 4 ans
            # pour 25 ans, 3 ans pour 20 ans, 2 ans pour 15 ans. Les seuils restent
            # écrits ici ; ce sont les noms des paramètres qui portent les valeurs.
            bonus_actif = (
                (duree_actif >= 35) * cadre_actif.service_35
                + ((duree_actif >= 25) & (duree_actif < 35)) * cadre_actif.service_25
                + ((duree_actif >= 20) & (duree_actif < 25)) * cadre_actif.service_20
                + ((duree_actif >= 15) & (duree_actif < 20)) * cadre_actif.service_15
            )

            # Le seuil de 20 ans n'est porté par aucun paramètre et par aucun texte
            # lu : voir la documentation de bonifications/militaire/bonus.
            bonus_militaire = (duree_militaire >= 20) * bonifications.militaire.bonus

            return (bonus_militaire + bonus_actif) * 4

    class duree_assurance(Variable):
        value_type = int
        entity = Individu
        definition_period = YEAR
        label = (
            "Durée d'assurance totale incluant les bonifications (trimestres validés)"
        )

        def formula(individu, period):
            duree_effective = individu("regime_name_duree_assurance_annuelle", period)
            bonifications = individu("regime_name_bonifications", period)
            return duree_effective + bonifications

    class taux_de_liquidation(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Taux de liquidation de la pension"

        def formula(individu, period, parameters):
            bareme_annuite = parameters(period).retraite.regime_name.bareme_annuite
            duree_cnrps = individu("regime_name_duree_assurance", period)
            duree_cnss = individu("cnss_duree_assurance", period)
            duree_totale = duree_cnrps + duree_cnss

            duree_requise_annees = individu("regime_name_duree_requise_annees", period)
            duree_requise_trimestres = 4 * duree_requise_annees

            # Coordination proratisation applies only if CNRPS alone < required
            duree_base_calcul = where(
                duree_cnrps >= duree_requise_trimestres, duree_cnrps, duree_totale
            )

            taux_annuite = bareme_annuite.calc(duree_base_calcul)
            return taux_annuite

    class pension_brute(Variable):
        value_type = float
        entity = Individu
        definition_period = YEAR
        label = "Pension brute"

        def formula(individu, period, parameters):
            taux_de_liquidation = individu("regime_name_taux_de_liquidation", period)
            salaire_de_reference = individu("regime_name_salaire_de_reference", period)
            pension_theorique = taux_de_liquidation * salaire_de_reference

            duree_cnrps = individu("regime_name_duree_assurance", period)
            duree_cnss = individu("cnss_duree_assurance", period)
            duree_totale = duree_cnrps + duree_cnss

            duree_requise_annees = individu("regime_name_duree_requise_annees", period)
            duree_requise_trimestres = 4 * duree_requise_annees

            # Proratisation only if coordination is active
            ratio_proratisation = where(
                duree_cnrps >= duree_requise_trimestres,
                1.0,
                where(duree_totale > 0, duree_cnrps / duree_totale, 0.0),
            )

            return pension_theorique * ratio_proratisation

# Third Party
from openfisca_core.model_api import (
    MONTH,
    Variable,
    min_,
    set_input_dispatch_by_period,
    where,
)

# First Party
from openfisca_tunisia_pension.entities import Individu


class age_deces(Variable):
    value_type = int
    entity = Individu
    default_value = -1  # Not deceased
    definition_period = MONTH
    label = "Age au décès"
    set_input = set_input_dispatch_by_period


class deces_par_accident(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Décès suite à un accident (circulation, travail)"
    set_input = set_input_dispatch_by_period


class cnrps_duree_services_effectifs(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Durée des services effectifs (années complètes)"
    set_input = set_input_dispatch_by_period


class cnrps_remuneration_annuelle_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Rémunération annuelle de base au moment du décès"
    set_input = set_input_dispatch_by_period


class cnrps_pension_reference_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Montant de la pension dont l'agent bénéficiait ou aurait bénéficié"
    set_input = set_input_dispatch_by_period


class nombre_orphelins_eligibles(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Nombre d'enfants eligibles à la Pension Temporaire d'Orphelin (PTO)"
    set_input = set_input_dispatch_by_period


class conjoint_survivant_eligible(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Présence d'un conjoint survivant éligible à la pension de réversion"
    set_input = set_input_dispatch_by_period


class cnrps_capital_deces(Variable):
    value_type = float
    entity = Individu
    label = "Montant du Capital-Décès servi aux ayants droit"
    definition_period = MONTH

    def formula(individu, period, parameters):
        age_deces = individu("age_deces", period)
        is_accident = individu("deces_par_accident", period)
        r_annuelle = individu("cnrps_remuneration_annuelle_deces", period)
        duree_services = individu("cnrps_duree_services_effectifs", period)
        nb_enfants = individu("nombre_enfants_charge", period)

        # Returns 0 if not deceased
        is_deceased = age_deces >= 0

        capital_deces = parameters(period).retraite.cnrps.capital_deces

        # CD = R + MA + ME (décret 93-308, art. 5)
        # MA : majoration d'ancienneté -> 1/12 de R par année de service,
        # plafonnée à 18 mois de salaire.
        duree_retenue = min_(duree_services, capital_deces.plafond_anciennete_mois)
        MA = (r_annuelle / 12) * duree_retenue

        CD1 = r_annuelle + MA

        # ME : majoration enfants -> 10 % du montant de base par enfant à charge.
        ME = CD1 * capital_deces.majoration_par_enfant * nb_enfants

        CD_base = CD1 + ME

        # Décès en service commandé / par accident : capital doublé (art. 5).
        multiplier_accident = where(
            is_accident * (age_deces < 60),
            capital_deces.multiplicateur_deces_accidentel,
            1.0,
        )

        CD_actif = CD_base * multiplier_accident

        # Retraité : le capital est réduit selon l'âge au décès (art. 6) — 50 %
        # au-delà de 60 ans, puis 40/30/20/10 %. Agent en activité (<60) : 100 %.
        taux_retraite = capital_deces.taux_retraite_selon_age.calc(age_deces)

        CD_final = CD_actif * taux_retraite

        # Art. 6 : le capital-décès ne peut être inférieur au SMIG annuel
        # (plancher non encore appliqué ici).

        return CD_final * is_deceased


class cnrps_pension_de_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Pension de réversion servie au conjoint survivant"
    definition_period = MONTH

    def formula(individu, period, parameters):
        pension_ref = individu("cnrps_pension_reference_deces", period)
        eligible = individu("conjoint_survivant_eligible", period)
        nb_orphelins = individu("nombre_orphelins_eligibles", period)
        is_deceased = individu("age_deces", period) >= 0

        survivants = parameters(period).retraite.cnrps.survivants
        taux_conjoint = survivants.taux_conjoint  # 0,75 (loi 85-12, art. 43)
        taux_orphelin = survivants.taux_orphelin  # 0,10 (art. 45)
        plafond = survivants.plafond_cumul  # 1,0 (art. 45)
        taux_5 = survivants.taux_partage_5_orphelins  # 0,50 (art. 45)

        # Art. 45 : le total (conjoint + orphelins) ne dépasse pas la pension de
        # l'agent. Au-delà de 2 orphelins, la part du conjoint est réduite du
        # dépassement (plafond − N×taux_orphelin) ; à partir de 5 orphelins elle
        # est ramenée à 50 % (les 50 % restants partagés entre les orphelins).
        taux_reversion = where(
            nb_orphelins >= 5,
            taux_5,
            where(
                nb_orphelins >= 3,
                plafond - nb_orphelins * taux_orphelin,
                taux_conjoint,
            ),
        )

        return pension_ref * taux_reversion * eligible * is_deceased


class cnrps_pension_orphelins_totale(Variable):
    value_type = float
    entity = Individu
    label = "Montant total des pensions temporaires d'orphelins (PTO) servi"
    definition_period = MONTH

    def formula(individu, period, parameters):
        pension_ref = individu("cnrps_pension_reference_deces", period)
        conjoint_eligible = individu("conjoint_survivant_eligible", period)
        nb_orphelins = individu("nombre_orphelins_eligibles", period)
        is_deceased = individu("age_deces", period) >= 0

        survivants = parameters(period).retraite.cnrps.survivants
        taux_orphelin = survivants.taux_orphelin  # 0,10 (art. 45)
        taux_conjoint = survivants.taux_conjoint  # 0,75 (art. 43)
        plafond = survivants.plafond_cumul  # 1,0 (art. 45)
        taux_5 = survivants.taux_partage_5_orphelins  # 0,50 (art. 45)

        # 10 % par orphelin (art. 45).
        taux_orphelins = nb_orphelins * taux_orphelin

        taux_orphelins = where(
            conjoint_eligible,
            # Avec conjoint : à partir de 5 orphelins, ils se partagent 50 %
            # (le conjoint garde 50 %) ; en deçà, ils perçoivent N×10 %.
            where(nb_orphelins >= 5, taux_5, taux_orphelins),
            # Sans conjoint (art. 46) : la part du conjoint leur est répartie,
            # le total restant plafonné à la pension de l'agent.
            min_(plafond, nb_orphelins * taux_orphelin + taux_conjoint)
            * (nb_orphelins > 0),
        )

        return pension_ref * taux_orphelins * is_deceased

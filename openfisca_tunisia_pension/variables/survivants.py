# Third Party
from openfisca_core.model_api import (
    MONTH,
    Variable,
    max_,
    min_,
    not_,
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


# Régime des salariés non agricoles (décret n° 74-499, section 5, articles 29 à 38).


class rsna_pension_reference_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Pension de vieillesse ou d'invalidité dont le défunt bénéficiait ou aurait dû bénéficier (RSNA)"
    set_input = set_input_dispatch_by_period


class nombre_orphelins_pere_et_mere_eligibles(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Parmi les orphelins éligibles, nombre d'orphelins de père et de mère"
    set_input = set_input_dispatch_by_period


def _taux_orphelins(individu, period, survivants):
    """Somme des taux d'orphelins avant tout plafonnement.

    Commune aux régimes dont l'orphelin de père et de mère a un taux propre : le nœud
    `survivants` du régime porte `taux_orphelin` et `taux_orphelin_pere_et_mere`.
    """
    nb_orphelins = individu("nombre_orphelins_eligibles", period)
    nb_pere_et_mere = min_(
        individu("nombre_orphelins_pere_et_mere_eligibles", period), nb_orphelins
    )
    return (
        (nb_orphelins - nb_pere_et_mere) * survivants.taux_orphelin
        + nb_pere_et_mere * survivants.taux_orphelin_pere_et_mere
    )


def _rsna_taux_orphelins(individu, period, parameters):
    """Somme des taux d'orphelins du RSNA avant tout plafonnement (article 34).

    De 1974 à 1981, l'orphelin de père et de mère a un taux propre ; depuis le décret
    n° 81-188, les deux taux sont égaux et la distinction ne change plus rien.
    """
    return _taux_orphelins(
        individu, period, parameters(period).retraite.rsna.survivants
    )


class rsna_taux_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Taux de la pension du conjoint survivant, en part de la pension de l'assuré (RSNA)"
    definition_period = MONTH

    def formula_1974_01_01(individu, period, parameters):
        """Article 31 du décret n° 74-499 : la moitié de la pension de l'assuré."""
        survivants = parameters(period).retraite.rsna.survivants
        eligible = individu("conjoint_survivant_eligible", period)
        return survivants.taux_conjoint * eligible

    def formula_1981_02_19(individu, period, parameters):
        """Article 31, alinéa 2, ajouté par le décret n° 81-188, article 2.

        « Ce taux est majoré à concurrence de 75 % de la pension de vieillesse ou
        d'invalidité dont bénéficiait ou aurait dû bénéficier le défunt au moment de son
        décès, à condition qu'il n'y ait pas d'enfant bénéficiaire, ou que le total de la
        pension de veuve et d'orphelin ne dépasse pas le montant de la pension de l'assuré.
        En cas de dépassement la pension d'orphelin est réduite d'autant. »

        Lecture retenue : « à concurrence de » fixe un plafond. Le taux de la moitié est
        relevé jusqu'à 75 % tant que la pension du conjoint et celles des orphelins,
        additionnées, ne dépassent pas la pension de l'assuré. Sans orphelin, 75 % ; avec
        un orphelin à 30 %, 70 % ; dès que la moitié et les orphelins atteignent la
        pension de l'assuré, la moitié sans majoration.
        """
        survivants = parameters(period).retraite.rsna.survivants
        eligible = individu("conjoint_survivant_eligible", period)
        taux_orphelins = _rsna_taux_orphelins(individu, period, parameters)
        taux = max_(
            survivants.taux_conjoint,
            min_(survivants.taux_conjoint_majore, 1 - taux_orphelins),
        )
        return taux * eligible


class rsna_pension_de_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Pension de réversion servie au conjoint survivant (RSNA)"
    definition_period = MONTH

    def formula(individu, period):
        pension_reference = individu("rsna_pension_reference_deces", period)
        taux = individu("rsna_taux_reversion", period)
        decede = individu("age_deces", period) >= 0
        return pension_reference * taux * decede


class rsna_pension_orphelins_totale(Variable):
    value_type = float
    entity = Individu
    label = "Montant total des pensions d'orphelins servies (RSNA)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        """Articles 34 et 38 du décret n° 74-499.

        Le total des pensions du conjoint survivant et des orphelins ne dépasse pas la
        pension de l'assuré ; les pensions d'orphelins sont, le cas échéant, réduites
        temporairement. Le décret n° 97-291 récrit l'article 38 sans changer la règle.
        """
        pension_reference = individu("rsna_pension_reference_deces", period)
        taux_conjoint = individu("rsna_taux_reversion", period)
        taux_orphelins = _rsna_taux_orphelins(individu, period, parameters)
        decede = individu("age_deces", period) >= 0
        taux = min_(taux_orphelins, max_(1 - taux_conjoint, 0))
        return pension_reference * taux * decede


# Régime des salariés agricoles (loi n° 81-6, titre II, section III, articles 60 à 69).


class rsa_pension_reference_deces(Variable):
    value_type = float
    entity = Individu
    default_value = 0.0
    definition_period = MONTH
    label = "Pension de vieillesse ou d'invalidité dont le défunt bénéficiait ou aurait dû bénéficier (RSA)"
    set_input = set_input_dispatch_by_period


class conjoint_survivant_remarie(Variable):
    value_type = bool
    entity = Individu
    default_value = False
    definition_period = MONTH
    label = "Le conjoint survivant s'est remarié après le décès, et ce mariage n'est pas dissous"
    set_input = set_input_dispatch_by_period
    documentation = """
    Lu par le régime des salariés agricoles (loi n° 81-6, article 63). Jusqu'au 3 août 1996,
    le remariage de la veuve supprime sa pension : la dissolution du nouveau mariage ne la
    rétablit pas, et l'entrée reste alors vraie. Depuis le 4 août 1996 (loi n° 96-66), il la
    suspend seulement, s'il intervient avant l'âge fixé par
    `retraite.rsa.survivants.age_remariage_suspensif` ; la pension est rétablie au décès du
    nouveau conjoint ou à la dissolution du mariage. Faux par défaut : sans déclaration, le
    conjoint n'est pas remarié.
    """


class age_remariage_conjoint_survivant(Variable):
    value_type = int
    entity = Individu
    default_value = 0
    definition_period = MONTH
    label = "Âge du conjoint survivant à son remariage"
    set_input = set_input_dispatch_by_period


class rsa_taux_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Taux de la pension du conjoint survivant, en part de la pension de l'assuré (RSA)"
    definition_period = MONTH

    def formula_1981_01_01(individu, period, parameters):
        """Articles 60 à 63 de la loi n° 81-6, en vigueur le 1er janvier 1981 (article 88).

        La veuve, ou le veuf invalide, reçoit la moitié de la pension du défunt (article
        62). Le remariage supprime la pension (article 63).
        """
        survivants = parameters(period).retraite.rsa.survivants
        eligible = individu("conjoint_survivant_eligible", period)
        remarie = individu("conjoint_survivant_remarie", period)
        return survivants.taux_conjoint * eligible * not_(remarie)

    def formula_1996_08_04(individu, period, parameters):
        """Article 63 nouveau, loi n° 96-66, exécutoire le 4 août 1996.

        Le remariage ne suspend plus la pension que s'il intervient avant 55 ans ; la
        pension est rétablie au décès du nouveau conjoint ou à la dissolution du mariage.
        Le taux de l'article 62 ne change pas.
        """
        survivants = parameters(period).retraite.rsa.survivants
        eligible = individu("conjoint_survivant_eligible", period)
        suspendu = individu("conjoint_survivant_remarie", period) * (
            individu("age_remariage_conjoint_survivant", period)
            < survivants.age_remariage_suspensif
        )
        return survivants.taux_conjoint * eligible * not_(suspendu)


class rsa_pension_de_reversion(Variable):
    value_type = float
    entity = Individu
    label = "Pension de réversion servie au conjoint survivant (RSA)"
    definition_period = MONTH

    def formula(individu, period):
        pension_reference = individu("rsa_pension_reference_deces", period)
        taux = individu("rsa_taux_reversion", period)
        decede = individu("age_deces", period) >= 0
        return pension_reference * taux * decede


class rsa_pension_orphelins_totale(Variable):
    value_type = float
    entity = Individu
    label = "Montant total des pensions d'orphelins servies (RSA)"
    definition_period = MONTH

    def formula_1981_01_01(individu, period, parameters):
        """Articles 65, 66 et 69 de la loi n° 81-6.

        L'orphelin reçoit le cinquième de la pension du défunt, les trois dixièmes s'il est
        orphelin de père et de mère (article 65). Le total des pensions du conjoint et des
        orphelins ne dépasse pas la pension du défunt — la « pension de référence du mari »
        en 1981, la pension dont bénéficiait ou aurait pu bénéficier le défunt depuis la loi
        n° 96-66 (article 69) : les pensions d'orphelins sont réduites.
        """
        pension_reference = individu("rsa_pension_reference_deces", period)
        taux_conjoint = individu("rsa_taux_reversion", period)
        taux_orphelins = _taux_orphelins(
            individu, period, parameters(period).retraite.rsa.survivants
        )
        decede = individu("age_deces", period) >= 0
        taux = min_(taux_orphelins, max_(1 - taux_conjoint, 0))
        return pension_reference * taux * decede

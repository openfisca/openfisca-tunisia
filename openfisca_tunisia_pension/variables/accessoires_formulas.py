# Third Party
from openfisca_core.model_api import MONTH, Variable, max_, min_, where

# First Party
from openfisca_tunisia_pension.entities import Individu


class cnrps_indemnites_familiales(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel des indemnités familiales CNRPS"
    definition_period = MONTH

    def formula(individu, period, parameters):
        nb_enfants = individu("nombre_enfants_charge", period)
        params_if = parameters(period).retraite.cnrps.accessoires.indemnites_familiales

        # Calculate allowance per child based on their rank
        # Enfant 1
        mnt_1 = (nb_enfants >= 1) * params_if.rang_1
        # Enfant 2
        mnt_2 = (nb_enfants >= 2) * params_if.rang_2
        # Enfant 3
        mnt_3 = (nb_enfants >= 3) * params_if.rang_3

        # Au-delà du troisième rang, la loi n° 88-39 du 6 mai 1988 limite le droit
        # aux trois premiers enfants à compter du 1er janvier 1989, en réservant
        # expressément les droits acquis antérieurement. L'enfant handicapé ouvre
        # droit quel que soit son rang (loi n° 81-46, art. 18 ; décret n° 96-1906,
        # art. 3). Avant 1989, aucune limitation : le décret n° 86-611 fixe un taux
        # pour le quatrième enfant.
        enfants_au_dela = max_(0, nb_enfants - 3)
        droits_acquis = individu(
            "nombre_enfants_indemnite_familiale_droit_acquis", period
        )
        handicapes = individu(
            "nombre_enfants_handicapes_au_dela_du_troisieme_rang", period
        )
        enfants_ouvrant_droit_au_dela = where(
            params_if.limitation_trois_premiers_enfants,
            # On ne peut ouvrir droit pour plus d'enfants qu'il n'y en a.
            min_(enfants_au_dela, droits_acquis + handicapes),
            enfants_au_dela,
        )
        mnt_4_plus = enfants_ouvrant_droit_au_dela * params_if.rang_4_et_plus

        return mnt_1 + mnt_2 + mnt_3 + mnt_4_plus


class cnrps_indemnite_revenu_unique(Variable):
    value_type = float
    entity = Individu
    label = "Indemnité de Revenu Unique (IRU) CNRPS"
    definition_period = MONTH

    def formula(individu, period, parameters):
        nb_enfants = individu("nombre_enfants_charge", period)
        conjoint_sans_revenu = individu("conjoint_sans_revenu", period)
        mere_divorcee = individu("mere_divorcee_garde_enfants", period)

        # The pensioner must have formed a family and had a single income.
        # This is simplified here by checking if they declare the spouse has no income
        # or if it's a divorced mother with custody (who receives it directly per manual).
        eligible = conjoint_sans_revenu + mere_divorcee

        params_iru = parameters(
            period
        ).retraite.cnrps.accessoires.indemnite_revenu_unique

        # Determine amount based on number of children
        mnt_1 = (nb_enfants == 1) * getattr(params_iru, "1_enfant", 0)
        mnt_2 = (nb_enfants == 2) * getattr(params_iru, "2_enfants", 0)
        mnt_3_plus = (nb_enfants >= 3) * getattr(params_iru, "3_enfants_et_plus", 0)

        return (mnt_1 + mnt_2 + mnt_3_plus) * eligible

# Third Party
from openfisca_core.model_api import MONTH, Variable, max_, min_

# First Party
from openfisca_tunisia_pension.entities import Individu


def _indemnite_des_trois_premiers_rangs(nb_enfants, params_if):
    """Les trois premiers rangs, dus sous tous les régimes successifs.

    Aucun texte lu n'a jamais limité le droit en deçà du troisième enfant : seul
    le sort des rangs suivants change au 1er janvier 1989.
    """
    return (
        (nb_enfants >= 1) * params_if.rang_1
        + (nb_enfants >= 2) * params_if.rang_2
        + (nb_enfants >= 3) * params_if.rang_3
    )


class cnrps_indemnites_familiales(Variable):
    value_type = float
    entity = Individu
    label = "Montant mensuel des indemnités familiales CNRPS"
    definition_period = MONTH

    def formula_1986_05_01(individu, period, parameters):
        """Chaque enfant au-delà du troisième rang ouvre droit à l'indemnité.

        Le décret n° 86-611 du 3 juin 1986, portant fixation des taux des
        indemnités à caractère familial (JORT n° 34 des 3-6 juin 1986, p. 674),
        fixe à son article premier quatre taux mensuels — premier enfant 7,600
        dinars, deuxième 6,500, troisième 5,600, quatrième 4,700. Aucun texte lu
        ne limite alors le nombre d'enfants ouvrant droit.

        La formule commence au 1er mai 1986, date d'effet que donne l'article 3
        du décret et première date portée par les quatre paramètres de rang :
        les lire plus tôt lèverait une ParameterNotFoundError. Avant cette date,
        la variable vaut zéro faute de taux publié, plutôt que d'interrompre le
        calcul.

        Les textes nomment le « quatrième enfant » ; cette formule applique son
        taux à chaque enfant au-delà du troisième, faute d'un texte lu qui
        tranche le sort du cinquième. Le point est posé en question ouverte.
        """
        nb_enfants = individu("nombre_enfants_charge", period)
        params_if = parameters(period).retraite.cnrps.accessoires.indemnites_familiales

        enfants_au_dela = max_(0, nb_enfants - 3)

        return (
            _indemnite_des_trois_premiers_rangs(nb_enfants, params_if)
            + enfants_au_dela * params_if.rang_4_et_plus
        )

    def formula_1989_01_01(individu, period, parameters):
        """Le droit est limité aux trois premiers enfants, sauf deux exceptions.

        La loi n° 88-39 du 6 mai 1988, relative à l'octroi des indemnités
        familiales dans le secteur public (JORT n° 33 du 13 mai 1988, p. 735),
        accorde l'indemnité par son article unique « dans la limite des trois
        premiers enfants », et dispose : « Les dispositions de la présente loi ne
        s'appliquent pas aux droits acquis antérieurement au 1er janvier 1989. »

        Deux catégories d'enfants échappent donc à la limitation, et le modèle
        les lit dans des variables d'entrée, puisqu'elles décrivent la situation
        d'un individu et non une règle :

        - ceux qui avaient **acquis le droit avant le 1er janvier 1989**, que la
          loi excepte expressément et dont le décret n° 96-1906 du 16 octobre
          1996 (article 2) fixe encore le taux au titre du « quatrième enfant
          ayant acquis ce droit antérieurement au 1er janvier 1989 » ;
        - l'**enfant handicapé**, qui ouvre droit quel que soit son rang (loi
          n° 81-46 du 29 mai 1981, article 18 ; décret n° 96-1906, article 3, qui
          lui donne le même taux).

        La date d'effet du 1er janvier 1989 est celle que l'article unique de la
        loi n° 88-39 réserve aux droits acquis, et celle qu'énonce l'article 2 du
        décret n° 88-1136 du 11 juin 1988, qui ne fixe plus que trois taux.
        """
        nb_enfants = individu("nombre_enfants_charge", period)
        params_if = parameters(period).retraite.cnrps.accessoires.indemnites_familiales

        enfants_au_dela = max_(0, nb_enfants - 3)
        droits_acquis = individu(
            "nombre_enfants_indemnite_familiale_droit_acquis", period
        )
        handicapes = individu(
            "nombre_enfants_handicapes_au_dela_du_troisieme_rang", period
        )
        # On ne peut ouvrir droit pour plus d'enfants qu'il n'y en a.
        enfants_ouvrant_droit_au_dela = min_(
            enfants_au_dela, droits_acquis + handicapes
        )

        return (
            _indemnite_des_trois_premiers_rangs(nb_enfants, params_if)
            + enfants_ouvrant_droit_au_dela * params_if.rang_4_et_plus
        )


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

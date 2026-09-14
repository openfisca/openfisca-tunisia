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
        """Les quatre premiers enfants ouvrent droit, et eux seuls.

        Le décret n° 86-611 du 3 juin 1986, portant fixation des taux des
        indemnités à caractère familial (JORT n° 34 des 3-6 juin 1986, p. 674),
        fixe à son article premier quatre taux mensuels, et quatre seulement —
        premier enfant 7,600 dinars, deuxième 6,500, troisième 5,600, quatrième
        4,700. Le barème s'arrête au quatrième rang : aucun taux n'est publié
        pour un cinquième enfant, qui n'ouvre donc aucun droit.

        La lecture est stricte, et non extensive : le taux du quatrième rang
        vaut pour le quatrième enfant, pas pour chacun de ceux qui le suivent.
        Le décret n° 96-1906 du 16 octobre 1996 confirme cette lecture en
        parlant au singulier du « quatrième enfant ayant acquis ce droit
        antérieurement au 1er janvier 1989 » (article 2).

        La formule commence au 1er mai 1986, date d'effet que donne l'article 3
        du décret et première date portée par les quatre paramètres de rang :
        les lire plus tôt lèverait une ParameterNotFoundError. Avant cette date,
        la variable vaut zéro faute de taux publié, plutôt que d'interrompre le
        calcul.
        """
        nb_enfants = individu("nombre_enfants_charge", period)
        params_if = parameters(period).retraite.cnrps.accessoires.indemnites_familiales

        # Le barème s'arrête au quatrième rang : au plus un enfant au-delà du
        # troisième, et non chacun de ceux qui suivent.
        quatrieme_enfant = min_(max_(0, nb_enfants - 3), 1)

        return (
            _indemnite_des_trois_premiers_rangs(nb_enfants, params_if)
            + quatrieme_enfant * params_if.rang_4
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
          ayant acquis ce droit antérieurement au 1er janvier 1989 ». Le texte
          parle du quatrième enfant, au singulier : le droit acquis ne vaut donc
          que pour un enfant, le barème ne connaissant pas de cinquième rang ;
        - l'**enfant handicapé**, qui ouvre droit quel que soit son rang (loi
          n° 81-46 du 29 mai 1981, article 18 ; décret n° 96-1906, article 3, qui
          vise « l'enfant handicapé venant après le 3e rang » et lui donne le
          même taux). Ici le rang est indifférent par disposition expresse : un
          cinquième enfant handicapé ouvre droit, et la limite du barème ne lui
          est pas opposable.

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
        # Le droit acquis ne vise que le quatrième enfant : un seul, quand bien
        # même plusieurs seraient déclarés. Le handicap, lui, ouvre droit quel
        # que soit le rang, et n'est donc pas borné de la même façon.
        droit_acquis_retenu = min_(droits_acquis, 1)
        # On ne peut ouvrir droit pour plus d'enfants qu'il n'y en a.
        enfants_ouvrant_droit_au_dela = min_(
            enfants_au_dela, droit_acquis_retenu + handicapes
        )

        return (
            _indemnite_des_trois_premiers_rangs(nb_enfants, params_if)
            + enfants_ouvrant_droit_au_dela * params_if.rang_4
        )


class cnrps_indemnite_revenu_unique(Variable):
    value_type = float
    entity = Individu
    label = "Indemnité de Revenu Unique (IRU) CNRPS"
    definition_period = MONTH

    def formula_1981_05_01(individu, period, parameters):
        """La majoration pour revenu unique, servie avec la pension.

        La loi n° 81-70 du 1er août 1981, modifiant la loi de finances pour la
        gestion 1981 (JORT n° 51 du 7 août 1981, p. 1789), ajoute par son
        article 4 un paragraphe V à l'article 22 de la loi n° 59-18 : « À la
        pension de retraite et à la pension de veuve s'ajoutent, le cas échéant,
        l'indemnité familiale et une majoration pour revenu unique attribuées
        dans les mêmes conditions et selon les mêmes taux et les mêmes modalités
        que les indemnités familiales et la majoration pour salaire unique
        servies aux agents en activité. » La loi n° 85-12 du 5 mars 1985,
        article 40, reconduit l'indemnité comme accessoire de la pension.

        La formule commence au 1er mai 1981, date d'**effet** que donne
        l'article 5 de la loi n° 81-70 — « L'article 4 de la présente loi prend
        effet à compter du 1er mai 1981 » — et non celle de sa signature ni de sa
        publication. C'est aussi la première date portée par les trois
        paramètres de montant. Avant cette date, le droit n'est pas ouvert aux
        retraités et la variable vaut zéro.

        Les montants eux-mêmes ne sont établis par aucun texte normatif : ils
        proviennent du manuel de liquidation de la caisse, qui ne cite pas leur
        source. Les paramètres le disent.
        """
        nb_enfants = individu("nombre_enfants_charge", period)
        conjoint_sans_revenu = individu("conjoint_sans_revenu", period)
        mere_divorcee = individu("mere_divorcee_garde_enfants", period)

        # Le droit suppose une famille et un revenu unique. La condition est
        # approchée ici par la déclaration d'un conjoint sans revenu, ou par
        # celle d'une mère divorcée ayant la garde, qui la perçoit directement
        # selon le manuel de la caisse.
        eligible = conjoint_sans_revenu + mere_divorcee

        params_iru = parameters(
            period
        ).retraite.cnrps.accessoires.indemnite_revenu_unique

        # `getattr` est ici le seul accès possible : « 1_enfant » n'est pas un
        # identifiant Python valide. Aucune valeur par défaut n'est passée, à
        # dessein : ParameterNotFoundError dérivant d'AttributeError, un défaut
        # transformerait un paramètre absent, mal orthographié ou renommé en un
        # zéro silencieux, que nul test ne verrait.
        mnt_1 = (nb_enfants == 1) * getattr(params_iru, "1_enfant")
        mnt_2 = (nb_enfants == 2) * getattr(params_iru, "2_enfants")
        mnt_3_plus = (nb_enfants >= 3) * getattr(params_iru, "3_enfants_et_plus")

        return (mnt_1 + mnt_2 + mnt_3_plus) * eligible

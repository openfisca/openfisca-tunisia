from numpy import (
    maximum as max_,
    minimum as min_,
    round,
)

from openfisca_core import periods


from openfisca_tunisia.variables.base import *  # noqa F401


class salaire_unique(Variable):
    value_type = bool
    entity = Menage
    label = "Indicatrice de salaire unique"
    definition_period = YEAR

    def formula(menage, period):
        salaire_imposable_personne_de_reference = menage.personne_de_reference(
            "salaire_imposable", period=period
        )
        salaire_imposable_conjoint = menage.conjoint("salaire_imposable", period=period)
        return xor_(
            salaire_imposable_personne_de_reference > 0, salaire_imposable_conjoint > 0
        )


# Allocations familiales
#
# Loi n° 60-30 du 14 décembre 1960, titre II, chapitre premier, section I (articles 52 à
# 65), en vigueur le 1er avril 1961 pour ces articles (article 130). Le montant est
# trimestriel (article 61) : il est ici réparti par tiers entre les mois du trimestre, chaque
# tiers calculé au droit en vigueur le premier jour du mois.


class TypesScolariteAllocationsFamiliales(Enum):
    __order__ = "aucune enseignement_primaire enseignement_second_degre_superieur_technique_professionnel"  # noqa: E501
    aucune = "Ne fréquente aucun établissement d'enseignement"
    enseignement_primaire = "Fréquente un établissement d'enseignement primaire"
    enseignement_second_degre_superieur_technique_professionnel = "Fréquente un établissement d'enseignement du second degré ou supérieur, technique ou professionnel"  # noqa: E501


class af_scolarite_enfant(Variable):
    value_type = Enum
    possible_values = TypesScolariteAllocationsFamiliales
    default_value = TypesScolariteAllocationsFamiliales.aucune
    entity = Individu
    label = "Établissement d'enseignement fréquenté régulièrement, au sens de l'article 54 de la loi n° 60-30"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class af_apprenti_remuneration_sous_plafond(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Enfant en apprentissage dont la rémunération ne dépasse pas 75 % du salaire minimum de référence"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Article 54 de la loi n° 60-30. Le salaire de référence est le salaire minimum légal du
    manœuvre du bâtiment dans la rédaction d'origine, et le SMIG du régime de 48 heures depuis
    la loi n° 96-65. Le premier n'étant pas connu ici, la comparaison est une entrée.
    """


class af_fille_remplacant_mere(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Fille qui remplace, auprès de ses frères et sœurs, la mère décédée, impotente, ou divorcée ou veuve occupant un emploi salarié absorbant toute son activité"  # noqa: E501
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class af_enfant_infirme(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Enfant infirme ou handicapé ouvrant droit aux allocations familiales au-delà de la limite d'âge"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Article 54 de la loi n° 60-30 : enfant qui, par suite d'infirmité ou de maladie incurable,
    est dans l'impossibilité permanente et absolue de se livrer à un travail salarié, et n'est
    pas pris en charge par un organisme public ou un organisme privé bénéficiant de l'aide de
    l'État ou des collectivités locales. Depuis la loi n° 96-65, aussi l'handicapé titulaire
    d'une carte d'handicapé qui n'est pas pris en charge intégralement.
    """


class af_droit_acquis(Variable):
    value_type = bool
    default_value = False
    entity = Individu
    label = "Enfant dont le droit aux allocations familiales est maintenu au-delà du nombre maximal d'enfants"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Deux textes maintiennent le droit d'un enfant venu au-delà du rang utile.

    - Loi n° 60-30, articles 127 et 128 : à titre transitoire, la limitation au quatrième
      enfant ne s'applique pas aux travailleurs dont les droits sont nés avant l'entrée en
      vigueur de la loi, le 1er avril 1961, pour les enfants nés avant le 1er janvier 1961.
      Les droits nés et déjà liquidés avant cette date restent régis par la législation
      antérieure (article 127, 1°), qui n'est pas connue ici : seul le 2° est couvert.
    - Loi n° 88-38, article 5 : le passage de quatre à trois enfants, au 1er janvier 1989,
      maintient « les droits acquis antérieurement à cette date ».

    Par défaut, aucun droit n'est maintenu : sans déclaration, seuls les enfants en rang
    utile ouvrent droit.
    """


class af_rang_enfant(Variable):
    value_type = int
    default_value = 0
    entity = Individu
    label = "Rang de l'enfant dans l'ordre de primogéniture ou d'adoption, au sens de l'article 52 de la loi n° 60-30"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    documentation = """
    Le rang est calculé parmi les enfants du ménage, l'aîné ayant le rang 1. Un enfant aîné
    qui ne vit plus dans le ménage compte pourtant dans l'ordre de primogéniture : le rang se
    saisit alors en entrée. Un enfant décédé ne compte plus : l'enfant qui le suit vient en
    rang utile (article 52, alinéas 3 et 4, rédaction de la loi n° 88-38).
    """

    def formula(individu, period):
        est_enfant = individu.has_role(Menage.ENFANT)
        naissance = individu("date_naissance", period).astype("datetime64[D]").astype(int)
        rang = individu.get_rank(individu.menage, naissance, condition=est_enfant)
        return where(est_enfant, rang + 1, 0)


class prestations_familiales_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant ouvrant droit aux allocations familiales du fait de son âge et de sa situation"
    definition_period = MONTH
    reference = "https://www.pist.tn/jort/1960/1960F/Jo05760.pdf"

    def formula_1961_04_01(individu, period, parameters):
        """Article 54 de la loi n° 60-30, rédaction d'origine (JORT n° 57/1960, p. 1607)."""
        age_limite = parameters(
            period
        ).prestations.contributives.prestations_familiales.af.age_limite
        age = individu("age", period)
        scolarite = individu("af_scolarite_enfant", period)
        TypesScolarite = scolarite.possible_values
        sans_emploi_salarie = individu("salaire_de_base", period) <= 0
        return individu.has_role(Menage.ENFANT) * (
            (age < age_limite.sans_condition)
            + (age < age_limite.enseignement_primaire)
            * (scolarite == TypesScolarite.enseignement_primaire)
            + (age < age_limite.apprentissage)
            * individu("af_apprenti_remuneration_sous_plafond", period)
            + (age < age_limite.etudes)
            * (
                scolarite
                == TypesScolarite.enseignement_second_degre_superieur_technique_professionnel
            )
            * sans_emploi_salarie
            + (age < age_limite.fille_au_foyer)
            * individu("af_fille_remplacant_mere", period)
            + (age >= age_limite.infirmite) * individu("af_enfant_infirme", period)
        )

    def formula_1996_08_04(individu, period, parameters):
        """Article 54 nouveau, loi n° 96-65 (JORT n° 60/1996, p. 1603).

        Sans clause d'entrée en vigueur, la loi devient exécutoire le 4 août 1996, cinq jours
        après le dépôt du fascicule, le 30 juillet (loi n° 93-64, article 2). La condition
        propre à l'enseignement primaire disparaît.
        """
        age_limite = parameters(
            period
        ).prestations.contributives.prestations_familiales.af.age_limite
        age = individu("age", period)
        scolarite = individu("af_scolarite_enfant", period)
        TypesScolarite = scolarite.possible_values
        sans_emploi_salarie = individu("salaire_de_base", period) <= 0
        return individu.has_role(Menage.ENFANT) * (
            (age < age_limite.sans_condition)
            + (age < age_limite.apprentissage)
            * individu("af_apprenti_remuneration_sous_plafond", period)
            + (age < age_limite.etudes)
            * (
                scolarite
                == TypesScolarite.enseignement_second_degre_superieur_technique_professionnel
            )
            * sans_emploi_salarie
            + (age < age_limite.fille_au_foyer)
            * individu("af_fille_remplacant_mere", period)
            + (age >= age_limite.infirmite) * individu("af_enfant_infirme", period)
        )


class af_enfant_ouvrant_droit(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant à charge venant en rang utile pour les allocations familiales"
    definition_period = MONTH

    def formula_1961_04_01(individu, period, parameters):
        """Article 52 : seuls ouvrent droit les premiers enfants, dans l'ordre de primogéniture.

        Le nombre maximal est de quatre (1961), puis de trois (loi n° 88-38, 1er janvier
        1989). Un enfant au-delà n'ouvre droit que si son droit est maintenu (`af_droit_acquis`).
        """
        af = parameters(period).prestations.contributives.prestations_familiales.af
        en_rang_utile = individu("af_rang_enfant", period) <= af.nb_enfants_max
        return individu("prestations_familiales_enfant_a_charge", period) * (
            en_rang_utile + individu("af_droit_acquis", period)
        )

    def formula_1996_08_04(individu, period, parameters):
        """Article 54 nouveau (loi n° 96-65) : l'enfant infirme ou handicapé au-delà de la
        limite d'âge est servi « quel que soit le rang »."""
        af = parameters(period).prestations.contributives.prestations_familiales.af
        en_rang_utile = individu("af_rang_enfant", period) <= af.nb_enfants_max
        hors_rang = (individu("age", period) >= af.age_limite.infirmite) * individu(
            "af_enfant_infirme", period
        )
        return individu("prestations_familiales_enfant_a_charge", period) * (
            en_rang_utile + individu("af_droit_acquis", period) + hors_rang
        )


class af_nbenf(Variable):
    value_type = int
    entity = Menage
    label = "Nombre d'enfants ouvrant droit aux allocations familiales"
    definition_period = MONTH

    def formula(menage, period):
        return menage.sum(menage.members("af_enfant_ouvrant_droit", period))


class af_remuneration_trimestrielle(Variable):
    value_type = float
    entity = Individu
    label = "Rémunération du trimestre servant de base aux allocations familiales"
    definition_period = MONTH

    def formula_1961_04_01(individu, period):
        """Article 61 : la rémunération trimestrielle effectivement perçue, déterminée
        conformément à l'article 42 (assiette des cotisations), du trimestre civil qui contient
        le mois. Seuls les salariés du régime de la loi n° 60-30 y ont droit (article 52)."""
        return _af_remuneration_trimestrielle(individu, period, ("rsna",))

    def formula_1989_10_01(individu, period):
        """Loi n° 89-73, articles 91 et 92 (titre III de la loi n° 81-6), en vigueur le
        1er octobre 1989 : les salariés du régime agricole amélioré reçoivent les allocations
        familiales pour les trois premiers enfants, aux conditions et aux taux des articles
        52 à 65 de la loi n° 60-30."""
        return _af_remuneration_trimestrielle(individu, period, ("rsna", "rsaa"))


def _af_remuneration_trimestrielle(individu, period, regimes):
    regime = individu("regime_securite_sociale_cotisant", period)
    ouvre_droit = sum(
        (regime == regime.possible_values[nom]) for nom in regimes
    )
    debut = period.start.offset("first-of", "month")
    premier_mois = periods.period(
        f"{debut.year}-{3 * ((debut.month - 1) // 3) + 1:02d}"
    )
    remuneration = sum(
        individu("assiette_cotisations_sociales", premier_mois.offset(k, "month"))
        for k in range(3)
    )
    return ouvre_droit * remuneration


class af_mensuelle(Variable):
    value_type = float
    entity = Menage
    label = "Allocations familiales, part du montant trimestriel afférente au mois"
    definition_period = MONTH

    def formula_1961_04_01(menage, period, parameters):
        """Article 61 : pourcentage par enfant de la rémunération trimestrielle plafonnée.

        Taux unique de 15 % par enfant en 1961 ; barème par rang depuis la loi n° 75-82
        (1er janvier 1976). L'enfant servi au-delà du quatrième, par droit maintenu
        (articles 127 et 128), reçoit le taux du quatrième rang.
        """
        af = parameters(period).prestations.contributives.prestations_familiales.af
        return _af_mensuelle(menage, period, af, af.taux.enf4)

    def formula_1989_01_01(menage, period, parameters):
        """Loi n° 88-38 : trois taux seulement depuis le 1er janvier 1989.

        L'article 5 maintient « les droits acquis antérieurement à cette date » : l'enfant
        servi au-delà du troisième, par droit maintenu, reçoit le taux du quatrième rang en
        vigueur le 31 décembre 1988. Depuis la loi n° 96-65, l'enfant infirme ou handicapé
        servi hors rang le reçoit aussi, faute d'un taux propre.
        """
        af = parameters(period).prestations.contributives.prestations_familiales.af
        taux_au_dela = parameters(
            "1988-12-31"
        ).prestations.contributives.prestations_familiales.af.taux.enf4
        return _af_mensuelle(menage, period, af, taux_au_dela)


def _af_mensuelle(menage, period, af, taux_au_dela):
    """Le tiers du montant trimestriel, au droit en vigueur le premier jour du mois.

    Article 55 : lorsque le père et la mère ouvrent tous deux droit, l'allocation la plus
    élevée est servie (en 1961, celle du père, la mère pouvant réclamer la différence ; depuis
    la loi n° 96-65, celle de la personne qui a la garde, ou la plus élevée). L'allocation
    étant proportionnelle à la rémunération, c'est celle de la rémunération la plus élevée.
    """
    remuneration = max_(
        menage.personne_de_reference("af_remuneration_trimestrielle", period),
        menage.conjoint("af_remuneration_trimestrielle", period),
    )
    base = min_(remuneration, af.plaf_trim)
    nombre = menage("af_nbenf", period)
    taux = (
        (nombre >= 1) * af.taux.enf1
        + (nombre >= 2) * af.taux.enf2
        + (nombre >= 3) * af.taux.enf3
        + max_(nombre - 3, 0) * taux_au_dela
    )
    return base * taux / 3


class af(Variable):
    value_type = float
    entity = Menage
    label = "Allocations familiales"
    definition_period = YEAR

    def formula(menage, period):
        return menage("af_mensuelle", period, options=[ADD])


class majoration_salaire_unique(Variable):
    value_type = float
    entity = Menage
    label = "Majoration du salaire unique"
    definition_period = YEAR  # TODO trimestrialiser

    def formula(menage, period, parameters):
        salaire_unique = menage("salaire_unique", period=period)
        # `af_nbenf` est mensuel : le nombre d'enfants est lu au premier mois de l'année.
        af_nbenf = menage("af_nbenf", period=period.first_month)
        P = parameters(period.start).prestations.contributives.prestations_familiales
        af_1enf = round(P.salaire_unique.enf1, 3)  # trimestrielle
        af_2enf = round(P.salaire_unique.enf2, 3)  # trimestrielle
        af_3enf = round(P.salaire_unique.enf3, 3)  # trimestrielle
        af = (
            (af_nbenf >= 1) * af_1enf
            + (af_nbenf >= 2) * af_2enf
            + (af_nbenf >= 3) * af_3enf
        )
        return 4 * af * salaire_unique  # annualisé


def _af_cong_naiss(age, _P):
    # _option={'age': ENFS}
    return 0


def _af_cong_jeun_trav(age, _P):
    #    Les salariés de moins de 18 ans du régime non agricole bénéficient de
    #    2 jours de congés par mois et au maximum 24 jours ouvrables,
    #    l'employeur se fera rembourser par la CNSS 12 jours de congés. Les
    #    salariés âgés de 18 à 20 ans bénéficient de 18 jours de congés
    #    ouvrables par an soit 6 jours remboursés à l'employeur par la CNSS.
    #    Le remboursement à l'employeur est effectué par la Caisse Nationale
    #    de Sécurité Sociale de l'avance faite en exécution de l'article 113
    #    alinéa 2 du Code du Travail.
    # , _option = {'age': ENFS}
    return 0


class contribution_frais_creche(Variable):
    value_type = float
    entity = Menage
    label = "Contribution aux frais de crêche"
    definition_period = YEAR

    def formula(menage, period, parameters):
        month = period.last_month
        smig48 = parameters(
            period.start
        ).marche_travail.smig_48h_mensuel  # TODO: smig 48H
        # TODO rework and test
        # Une prise en charge peut être accordée à la mère exerçant une
        # activité salariée et dont le salaire ne dépasse pas deux fois et demie
        # le SMIG pour 48 heures de travail par semaine. Cette contribution est
        # versée pour les enfants ouvrant droit aux prestations familiales et
        # dont l'âge est compris entre 2 et 36 mois. Elle s'élève à 15 dinars par
        # enfant et par mois pendant 11 mois.
        somme_salaire_imposable = menage.personne_de_reference(
            "salaire_imposable", period=month
        ) + menage.conjoint("salaire_imposable", period=month)
        age_en_mois = menage.members("age_en_mois", period=month)
        creche = parameters(
            period
        ).prestations.contributives.prestations_familiales.creche
        age_en_mois_benjamin = menage.min(age_en_mois)[0]

        elig_age = (age_en_mois_benjamin <= creche.age_max) * (
            age_en_mois_benjamin >= creche.age_min
        )
        elig_sal = somme_salaire_imposable < creche.plaf * smig48
        # duration of payment is at most `creche.duree` months, but we also
        # cannot give a negative number of months if the beneficiary is older
        # than one year. the original implementation used
        # `min(creche.duree, 12 - age_en_mois_benjamin)` which produces a
        # negative factor when the youngest child has more than 12 months.
        # clamp to zero to avoid negative contributions.
        months = max_(0, min_(creche.duree, 12 - age_en_mois_benjamin))
        return creche.montant * elig_age * elig_sal * months


class prestations_familiales(Variable):  # TODO add _af_cong_naiss, af_cong_jeun_trav
    value_type = float
    entity = Menage
    label = "Prestations familales"
    definition_period = YEAR

    def formula(menage, period):
        af = menage("af", period=period)
        majoration_salaire_unique = menage("majoration_salaire_unique", period=period)
        contribution_frais_creche = menage("contribution_frais_creche", period=period)
        return af + majoration_salaire_unique + contribution_frais_creche


#
# Assurances sociales   Maladie
#


def prestationl(age, sal, parameters):
    """
    Assurance sociale - prestation en espèces TODO: à compléter
    """
    # , _option = {'age': ENFS}
    #    P = _P.as.maladie
    P = 0
    mal = 0
    smig = parameters.marche_travail.smig
    return mal * P.part * max(P.plaf_mult * smig, sal) * P.duree


def _as_maternite(age, sal, parameters):
    """
    Assurance sociale - maternité  TODO: à compléter
    """
    # P = parameters.as.maternite
    # smig = parameters.marche_travail.smig
    # return P.part*max(P.plaf_mult*smig,sal)*P.duree
    return 0


def _as_deces(sal, paramters):
    """
    Assurance sociale - décès   # TODO: à compléter
    """
    # P = _P.as.deces
    return 0

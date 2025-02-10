from openfisca_tunisia.variables.base import *


class amen_social_presence_handicap_lourd(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage comprenant un membre avec un handicap lourd'
    definition_period = MONTH
    # Critères primaires du décret 2020-317 du 19 mai 2020
    # Handicap de niveau 3

    def formula_2020(menage, period, parameters):
        return menage.sum(menage.members('handicap', period) >= 3)


class amen_social_pas_d_achat_onereux(Variable):
    value_type = bool
    default_value = True
    entity = Menage
    label = "Ménage n'ayant pas fait d'achat onéreux"
    definition_period = ETERNITY
    # Critères primaires du décret 2020-317 du 19 mai 2020
    # Ni le chef du ménage ni aucun membre de son ménage n’a effectué une transaction d’achat
    # ou de vente d’un bien mobilier ou immobilier dont la valeur dépasse 30 fois le SMIG. Ce
    # critère est vérifiable actuellement uniquement pour les véhicules immatriculés par les
    # recoupements administratifs avec l’Agence Technique des Transports Terrestres (ATTT).


class amen_social_pas_de_residence_secondaire(Variable):
    value_type = bool
    default_value = True
    entity = Menage
    label = 'Ménage ne possédant pas de résidence secondaire'
    definition_period = ETERNITY
    # Critères primaires du décret 2020-317 du 19 mai 2020
    # Le ménage n’est pas propriétaire d’un logement secondaire


class amen_social_eligible(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au programme Amen social'
    definition_period = MONTH

    def formula_2020(menage, period, parameters):
        # Critères primaires du décret 2020-317 du 19 mai 2020
        pas_de_residence_secondaire = menage('amen_social_pas_de_residence_secondaire', period)
        pas_d_achat_onereux = menage('amen_social_pas_d_achat_onereux', period)

        # Citère du revenu selon présence ou non de handicap lourd
        presence_handicap_lourd = menage('amen_social_presence_handicap_lourd', period)
        taille_menage = menage.nb_persons()
        revenu_menage = menage('amen_social_revenu', period)
        seuil_de_revenu = parameters(period).prestations.non_contributives.amen_social.eligibilite
        smig_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        conditions_sans_handicap = [
            taille_menage == 1,
            taille_menage == 2,
            (taille_menage == 3) + (taille_menage == 4),
            taille_menage >= 5,
            ]
        valeurs_choisies_sans_handicap = [
            smig_mensuel * seuil_de_revenu.un_membre,
            smig_mensuel * seuil_de_revenu.deux_membres,
            smig_mensuel * seuil_de_revenu.trois_quatre_membres,
            smig_mensuel * seuil_de_revenu.plus_de_cinq_membres,
            ]

        conditions_avec_handicap = [
            (taille_menage == 1) * presence_handicap_lourd,
            (taille_menage == 2) * presence_handicap_lourd,
            ((taille_menage == 3) + (taille_menage == 4)) * presence_handicap_lourd,
            (taille_menage >= 5) * presence_handicap_lourd,
            ]
        valeurs_choisies_avec_handicap = [
            smig_mensuel * seuil_de_revenu.handicap_lourd.un_membre,
            smig_mensuel * seuil_de_revenu.handicap_lourd.deux_membres,
            smig_mensuel * seuil_de_revenu.handicap_lourd.trois_quatre_membres,
            smig_mensuel * seuil_de_revenu.handicap_lourd.plus_de_cinq_membres,
            ]

        critere_revenu = where(
            presence_handicap_lourd,
            revenu_menage <= select(conditions_avec_handicap, valeurs_choisies_avec_handicap),
            revenu_menage <= select(conditions_sans_handicap, valeurs_choisies_sans_handicap)
            )
        return pas_d_achat_onereux * pas_de_residence_secondaire * critere_revenu


class amen_social_revenu(Variable):
    value_type = float
    entity = Menage
    label = 'Revenu du ménage au sens du programme Amen social'
    definition_period = MONTH

    def formula_2020(menage, period, parameters):
        revenu_menage = (
            menage.sum(menage.members('salaire_net_a_payer', period))
            + menage.sum(menage.members('pension_de_retraite', period))
            )
        return revenu_menage


class transfert_monetaire_permanent_eligible(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au transfert monétaire permanent du programme Amen social'
    definition_period = MONTH

    def formula_2020(menage, period):
        return (
            menage('transfert_monetaire_permanent_eligibilite_score', period)
            + menage('transfert_monetaire_permanent_eligibilite_supplementaire', period)
            )


class transfert_monetaire_permanent_eligibilite_score(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au programme Amen social selon le modèle de ciblage'
    definition_period = MONTH

    def formula_2022_06(menage, period, parameters):
        decile = parameters(period).prestations.non_contributives.amen_social.decile
        return (
            menage('amen_social_eligible', period)
            + (menage('amen_social_score_decile', period) <= decile)
            )


class transfert_monetaire_permanent_eligibilite_supplementaire(Variable):
    value_type = bool
    entity = Menage
    label = "Ménage éligible au programme Amen social selon les critères supplémentaires d'éligibilité"
    definition_period = MONTH


class amen_social_enfants_a_charge(Variable):
    value_type = int
    entity = Menage
    label = 'Enfant considéré à charge au sens de la prestation Amen social'
    definition_period = MONTH

    def formula_2020(menage, period, parameters):
        age = menage.members('age', period)
        # Les enfants sont considérés comme elève dès 6 ans  (pris quand ?)
        # eleve = menage.members('eleve', period.this_year)
        etudiant = menage.members('etudiant', period.this_year)
        handicap = menage.members('handicap', period.this_year) == 3
        amen_social = parameters(period).prestations.non_contributives.amen_social.supplements
        condition_enfant = (age >= 6) * (age <= amen_social.limite_age_enfant)  # * eleve
        condition_jeune_etudiant = (age <= amen_social.limite_age_etudiant) * etudiant
        enfant_a_charge = condition_enfant + condition_jeune_etudiant + handicap
        return menage.sum(1 * enfant_a_charge, role = Menage.ENFANT)


class amen_social_enfants_handicapes_a_charge(Variable):
    value_type = int
    entity = Menage
    label = 'Enfant considéré à charge au sens de la prestation Amen social'
    definition_period = MONTH

    def formula_2020(menage, period, parameters):
        age = menage.members('age', period)
        handicap = menage.members('handicap', period.this_year) == 3
        amen_social = parameters(period).prestations.non_contributives.amen_social.supplements
        condition_enfant = (age >= 6) * (age <= amen_social.limite_age_enfant)
        condition_jeune_etudiant = (age <= amen_social.limite_age_etudiant)
        enfant_a_charge_handicape = (condition_enfant + condition_jeune_etudiant) * handicap
        return menage.sum(enfant_a_charge_handicape, role = Menage.ENFANT)


class transfert_monetaire_permanent(Variable):
    value_type = float
    entity = Menage
    label = 'Transfert monétaire permanent mensuel du programme Amen social'
    definition_period = MONTH

    def formula_2020(menage, period, parameters):
        amen_social = parameters(period).prestations.non_contributives.amen_social
        supplements = amen_social.supplements
        eligible = menage('transfert_monetaire_permanent_eligible', period)
        enfants_a_charge = menage('amen_social_enfants_a_charge', period)
        enfants_handicapes_a_charge = menage('amen_social_enfants_handicapes_a_charge', period)
        tmp = eligible * (
            amen_social.allocation_base
            + enfants_a_charge * supplements.amen_social_enfants_a_charge
            + enfants_handicapes_a_charge * supplements.amen_social_enfants_a_charge * supplements.handicap
            )
        return tmp

# TODO

# - séparer éligibilité AMEN et TMP
# - Coder éligibilité AMG1 et AMG2

# Amen regroupe amg1 amg2 et tmp

# sante_amg1

# sante_amg2
# - Limiter  Personne à charge : que enfant à charge
#
# Enfant en âge de scolairite que par âge 6- 18 an sauf demande attestaion pour rentrée scolaire
# pour prestation monétaire ou en nature

# - Rajouter allocations familiales
# Allocaion familiales
# Critère d'éligibilité inscrit à Amen et IS et décret 3.17 valide.
# 30 DT - de 0 à 18.
# Pas de score


# - Niveau de handicap
# handicap_leger, handicap_lourd

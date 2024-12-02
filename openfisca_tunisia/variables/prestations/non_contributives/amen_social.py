from openfisca_tunisia.variables.base import *


class amen_social_eligible(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au programme Amen social'
    definition_period = MONTH

    def formula(menage, period, parameters):
        taille_menage = menage.nb_persons()
        revenu_menage = menage.sum(menage.members('salaire_net_a_payer', period))   # Corriger les revenus
        seuil_de_revenu = parameters(period).prestations.non_contributives.amen_social.eligibilite
        smig_mensuel = smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        condiitons = [
            taille_menage == 1,
            taille_menage == 2,
            (taille_menage == 3) + (taille_menage == 4),
            taille_menage >= 5,
            ]
        valeurs_choisies = [
            smig_mensuel * seuil_de_revenu.un_membre,
            smig_mensuel * seuil_de_revenu.deux_membres,
            smig_mensuel * seuil_de_revenu.trois_quatre_membres,
            smig_mensuel * seuil_de_revenu.plus_de_cinq_membres,
            ]
        return revenu_menage <= select(condiitons, valeurs_choisies)

class transfert_monetaire_permanent_eligible(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au transfert monétaire permanent du programme Amen social'
    definition_period = MONTH

    def formula(menage, period):
        return (
            menage('transfert_monetaire_permanent_eligibilite_score', period)
            + menage('transfert_monetaire_permanent_eligibilite_supplementaire', period)
            )


class transfert_monetaire_permanent_eligibilite_score(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au programme Amen social selon le modèle de ciblage'
    definition_period = MONTH

    def formula(menage, period):
        return (
            menage('amen_social_eligible', period)
            + (menage('amen_social_score_decile', period) <= 2)
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

    def formula(menage, period, parameters):
        age = menage.members('age', period)
        eleve = menage.members('eleve', period.this_year)
        etudiant = menage.members('etudiant', period.this_year)
        invalide = menage.members('invalide', period.this_year)
        amen_social = parameters(period).prestations.non_contributives.amen_social.supplements
        condition_enfant = (age <= amen_social.limite_age_enfant) * eleve
        condition_jeune_etudiant = (age <= amen_social.limite_age_etudiant) * etudiant
        enfant_a_charge = condition_enfant + condition_jeune_etudiant + invalide
        return menage.sum(enfant_a_charge, role = Menage.ENFANT)


class transfert_monetaire_permanent(Variable):
    value_type = float
    entity = Menage
    label = 'Transfert monétaire permanent mensuel du programme Amen social'
    definition_period = MONTH

    def formula(menage, period, parameters):
        amen_social = parameters(period).prestations.non_contributives.amen_social
        eligible = menage('transfert_monetaire_permanent_eligible', period)

        allocation = eligible * (
            amen_social.allocation_base
            + amen_social_enfant_a_charge
            )

        return allocation

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
